import os
from typing import Any, Optional

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import (MCPToolset,
                                                   StdioServerParameters)
from google.genai import types

load_dotenv("src/.env")
print("ok")
from google.adk.models.lite_llm import LiteLlm

INSTRUCTION = """You are a math agent.
When given any mathematical expression, generate a Python code snippet that evaluates the expression and assigns the result to a variable named 'result'.
Always end your code with 'print(result)' to display the output.
Use the 'code_execution_tool' to execute the code and print the result.
If code execution fails, return a clear error message along with a helpful suggestion for debugging."""


class MCPClient:
    def __init__(self):
        self.exit_stack: Optional[Any] = None
        self.server_params: Optional[Any] = None
        self.tools: Optional[Any] = None

    async def connect_to_server(self, path: str):
        """Connect to the mcp server

        Args:
            path: Path to the server script.
        """
        self.server_params = StdioServerParameters(command="python", args=[path])

        print("Connected to the mcp server")

    async def get_mcp_tools(self):
        """Get tools from the mcp server"""
        self.tools, self.exit_stack = await MCPToolset.from_server(
            connection_params=self.server_params
        )

        print(f"Fetched {len(self.tools)} tools from MCP server.")

    async def get_agent(self):
        """Main proccess"""
        print("Gettt")
        root_agent = Agent(
            name="math_agent",
            model=LiteLlm(model="azure/gpt-4o-mini"),
            tools=self.tools,
            instruction=INSTRUCTION,
            description="Agent to answer questions about mathematics.",
        )

        return root_agent

    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main():
    print("Start")
    client = MCPClient()
    path = "src/server.py"
    try:
        if os.path.exists(path=path):
            print("Init...")
            await client.connect_to_server(path)
            print("Init success")
            session_service = InMemorySessionService()

            session = session_service.create_session(
                state={}, app_name="math_agent", user_id="user_1"
            )

            query = """Evaluate: ∫ 3ax/(b2 +c2x2) dx"""
            print(f"User Query: '{query}'")
            content = types.Content(role="user", parts=[types.Part(text=query)])

            await client.get_mcp_tools()
            root_agent = await client.get_agent()

            runner = Runner(
                app_name="math_agent",
                agent=root_agent,
                session_service=session_service,
            )
            print("Running agent...")
            events_async = runner.run_async(
                session_id=session.id, user_id=session.user_id, new_message=content
            )

            async for event in events_async:
                print(f"Event received: {event.content.parts[0].text}")

        else:
            print("Path not found!")
    finally:
        print("Shut down")
        await client.cleanup()


if __name__ == "__main__":
    import asyncio
    import json

    asyncio.run(main())
