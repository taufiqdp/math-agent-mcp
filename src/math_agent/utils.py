async def print_event(event):
    """Prints the details of a received event in a structured format."""
    print("\n--- Event Received ---")
    print(f"Timestamp: {event.timestamp}")
    print(f"Author: {event.author}")
    print(f"Invocation ID: {event.invocation_id}")

    if event.content and event.content.parts:
        print("Content Parts:")
        for part in event.content.parts:
            if part.text:
                print(f"  Text: {part.text.strip()}")
            elif part.function_call:
                print("  Function Call:")
                print(f"    Name: {part.function_call.name}")
                print(f"    Args: {part.function_call.args}")
            elif part.function_response:
                print("  Function Response:")
                print(f"    Name: {part.function_response.name}")
                print(f"    Response: {part.function_response.response}")
            elif part.thought:
                print(f"  Thought: {part.thought.strip()}")

    if event.turn_complete:
        print("Turn Complete: True")

    if event.error_code:
        print(f"Error Code: {event.error_code}")
        print(f"Error Message: {event.error_message}")

    if event.actions and (
        event.actions.state_delta
        or event.actions.artifact_delta
        or event.actions.transfer_to_agent
        or event.actions.escalate
        or event.actions.requested_auth_configs
    ):
        print("Actions:")
        if event.actions.state_delta:
            print(f"  State Delta: {event.actions.state_delta}")
        if event.actions.artifact_delta:
            print(f"  Artifact Delta: {event.actions.artifact_delta}")
        if event.actions.transfer_to_agent:
            print(f"  Transfer to Agent: {event.actions.transfer_to_agent}")
        if event.actions.escalate:
            print(f"  Escalate: {event.actions.escalate}")
        if event.actions.requested_auth_configs:
            print(f"  Requested Auth Configs: {event.actions.requested_auth_configs}")

    if event.long_running_tool_ids:
        print(f"Long Running Tool IDs: {event.long_running_tool_ids}")

    print("---------------------\n")
