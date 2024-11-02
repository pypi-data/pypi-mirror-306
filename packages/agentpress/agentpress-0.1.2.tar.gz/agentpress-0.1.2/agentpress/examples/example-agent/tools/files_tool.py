import os
import asyncio
from datetime import datetime
from agentpress.tool import Tool, ToolResult, tool_schema
from agentpress.state_manager import StateManager

class FilesTool(Tool):
    # Excluded files, directories, and extensions
    EXCLUDED_FILES = {
        ".DS_Store",
        ".gitignore",
        "package-lock.json",
        "postcss.config.js",
        "postcss.config.mjs",
        "playwright.config.js",
        "jsconfig.json",
        "components.json",
        "tsconfig.tsbuildinfo",
        "next-env.d.ts",
        "tsconfig.json",
        "firebase-service-account.json",
        "Dockerfile"
    }

    EXCLUDED_DIRS = {
        "src/components/ui",
        "cypress",
        "node_modules",
        "migrations",
        ".next",
        "playwright-report",
        "test-results",
        "dist",
        "build",
        "coverage",
        "terminal_logs",
        ".git"
    }

    EXCLUDED_EXT = {
        ".ico",
        ".svg",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".db",
        ".sql"
    }

    def __init__(self):
        super().__init__()
        self.workspace = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'workspace')
        os.makedirs(self.workspace, exist_ok=True)
        self.state_manager = StateManager("state.json")
        asyncio.create_task(self._init_workspace_state())

    def _should_exclude_file(self, rel_path: str) -> bool:
        """Check if a file should be excluded based on path, name, or extension"""
        # Check filename
        filename = os.path.basename(rel_path)
        if filename in self.EXCLUDED_FILES:
            return True

        # Check directory
        dir_path = os.path.dirname(rel_path)
        if any(excluded in dir_path for excluded in self.EXCLUDED_DIRS):
            return True

        # Check extension
        _, ext = os.path.splitext(filename)
        if ext.lower() in self.EXCLUDED_EXT:
            return True

        return False

    async def _init_workspace_state(self):
        """Initialize or update the workspace state in JSON"""
        files_state = {}
        
        # Walk through workspace and record all files
        for root, _, files in os.walk(self.workspace):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.workspace)

                # Skip excluded files
                if self._should_exclude_file(rel_path):
                    continue

                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    files_state[rel_path] = content
                except Exception as e:
                    print(f"Error reading file {rel_path}: {e}")
                except UnicodeDecodeError:
                    print(f"Skipping binary file: {rel_path}")

        await self.state_manager.set("files", files_state)

    async def _update_workspace_state(self):
        """Update the workspace state after any file operation"""
        await self._init_workspace_state()

    @tool_schema({
        "name": "create_file",
        "description": "Create a new file in the workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The relative path of the file to create"},
                "content": {"type": "string", "description": "The content to write to the file"}
            },
            "required": ["file_path", "content"]
        }
    })
    async def create_file(self, file_path: str, content: str) -> ToolResult:
        try:
            full_path = os.path.join(self.workspace, file_path)
            if os.path.exists(full_path):
                return self.fail_response(f"File '{file_path}' already exists. Use update_file to modify existing files.")
            
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            
            await self._update_workspace_state()
            return self.success_response(f"File '{file_path}' created successfully.")
        except Exception as e:
            return self.fail_response(f"Error creating file: {str(e)}")

    @tool_schema({
        "name": "read_file",
        "description": "Read the contents of a file in the workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The relative path of the file to read"}
            },
            "required": ["file_path"]
        }
    })
    async def read_file(self, file_path: str) -> ToolResult:
        try:
            workspace_state = await self.state_manager.get("workspace")
            if file_path in workspace_state["files"]:
                return self.success_response({
                    "file_path": file_path,
                    "content": workspace_state["files"][file_path]["content"]
                })
            return self.fail_response(f"File '{file_path}' not found in workspace state.")
        except Exception as e:
            return self.fail_response(f"Error reading file: {str(e)}")

    @tool_schema({
        "name": "update_file",
        "description": "Update the contents of a file in the workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The relative path of the file to update"},
                "content": {"type": "string", "description": "The new content to write to the file"}
            },
            "required": ["file_path", "content"]
        }
    })
    async def update_file(self, file_path: str, content: str) -> ToolResult:
        try:
            full_path = os.path.join(self.workspace, file_path)
            with open(full_path, 'w') as f:
                f.write(content)
            
            await self._update_workspace_state()
            return self.success_response(f"File '{file_path}' updated successfully.")
        except Exception as e:
            return self.fail_response(f"Error updating file: {str(e)}")

    @tool_schema({
        "name": "delete_file",
        "description": "Delete a file from the workspace",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The relative path of the file to delete"}
            },
            "required": ["file_path"]
        }
    })
    async def delete_file(self, file_path: str) -> ToolResult:
        try:
            full_path = os.path.join(self.workspace, file_path)
            os.remove(full_path)
            
            await self._update_workspace_state()
            return self.success_response(f"File '{file_path}' deleted successfully.")
        except Exception as e:
            return self.fail_response(f"Error deleting file: {str(e)}")


if __name__ == "__main__":
    async def test_files_tool():
        files_tool = FilesTool()
        test_file_path = "test_file.txt"
        test_content = "This is a test file."
        updated_content = "This is an updated test file."

        print(f"Using workspace directory: {files_tool.workspace}")

        # Test create_file
        create_result = await files_tool.create_file(test_file_path, test_content)
        print("Create file result:", create_result)

        # Test read_file
        read_result = await files_tool.read_file(test_file_path)
        print("Read file result:", read_result)

        # Test update_file
        update_result = await files_tool.update_file(test_file_path, updated_content)
        print("Update file result:", update_result)

        # Test read_file after update
        read_updated_result = await files_tool.read_file(test_file_path)
        print("Read updated file result:", read_updated_result)

        # Test delete_file
        delete_result = await files_tool.delete_file(test_file_path)
        print("Delete file result:", delete_result)

        # Test read_file after delete (should fail)
        read_deleted_result = await files_tool.read_file(test_file_path)
        print("Read deleted file result:", read_deleted_result)

    asyncio.run(test_files_tool())