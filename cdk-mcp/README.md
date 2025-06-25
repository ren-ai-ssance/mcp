# MCP RAG

### VPC 구성
```typescript
const vpc = new ec2.Vpc(this, `vpc-for-${projectName}`, {
  vpcName: `vpc-for-${projectName}`,
  maxAzs: 2,
  ipAddresses: ec2.IpAddresses.cidr("10.20.0.0/16"),
  natGateways: 1,
  createInternetGateway: true,
  subnetConfiguration: [
    {
      cidrMask: 24,
      name: `public-subnet-for-${projectName}`,
      subnetType: ec2.SubnetType.PUBLIC
    }, 
    {
      cidrMask: 24,
      name: `private-subnet-for-${projectName}`,
      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
    }
  ]
});
```

### OpenSearch Serverless 구성
```typescript
const OpenSearchCollection = new opensearchserverless.CfnCollection(this, `opensearch-correction-for-${projectName}`, {
  name: collectionName,    
  description: `opensearch correction for ${projectName}`,
  standbyReplicas: 'DISABLED',
  type: 'VECTORSEARCH',
});
```

### EC2 인스턴스 구성
```typescript
const appInstance = new ec2.Instance(this, `app-for-${projectName}`, {
  instanceName: `app-for-${projectName}`,
  instanceType: new ec2.InstanceType('m5.large'),
  machineImage: new ec2.AmazonLinuxImage({
    generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023
  }),
  vpc: vpc,
  vpcSubnets: {
    subnets: vpc.privateSubnets  
  },
  securityGroup: ec2Sg,
  role: ec2Role,
  userData: userData,
  blockDevices: [{
    deviceName: '/dev/xvda',
    volume: ec2.BlockDeviceVolume.ebs(80, {
      deleteOnTermination: true,
      encrypted: true,
    }),
  }],
});
```

### Lambda RAG 함수 구성
```typescript
const lambdaRag = new lambda.DockerImageFunction(this, `lambda-rag-for-${projectName}`, {
  description: 'RAG based on Knoeledge Base',
  functionName: `lambda-rag-for-${projectName}`,
  code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../../lambda-rag')),
  timeout: cdk.Duration.seconds(120),
  memorySize: 4096,
  role: roleLambdaRag,
  environment: {
    bedrock_region: String(region),
    projectName: projectName,
    "sharing_url": 'https://'+distribution.domainName,
  }
});
```

### CloudFront 배포 구성
```typescript
const distribution = new cloudFront.Distribution(this, `cloudfront-for-${projectName}`, {
  comment: `CloudFront-for-${projectName}`,
  defaultBehavior: {
    origin: albOrigin,
    viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
    cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
    originRequestPolicy: cloudFront.OriginRequestPolicy.ALL_VIEWER        
  },
  additionalBehaviors: {
    '/docs/*': {
      origin: s3Origin,
      viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
      cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
      originRequestPolicy: cloudFront.OriginRequestPolicy.CORS_S3_ORIGIN
    }
  }
});
```
