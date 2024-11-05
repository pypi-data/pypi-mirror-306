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

        # Initialize conversation with system prompt and initial context
        self._initialize_base_conversation(instructions, context)

        # Process context files in chunks
        if context_files:
            self._process_context_files(context_files)

        # Add crawl logs if present
        if crawl_logs:
            self._add_crawl_logs_in_chunks(crawl_logs)

        # Process file attachments
        self._process_attachments(file_attachments)

        # Process image assets
        self._process_images(file_attachments, assets_link)

    def _initialize_base_conversation(self, instructions, context):
        """Initialize the base conversation with system prompt and initial context."""
        prompt = self._get_system_prompt()
        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Development plan: {instructions['Implementation_plan']} and original raw request, use if Implementation_plan missing some pieces: {instructions['original_prompt']}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

    def _get_system_prompt(self):
        """Return the system prompt for the conversation."""
        return """You are an expert software engineer. Follow these guidelines strictly when responding to instructions:

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

    def _process_context_files(self, context_files, chunk_size=5):
        """Process context files in chunks to avoid too long messages."""
        for i in range(0, len(context_files), chunk_size):
            chunk = context_files[i:i + chunk_size]
            all_file_contents = ""
            
            for file_path in chunk:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

    def _add_crawl_logs_in_chunks(self, crawl_logs, chunk_size=1000):
        """Add crawl logs to conversation history in manageable chunks."""
        if isinstance(crawl_logs, str):
            # Split crawl logs into chunks
            for i in range(0, len(crawl_logs), chunk_size):
                chunk = crawl_logs[i:i + chunk_size]
                self.conversation_history.append({"role": "user", "content": f"This is supported data chunk {i//chunk_size + 1} for this process: {chunk}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
        else:
            # Handle case where crawl_logs might be a different data structure
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this process: {str(crawl_logs)[:chunk_size]}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

    def _process_attachments(self, file_attachments, chunk_size=1000):
        """Process non-image file attachments in chunks."""
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    # Split file content into chunks if it's too long
                    for i in range(0, len(file_content), chunk_size):
                        chunk = file_content[i:i + chunk_size]
                        self.conversation_history.append({
                            "role": "user", 
                            "content": f"File: {os.path.relpath(file_path)} (part {i//chunk_size + 1}):\n{chunk}"
                        })
                        self.conversation_history.append({"role": "assistant", "content": "Understood."})

    def _process_images(self, file_attachments, assets_link, batch_size=5):
        """Process image files and asset links in batches."""
        # Process image files in batches
        image_files = process_image_files(file_attachments)
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i:i + batch_size]
            message_content = [{"type": "text", "text": f"Processing image batch {i//batch_size + 1}:"}]
            
            for base64_image in batch:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"{base64_image}"
                    }
                })

            self.conversation_history.append({"role": "user", "content": message_content})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        # Process asset links in batches
        if assets_link:
            for i in range(0, len(assets_link), batch_size):
                batch = assets_link[i:i + batch_size]
                message_content = [{"type": "text", "text": f"Processing asset links batch {i//batch_size + 1}:"}]
                
                for image_url in batch:
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
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The specific task or instruction for coding.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        is_svg = file_name.lower().endswith('.svg')

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        user_prompt = f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'}, implement the following task with utmost efficiency and precision:\n"
        user_prompt += f"Update comprehensive code for this file that matches with original instruction: {file_name}:\n"

        if is_svg:
            #user_prompt += f"Image implementation: {prompt}\n"
            user_prompt += (
                "Create a visually appealing design with elegant UI.\n"
                "Balance aesthetics and functionality, ensuring each element enhances the user experience.\n"
                "Prioritize smooth performance and sophistication in all visual aspects.\n"
            )
        else:
            #user_prompt += f"Main Task: {prompt}\n"
            user_prompt += (
                f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}"
                "IF UI-related tasks:\n"
                "- Ensure perfect alignment and consistent padding for a clean, good look.\n"
                "- Implement a visually striking design with smooth, intuitive interactions.\n"
                "- Create a top-notch, bug-free design as an expert for the user.\n"
                "- Enhance user experience while maintaining optimal performance.\n"
                "- Ensure responsiveness and cross-device compatibility.\n"
                "For LOGIC CODE TYPES:\n"
                "- Respect and use existing conventions, libraries, etc. that are already present in the code base.\n"
                "- Always use best practices when coding, including proper error handling and input validation.\n"
                "- Modify only the specific parts mentioned in the instructions; leave all other code unchanged.\n"
                "- Do not alter the overall structure or logic flow of the existing code if not explicitly requested.\n"
                "- Ensure compatibility with the specified tech stack and follow best practices for that stack.\n"
                "- Implement robust error handling and logging for easier debugging.\n"
                "- Don't change the names of existing functions or classes, as they may be referenced from other code like unit tests, etc."
            )

        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
        user_prompt += "NOTICE: Your response must ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            content = response.choices[0].message.content
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and "> REPLACE" in lines[-1]:
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                self.conversation_history.append({"role": "assistant", "content": content})
                # The response was cut off, prompt AI to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                continuation_response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                continuation_content = continuation_response.choices[0].message.content
                continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]

                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                    # Combine the incomplete and continuation responses
                    complete_content = content + continuation_content
                    self.conversation_history = self.conversation_history[:-2]
                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                    return complete_content
                else:
                    content = content + continuation_content
                    self.conversation_history.append({"role": "assistant", "content": content})
                    # The response was cut off, prompt AI to continue
                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                    continuation_response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                    continuation_content1 = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content1.splitlines() if line.strip()]

                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                        # Combine the incomplete and continuation responses
                        complete_content = content + continuation_content1
                        self.conversation_history = self.conversation_history[:-4]
                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                        return complete_content
                    else:
                        content = content + continuation_content1
                        self.conversation_history.append({"role": "assistant", "content": content})
                        # The response was cut off, prompt AI to continue
                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                        continuation_response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                        continuation_content2 = continuation_response.choices[0].message.content
                        continuation_lines = [line.strip() for line in continuation_content2.splitlines() if line.strip()]

                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                            # Combine the incomplete and continuation responses
                            complete_content = content + continuation_content2
                            return complete_content
                        else:
                            complete_content = content + continuation_content2
                            self.conversation_history = self.conversation_history[:-6]
                            self.conversation_history.append({"role": "assistant", "content": complete_content})
                            logger.error(f"  The `CodingAgent` encountered an error while getting coding request")
                            return complete_content

        except Exception as e:
            logger.error(f" The `CodingAgent` encountered an error while getting coding request")
            logger.error(f" {e}")
            raise


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
