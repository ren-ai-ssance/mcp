from mcp.server.fastmcp import FastMCP 

mcp =FastMCP("Math") 

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

if __name__ =="__main__":
    print(f"###### main ######")
    mcp.run(transport="stdio")