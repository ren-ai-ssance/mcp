def load_config(mcp_type):
    if mcp_type == "default":
        return {
            "mcpServers": {
                "search": {
                    "command": "python",
                    "args": [
                        "application/mcp-server.py"
                    ]
                },
                "playwright": {
                    "command": "npx",
                    "args": [
                        "@playwright/mcp@latest"
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
                    "{\"vaultPath\":\"/Users/ksdyb/Library/Mobile Documents/iCloud~md~obsidian/Documents/memo\"}"
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
                "imageGeneration": {
                    "command": "python",
                    "args": [
                        "application/mcp_server_aws_cost.py"
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