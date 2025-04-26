from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import (MCPToolset,
                                                   StdioServerParameters)
from google.genai import types

from .utils import print_event

load_dotenv("src/.env")


async def get_tools():
    """Gets tools from the File System MCP Server."""
    print("Connecting to MCP server...")
    server_params = StdioServerParameters(
        command="deno",
        args=[
            "run",
            "-N",
            "-R=node_modules",
            "-W=node_modules",
            "--node-modules-dir=auto",
            "jsr:@pydantic/mcp-run-python",
            "stdio",
        ],
    )

    tools, exit_stack = await MCPToolset.from_server(connection_params=server_params)
    print("Connected to MCP server.")
    return tools, exit_stack


async def get_agent():
    """Creates the root agent."""
    tools, exit_stack = await get_tools()
    for tool in tools:
        print(f"Tool: {tool.name}\nSchema: {tool.mcp_tool.inputSchema}")

    root_agent = Agent(
        model="gemini-2.0-flash",
        name="MathAgent",
        tools=tools,
        instruction="Answer math questions using the tools provided.",
    )

    return root_agent, exit_stack


async def main():
    try:
        session_service = InMemorySessionService()
        root_agent, exit_stack = await get_agent()

        sesseion = session_service.create_session(
            state={},
            app_name="MathAgent",
            user_id="user",
        )

        question = "How many days between 1st January 2023 and 1st June 2024?"
        content = types.Content(role="user", parts=[types.Part(text=question)])

        runner = Runner(
            app_name="MathAgent", agent=root_agent, session_service=session_service
        )

        print("Running agent...")
        events_async = runner.run_async(
            session_id=sesseion.id,
            user_id=sesseion.user_id,
            new_message=content,
        )

        async for event in events_async:
            await print_event(event)

    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
