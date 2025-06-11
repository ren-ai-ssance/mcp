import chat
import logging
import sys
import utils

logging.basicConfig(
    level=logging.INFO,  # Default to INFO level
    format='%(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("mcp-cost")

config = utils.load_config()
print(f"config: {config}")

managed_opensearch_url = config["managed_opensearch_url"] if "managed_opensearch_url" in config else None
opensearch_username = config["opensearch_username"] if "opensearch_username" in config else None
opensearch_password = config["opensearch_password"] if "opensearch_password" in config else None

aws_region = config["region"] if "region" in config else "us-west-2"

mcp_user_config = {}    
def load_config(mcp_type):
    if mcp_type == "default":
        return {
            "mcpServers": {
                "search": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_basic.py"
                    ]
                }
            }
        }
    elif mcp_type == "image_generation":
        return {
            "mcpServers": {
                "imageGeneration": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_image_generation.py"
                    ]
                }
            }
        }    
    elif mcp_type == "airbnb":
        return {
            "mcpServers": {
                "airbnb": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@openbnb/mcp-server-airbnb",
                        "--ignore-robots-txt"
                    ]
                }
            }
        }
    elif mcp_type == "playwright":
        return {
            "mcpServers": {
                "playwright": {
                    "command": "npx",
                    "args": [
                        "@playwright/mcp@latest"
                    ]
                }
            }
        }
    elif mcp_type == "obsidian":
        return {
            "mcpServers": {
                "mcp-obsidian": {
                "command": "npx",
                "args": [
                    "-y",
                    "@smithery/cli@latest",
                    "run",
                    "mcp-obsidian",
                    "--config",
                    "{\"vaultPath\":\"/\"}"
                ]
                }
            }
        }
    elif mcp_type == "aws_diagram":
        return {
            "mcpServers": {
                "awslabs.aws-diagram-mcp-server": {
                    "command": "uvx",
                    "args": ["awslabs.aws-diagram-mcp-server"],
                    "env": {
                        "FASTMCP_LOG_LEVEL": "ERROR"
                    },
                }
            }
        }
    
    elif mcp_type == "aws_documentation":
        return {
            "mcpServers": {
                "awslabs.aws-documentation-mcp-server": {
                    "command": "uvx",
                    "args": ["awslabs.aws-documentation-mcp-server@latest"],
                    "env": {
                        "FASTMCP_LOG_LEVEL": "ERROR"
                    }
                }
            }
        }
    
    elif mcp_type == "aws_cost":
        return {
            "mcpServers": {
                "aws_cost": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_aws_cost.py"
                    ]
                }
            }
        }    
    elif mcp_type == "aws_cloudwatch":
        return {
            "mcpServers": {
                "aws_cloudwatch_log": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_aws_log.py"
                    ]
                }
            }
        }    
    
    elif mcp_type == "aws_storage":
        return {
            "mcpServers": {
                "aws_storage": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_aws_storage.py"
                    ]
                }
            }
        }    
        
    elif mcp_type == "arxiv":
        return {
            "mcpServers": {
                "arxiv-mcp-server": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@smithery/cli@latest",
                        "run",
                        "arxiv-mcp-server",
                        "--config",
                        "{\"storagePath\":\"/Users/ksdyb/Downloads/ArXiv\"}"
                    ]
                }
            }
        }
    
    elif mcp_type == "firecrawl":
        return {
            "mcpServers": {
                "firecrawl-mcp": {
                    "command": "npx",
                    "args": ["-y", "firecrawl-mcp"],
                    "env": {
                        "FIRECRAWL_API_KEY": chat.firecrawl_key
                    }
                }
            }
        }
    
    elif mcp_type == "aws_rag":
        return {
            "mcpServers": {
                "aws_storage": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_rag.py"
                    ]
                }
            }
        }    
    
    elif mcp_type == "code_interpreter":
        return {
            "mcpServers": {
                "aws_storage": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_coder.py"
                    ]
                }
            }
        }    
    
    elif mcp_type == "aws_cli":
        return {
            "mcpServers": {
                "aw-cli": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_aws_cli.py"
                    ]
                }
            }
        }    
    
    elif mcp_type == "tavily":
        return {
            "mcpServers": {
                "tavily-mcp": {
                    "command": "npx",
                    "args": ["-y", "tavily-mcp@0.1.4"],
                    "env": {
                        "TAVILY_API_KEY": chat.tavily_key
                    },
                }
            }
        }
    elif mcp_type == "wikipedia":
        return {
            "mcpServers": {
                "wikipedia": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_wikipedia.py"
                    ]
                }
            }
        }      
    elif mcp_type == "terminal":
        return {
            "mcpServers": {
                "iterm-mcp": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "iterm-mcp"
                    ]
                }
            }
        }
    
    elif mcp_type == "filesystem":
        return {
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "@modelcontextprotocol/server-filesystem",
                        "~/"
                    ]
                }
            }
        }
    
    elif mcp_type == "puppeteer":
        return {
            "mcpServers": {
                "puppeteer": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
                }
            }
        }
    
    elif mcp_type == "perplexity":
        return {
            "mcpServers": {
                "perplexity-mcp": {                    
                    "command": "uvx",
                    "args": [
                        "perplexity-mcp"
                    ],
                    "env": {
                        "PERPLEXITY_API_KEY": chat.perplexity_key,
                        "PERPLEXITY_MODEL": "sonar"
                    }
                }
            }
        }

    elif mcp_type == "text_editor":
        return {
            "mcpServers": {
                "textEditor": {
                    "command": "npx",
                    "args": ["-y", "mcp-server-text-editor"]
                }
            }
        }
    
    elif mcp_type == "context7":
        return {
            "mcpServers": {
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp@latest"]
                }
            }
        }
    
    elif mcp_type == "pubmed":
        return {
            "mcpServers": {
                "pubmed": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_pubmed.py"  
                    ]
                }
            }
        }
    
    elif mcp_type == "chembl":
        return {
            "mcpServers": {
                "chembl": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_chembl.py"
                    ]
                }
            }
        }
    
    elif mcp_type == "clinicaltrial":
        return {
            "mcpServers": {
                "clinicaltrial": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_clinicaltrial.py"
                    ]
                }
            }
        }
    
    elif mcp_type == "arxiv-manual":
        return {
            "mcpServers": {
                "arxiv-manager": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_arxiv.py"
                    ]
                }
            }
        }
    
    elif mcp_type == "tavily-manual":
        return {
            "mcpServers": {
                "arxiv-manager": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_tavily.py"
                    ]
                }
            }
        }
    elif mcp_type == "use_aws":
        return {
            "mcpServers": {
                "use_aws": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_use_aws.py"
                    ]
                }
            }
        }
    
    elif mcp_type == "aws_cloudwatch_logs":  # AWS Labs cloudwatch-logs MCP Server
        return {
            "mcpServers": {
                "awslabs.cloudwatch-logs-mcp-server": {
                    "command": "uvx",
                    "args": [
                        "awslabs.cloudwatch-logs-mcp-server@latest"
                    ],
                    "env": {
                        "AWS_REGION": aws_region,
                        "FASTMCP_LOG_LEVEL": "ERROR"
                    }
                }
            }
        }
    
    elif mcp_type == "aws_knowledge_base":  # AWS Labs cloudwatch-logs MCP Server
        return {
            "mcpServers": {
                "aws_knowledge_base": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_kb.py"
                    ],
                    "env": {
                        "KB_INCLUSION_TAG_KEY": "mcp-rag"
                    }
                }
            }
        }
    
    elif mcp_type == "opensearch":
        return {
            "mcpServers": {
                "opensearch-mcp-server": {
                    "command": "uvx",
                    "args": [
                        "opensearch-mcp-server-py"
                    ],
                    "env": {
                        "OPENSEARCH_URL": managed_opensearch_url,
                        "AWS_REGION":"us-west-2",
                        "OPENSEARCH_USERNAME": opensearch_username,
                        "OPENSEARCH_PASSWORD": opensearch_password
                    }
                }
            }
        }
    
    elif mcp_type == "사용자 설정":
        return mcp_user_config

def load_selected_config(mcp_selections: dict[str, bool]):
    #logger.info(f"mcp_selections: {mcp_selections}")
    loaded_config = {}

    selected_servers = [server for server, is_selected in mcp_selections.items() if is_selected]
    logger.info(f"selected_servers: {selected_servers}")

    for server in selected_servers:
        logger.info(f"server: {server}")

        if server == "image generation":
            config = load_config('image_generation')
        elif server == "aws diagram":
            config = load_config('aws_diagram')
        elif server == "aws document":
            config = load_config('aws_documentation')
        elif server == "aws cost":
            config = load_config('aws_cost')
        elif server == "ArXiv":
            config = load_config('arxiv')
        elif server == "aws cloudwatch":
            config = load_config('aws_cloudwatch')
        elif server == "aws storage":
            config = load_config('aws_storage')
        elif server == "knowledge base":
            config = load_config('aws_rag')
        elif server == "code interpreter":
            config = load_config('code_interpreter')
        elif server == "aws cli":
            config = load_config('aws_cli')
        elif server == "text editor":
            config = load_config('text_editor')
        else:
            config = load_config(server)
        logger.info(f"config: {config}")
        
        if config:
            loaded_config.update(config["mcpServers"])

    logger.info(f"loaded_config: {loaded_config}")
        
    return {
        "mcpServers": loaded_config
    }
