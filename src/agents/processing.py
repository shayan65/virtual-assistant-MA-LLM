import json

########################################
# Chat Properties
########################################
def craft_agent_chat_context(context: str) -> dict:
    """
    Craft the context for the agent to use in chat endpoints.

    Parameters:
    - context (str): The context information for the agent.

    Returns:
    - dict: A dictionary representing the context with its role and content.
    """
    return {
        "role": "system",
        "content": context
    }

def craft_agent_chat_first_message(content: str) -> dict:
    """
    Craft the first message for the agent to use in chat endpoints.

    Parameters:
    - content (str): The content of the first message from the agent.

    Returns:
    - dict: A dictionary representing the first message with its role and content.
    """
    return {
        "role": "assistant",
        "content": content
    }

def craft_agent_chat_instructions(instructions: str, response_shape: dict) -> dict:
    """
    Craft the instructions for the agent to use in chat endpoints.

    Parameters:
    - instructions (str): The instructions for the agent.
    - response_shape (dict): The expected JSON shape of the response.

    Returns:
    - dict: A dictionary representing the instructions with its role and content.
    """
    formatted_response_shape = json.dumps(response_shape, ensure_ascii=False, indent=2)
    instructions_content = f"{instructions}\n\nFollow a RFC8259 compliant JSON with a shape of:\n{formatted_response_shape} format without deviation."
    
    return {
        "role": "user",
        "content": instructions_content
    }
