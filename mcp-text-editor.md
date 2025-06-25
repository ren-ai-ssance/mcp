# MCP Text Editor

[MCP Server Text Editor](https://github.com/bhouston/mcp-server-text-editor)를 이용해 text editor를 이용할 수 있습니다. 

이때의 MCP config는 아래와 같습니다.

```python
{
  "mcpServers": {
    "textEditor": {
      "command": "npx",
      "args": ["-y", "mcp-server-text-editor"]
    }
  }
}
```

상세한 내용은 [Claude Text Editor MCP Server](https://www.npmjs.com/package/mcp-server-text-editor)을 참조합니다.
