import os
import sys
from datetime import datetime
import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, crawl_logs, file_attachments, assets_link):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `CodingAgent` is initializing setup with provided instructions and context")

        prompt = f"""You are an expert software engineer. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure the SEARCH section exactly matches existing code, including whitespace and comments.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Development plan: {instructions['Implementation_plan']} and original raw request, use if Implementation_plan missing some pieces: {instructions['original_prompt']}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this entire process, use it if appropriate: {crawl_logs}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        all_attachment_file_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            self.conversation_history.append({"role": "user", "content": f"User has attached these files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the original Development plan, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})



    async def get_coding_request(self, file, techStack):
        """
        Get coding response for the given instruction and context from Azure OpenAI.

        Args:
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        is_svg = file_name.lower().endswith('.svg')

        # Build the user prompt
        user_prompt = self._build_user_prompt(file_name, techStack, is_svg)
        self._add_to_conversation(user_prompt)

        try:
            return await self._get_complete_response()
        except Exception as e:
            logger.error(f" The `CodingAgent` encountered an error while getting coding request")
            logger.error(f" {e}")
            raise

    def _build_user_prompt(self, file_name, techStack, is_svg):
        """Build the user prompt based on file type and tech stack."""
        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."
        
        prompt = [
            f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'}, implement the following task with utmost efficiency and precision:",
            f"Update comprehensive code for this file that matches with original instruction: {file_name}:"
        ]

        if is_svg:
            prompt.extend([
                "Create a visually appealing design with elegant UI.",
                "Balance aesthetics and functionality, ensuring each element enhances the user experience.",
                "Prioritize smooth performance and sophistication in all visual aspects."
            ])
        else:
            prompt.extend([
                f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}",
                "IF UI-related tasks:",
                "- Ensure perfect alignment and consistent padding for a clean, good look.",
                "- Implement a visually striking design with smooth, intuitive interactions.",
                "- Create a top-notch, bug-free design as an expert for the user.",
                "- Enhance user experience while maintaining optimal performance.",
                "- Ensure responsiveness and cross-device compatibility.",
                "For LOGIC CODE TYPES:",
                "- Respect and use existing conventions, libraries, etc. that are already present in the code base.",
                "- Always use best practices when coding, including proper error handling and input validation.",
                "- Modify only the specific parts mentioned in the instructions; leave all other code unchanged.",
                "- Do not alter the overall structure or logic flow of the existing code if not explicitly requested.",
                "- Ensure compatibility with the specified tech stack and follow best practices for that stack.",
                "- Implement robust error handling and logging for easier debugging.",
                "- Don't change the names of existing functions or classes, as they may be referenced from other code like unit tests, etc."
            ])

        if not is_svg:
            prompt.append(lazy_prompt)
            
        prompt.append("NOTICE: Your response must ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.")
        
        return "\n".join(prompt)

    def _add_to_conversation(self, user_prompt):
        """Add the prompt to conversation history with appropriate handling."""
        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})
        self.conversation_history.append({"role": "user", "content": user_prompt})

    async def _get_complete_response(self, max_attempts=3):
        """Get complete response with continuation handling if needed."""
        content = ""
        attempts = 0
        
        while attempts < max_attempts:
            response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            new_content = response.choices[0].message.content
            content += new_content
            
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and "> REPLACE" in lines[-1]:
                if attempts > 0:
                    # Clean up intermediate conversation entries
                    self.conversation_history = self.conversation_history[:-2 * attempts]
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
                
            # Response was cut off, prepare for continuation
            self.conversation_history.append({"role": "assistant", "content": content})
            self.conversation_history.append({
                "role": "user", 
                "content": "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
            })
            
            attempts += 1
            
        # If we get here, we've hit max attempts without a complete response
        logger.error("  The `CodingAgent` failed to get a complete response after maximum attempts")
        return content


    async def get_coding_requests(self, file, techStack):
        """
        Get coding responses for a file from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The coding task prompt.

        Returns:
            str: The code response or error reason.
        """
        return await self.get_coding_request(file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### The `CodingAgent` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### The `CodingAgent` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None
