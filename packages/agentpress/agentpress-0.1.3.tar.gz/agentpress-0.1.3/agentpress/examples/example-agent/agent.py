import asyncio
import json
from agentpress.thread_manager import ThreadManager
from tools.files_tool import FilesTool
from agentpress.state_manager import StateManager
from tools.terminal_tool import TerminalTool

async def run_agent(thread_id: str, max_iterations: int = 5):
    # Initialize managers and tools
    thread_manager = ThreadManager()
    state_manager = StateManager()
    
    thread_manager.add_tool(FilesTool)
    thread_manager.add_tool(TerminalTool)

    async def init():
        pass

    async def pre_iteration():
        # Update files state
        files_tool = FilesTool()
        await files_tool._init_workspace_state()

    async def after_iteration():
        # Ask the user for a custom message or use the default
        custom_message = input("Enter a message to send (or press Enter to use 'Continue!!!' as message): ")

        message_content = custom_message if custom_message else """ 
        Continue!!!
        """
        await thread_manager.add_message(thread_id, {
            "role": "user", 
            "content": message_content
        })
 
    async def finalizer():
        pass    

    await init()

    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        await pre_iteration()

        system_message = {
            "role": "system", 
            "content": """
You are a world-class web developer who can create, edit, and delete files, and execute terminal commands. You write clean, well-structured code. Keep iterating on existing files, continue working on this existing codebase - do not omit previous progress; instead, keep iterating.

RULES: 
- All current file contents are available to you in the <current_workspace_state> section
- Each file in the workspace state includes its full content
- Use str_replace for precise replacements in files
- NEVER include comments in any code you write - the code should be self-documenting
- Always maintain the full context of files when making changes
- When creating new files, write clean code without any comments or documentation

<available_tools>
[create_file(file_path, file_contents)] - Create new files
[delete_file(file_path)] - Delete existing files
[str_replace(file_path, old_str, new_str)] - Replace specific text in files
[execute_command(command)] - Execute terminal commands
</available_tools>

ALWAYS RESPOND WITH MULTIPLE SIMULTANEOUS ACTIONS:
<thoughts>
[Provide a concise overview of your planned changes and implementations]
</thoughts>

<actions>
[Include multiple tool calls]
</actions>

EDITING GUIDELINES:
1. Review the current file contents in the workspace state
2. Make targeted changes with str_replace
3. Write clean, self-documenting code without comments
4. Use create_file for new files and str_replace for modifications

Example workspace state for a file:
{
  "index.html": {
    "content": "<!DOCTYPE html>\\n<html>\\n<head>..."
  }
}

Think deeply and step by step.
            """
        }

        state = await state_manager.export_store()

        state_message = {
            "role": "user",
            "content": f"""
Current development environment workspace state:
            <current_workspace_state>
{json.dumps(state, indent=2)}
</current_workspace_state>
            """
        }

        model_name = "anthropic/claude-3-5-sonnet-latest"

        response = await thread_manager.run_thread(
                    thread_id=thread_id,
                    system_message=system_message,
                    model_name=model_name,
                    temperature=0.1,
                    max_tokens=4096,
                    tool_choice="auto",
                    additional_message=state_message,
                    execute_tools_async=True,
                    use_tools=True,
                    execute_model_tool_calls=True                    
                )
        
        print(response)

        # Call after_iteration without arguments
        await after_iteration()

    await finalizer()


if __name__ == "__main__":
    async def main():
        thread_manager = ThreadManager()
        thread_id = await thread_manager.create_thread()

        await thread_manager.add_message(
            thread_id, 
            {
                "role": "user", 
                "content": "Let's create a identical 1to1 Airbnb Clone using HTML, CSS, Javascript. Use images from pixabay, pexels, and co."
            }
        )      

        await run_agent(thread_id)
    
    asyncio.run(main())