import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as opensearchserverless from 'aws-cdk-lib/aws-opensearchserverless';
import * as cloudFront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path";

const projectName = `mcp-rag`; 
const region = process.env.CDK_DEFAULT_REGION;    
const accountId = process.env.CDK_DEFAULT_ACCOUNT;
const bucketName = `storage-for-${projectName}-${accountId}-${region}`; 
const vectorIndexName = projectName


export class CdkMcpRagStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Knowledge Base Role
    const knowledge_base_role = new iam.Role(this,  `role-knowledge-base-for-${projectName}`, {
      roleName: `role-knowledge-base-for-${projectName}-${region}`,
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal("bedrock.amazonaws.com")
      )
    });
    
    const bedrockInvokePolicy = new iam.PolicyStatement({ 
      effect: iam.Effect.ALLOW,
      resources: [
        `arn:aws:bedrock:us-west-2::foundation-model/*`,
        `arn:aws:bedrock:us-east-1::foundation-model/*`,
        `arn:aws:bedrock:us-east-2::foundation-model/*`
      ],
      // resources: ['*'],
      actions: [
        "bedrock:InvokeModel", 
        "bedrock:Retrieve", 
        "bedrock:InvokeModelEndpoint", 
        "bedrock:InvokeModelEndpointAsync",        
      ],
    });        
    knowledge_base_role.attachInlinePolicy( 
      new iam.Policy(this, `bedrock-invoke-policy-for-${projectName}`, {
        statements: [bedrockInvokePolicy],
      }),
    );  
    
    const bedrockKnowledgeBaseS3Policy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload",
        "s3:CreateBucket",
        "s3:PutObject",
        "s3:PutBucketLogging",
        "s3:PutBucketVersioning",
        "s3:PutBucketNotification",
      ],
    });
    knowledge_base_role.attachInlinePolicy( 
      new iam.Policy(this, `knowledge-base-s3-policy-for-${projectName}`, {
        statements: [bedrockKnowledgeBaseS3Policy],
      }),
    );  
    
    const knowledgeBaseOpenSearchPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ["aoss:APIAccessAll"],
    });
    knowledge_base_role.attachInlinePolicy( 
      new iam.Policy(this, `bedrock-agent-opensearch-policy-for-${projectName}`, {
        statements: [knowledgeBaseOpenSearchPolicy],
      }),
    );  

    const knowledgeBaseBedrockPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ["bedrock:*"],
    });
    knowledge_base_role.attachInlinePolicy( 
      new iam.Policy(this, `bedrock-agent-bedrock-policy-for-${projectName}`, {
        statements: [knowledgeBaseBedrockPolicy],
      }),
    );  

    // OpenSearch Serverless
    const collectionName = vectorIndexName
    const OpenSearchCollection = new opensearchserverless.CfnCollection(this, `opensearch-correction-for-${projectName}`, {
      name: collectionName,    
      description: `opensearch correction for ${projectName}`,
      standbyReplicas: 'DISABLED',
      type: 'VECTORSEARCH',
    });
    const collectionArn = OpenSearchCollection.attrArn

    new cdk.CfnOutput(this, `OpensearchCollectionEndpoint-${projectName}`, {
      value: OpenSearchCollection.attrCollectionEndpoint,
      description: 'The endpoint of opensearch correction',
    });

    const encPolicyName = `encription-${projectName}-${region}`
    const encPolicy = new opensearchserverless.CfnSecurityPolicy(this, `opensearch-encription-policy-for-${projectName}`, {
      name: encPolicyName,
      type: "encryption",
      description: `opensearch encryption policy for ${projectName}`,
      policy:
        `{"Rules":[{"ResourceType":"collection","Resource":["collection/${collectionName}"]}],"AWSOwnedKey":true}`,
    });
    OpenSearchCollection.addDependency(encPolicy);

    const netPolicyName = `network-${projectName}-${region}`
    const netPolicy = new opensearchserverless.CfnSecurityPolicy(this, `opensearch-network-policy-for-${projectName}`, {
      name: netPolicyName,
      type: 'network',    
      description: `opensearch network policy for ${projectName}`,
      policy: JSON.stringify([
        {
          Rules: [
            {
              ResourceType: "dashboard",
              Resource: [`collection/${collectionName}`],
            },
            {
              ResourceType: "collection",
              Resource: [`collection/${collectionName}`],              
            }
          ],
          AllowFromPublic: true,          
        },
      ]), 
      
    });
    OpenSearchCollection.addDependency(netPolicy);

    const account = new iam.AccountPrincipal(this.account)
    const dataAccessPolicyName = `data-${projectName}`
    const dataAccessPolicy = new opensearchserverless.CfnAccessPolicy(this, `opensearch-data-collection-policy-for-${projectName}`, {
      name: dataAccessPolicyName,
      type: "data",
      policy: JSON.stringify([
        {
          Rules: [
            {
              Resource: [`collection/${collectionName}`],
              Permission: [
                "aoss:CreateCollectionItems",
                "aoss:DeleteCollectionItems",
                "aoss:UpdateCollectionItems",
                "aoss:DescribeCollectionItems",
              ],
              ResourceType: "collection",
            },
            {
              Resource: [`index/${collectionName}/*`],
              Permission: [
                "aoss:CreateIndex",
                "aoss:DeleteIndex",
                "aoss:UpdateIndex",
                "aoss:DescribeIndex",
                "aoss:ReadDocument",
                "aoss:WriteDocument",
              ], 
              ResourceType: "index",
            }
          ],
          Principal: [
            account.arn
          ], 
        },
      ]),
    });
    OpenSearchCollection.addDependency(dataAccessPolicy);

    // s3 
    const s3Bucket = new s3.Bucket(this, `storage-${projectName}`,{
      bucketName: bucketName,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      publicReadAccess: false,
      versioned: false,
      cors: [
        {
          allowedHeaders: ['*'],
          allowedMethods: [
            s3.HttpMethods.POST,
            s3.HttpMethods.PUT,
          ],
          allowedOrigins: ['*'],
        },
      ],
    });
    new cdk.CfnOutput(this, 'bucketName', {
      value: s3Bucket.bucketName,
      description: 'The nmae of bucket',
    });

    // agent role
    const agent_role = new iam.Role(this,  `role-agent-for-${projectName}`, {
      roleName: `role-agent-for-${projectName}-${region}`,
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal("bedrock.amazonaws.com")
      )
    });

    const bedrockRetrievePolicy = new iam.PolicyStatement({ 
      effect: iam.Effect.ALLOW,
      resources: [
        `arn:aws:bedrock:${region}:${accountId}:knowledge-base/*`
      ],
      actions: [
        "bedrock:Retrieve"
      ],
    });        
    agent_role.attachInlinePolicy( 
      new iam.Policy(this, `bedrock-retrieve-policy-for-${projectName}`, {
        statements: [bedrockRetrievePolicy],
      }),
    );  
    
    const agentInferencePolicy = new iam.PolicyStatement({ 
      effect: iam.Effect.ALLOW,
      resources: [
        `arn:aws:bedrock:${region}:${accountId}:inference-profile/*`,
        `arn:aws:bedrock:*::foundation-model/*`
      ],
      actions: [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:GetInferenceProfile",
        "bedrock:GetFoundationModel"
      ],
    });        
    agent_role.attachInlinePolicy( 
      new iam.Policy(this, `agent-inference-policy-for-${projectName}`, {
        statements: [agentInferencePolicy],
      }),
    );  

    // Lambda Invoke
    agent_role.addToPolicy(new iam.PolicyStatement({
      resources: ['*'],
      actions: [
        'lambda:InvokeFunction',
        'cloudwatch:*'
      ]
    }));
    agent_role.addManagedPolicy({
      managedPolicyArn: 'arn:aws:iam::aws:policy/AWSLambdaExecute',
    });

    // Bedrock
    const BedrockPolicy = new iam.PolicyStatement({  
      resources: ['*'],
      actions: ['bedrock:*'],
    });     
    agent_role.attachInlinePolicy( // add bedrock policy
      new iam.Policy(this, `bedrock-policy-agent-for-${projectName}`, {
        statements: [BedrockPolicy],
      }),
    );   
    
    // Secret
    const langsmithApiSecret = new secretsmanager.Secret(this, `weather-langsmith-secret-for-${projectName}`, {
      description: 'secret for lamgsmith api key', // openweathermap
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      secretName: `langsmithapikey-${projectName}`,
      secretObjectValue: {
        langchain_project: cdk.SecretValue.unsafePlainText(projectName),
        langsmith_api_key: cdk.SecretValue.unsafePlainText(''),
      }, 
    });

    const tavilyApiSecret = new secretsmanager.Secret(this, `weather-tavily-secret-for-${projectName}`, {
      description: 'secret for lamgsmith api key', // openweathermap
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      secretName: `tavilyapikey-${projectName}`,
      secretObjectValue: {
        project_name: cdk.SecretValue.unsafePlainText(projectName),
        tavily_api_key: cdk.SecretValue.unsafePlainText(''),
      },
    });

    // cloudfront for sharing s3
    const distribution_sharing = new cloudFront.Distribution(this, `sharing-for-${projectName}`, {
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(s3Bucket),
        allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
        cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
        viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      priceClass: cloudFront.PriceClass.PRICE_CLASS_200,  
    });
    new cdk.CfnOutput(this, `distribution-sharing-DomainName-for-${projectName}`, {
      value: 'https://'+distribution_sharing.domainName,
      description: 'The domain name of the Distribution Sharing',
    });      
    
    // lambda-rag
    const roleLambdaRag = new iam.Role(this, `role-lambda-rag-for-${projectName}`, {
      roleName: `role-lambda-rag-for-${projectName}-${region}`,
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal("lambda.amazonaws.com"),
        new iam.ServicePrincipal("bedrock.amazonaws.com"),
      ),
      // managedPolicies: [cdk.aws_iam.ManagedPolicy.fromAwsManagedPolicyName('CloudWatchLogsFullAccess')] 
    });
    // roleLambdaRag.addManagedPolicy({  // grant log permission
    //   managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
    // });
    const CreateLogPolicy = new iam.PolicyStatement({  
      resources: [`arn:aws:logs:${region}:${accountId}:*`],
      actions: ['logs:CreateLogGroup'],
    });        
    roleLambdaRag.attachInlinePolicy( 
      new iam.Policy(this, `create-log-policy-lambda-rag-for-${projectName}`, {
        statements: [CreateLogPolicy],
      }),
    );
    const CreateLogStreamPolicy = new iam.PolicyStatement({  
      resources: [`arn:aws:logs:${region}:${accountId}:log-group:/aws/lambda/*`],
      actions: ["logs:CreateLogStream","logs:PutLogEvents"],
    });        
    roleLambdaRag.attachInlinePolicy( 
      new iam.Policy(this, `create-stream-log-policy-lambda-rag-for-${projectName}`, {
        statements: [CreateLogStreamPolicy],
      }),
    );      
    tavilyApiSecret.grantRead(roleLambdaRag) 

    // bedrock
    roleLambdaRag.attachInlinePolicy( 
      new iam.Policy(this, `tool-bedrock-invoke-policy-for-${projectName}`, {
        statements: [bedrockInvokePolicy],
      }),
    );  
    roleLambdaRag.attachInlinePolicy( 
      new iam.Policy(this, `tool-bedrock-agent-opensearch-policy-for-${projectName}`, {
        statements: [knowledgeBaseOpenSearchPolicy],
      }),
    );  
    roleLambdaRag.attachInlinePolicy( 
      new iam.Policy(this, `tool-bedrock-agent-bedrock-policy-for-${projectName}`, {
        statements: [knowledgeBaseBedrockPolicy],
      }),
    );  
    
    const lambdaRag = new lambda.DockerImageFunction(this, `lambda-rag-for-${projectName}`, {
      description: 'RAG based on Knoeledge Base',
      functionName: `lambda-rag-for-${projectName}`,
      code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../../lambda-rag')),
      timeout: cdk.Duration.seconds(120),
      role: roleLambdaRag,
      environment: {
        bedrock_region: String(region),
        projectName: projectName,
        "sharing_url": 'https://'+distribution_sharing.domainName,
      }
    });     
    
    lambdaRag.grantInvoke(new cdk.aws_iam.ServicePrincipal("bedrock.amazonaws.com")); 

  }
}
