import docker
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Math Agent")


@mcp.tool()
def execute_python_code(code: str) -> dict:
    """Execute python code and return the result.

    Args:
        code (str): The code to execute.
        eg. '''
        import math

        def calculate_square_root(number):
            return math.sqrt(number)

        resutl = calculate_square_root(16)
        print(result)
        '''

    Returns:
        Result
    """
    try:
        print("ok from server")
        client = docker.from_env()

        container = client.containers.run(
            image="python-sandbox:latest",
            command=["python", "-c", code],
            remove=True,
            stdout=True,
            stderr=True,
            mem_limit="128m",
        )

        result = container.decode().strip()

        return dict(status="success", msg=result)
    except Exception as e:
        return dict(status="error", msg=str(e))


if __name__ == "__main__":
    mcp.run(transport="stdio")
