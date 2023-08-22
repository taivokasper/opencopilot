import os
from dotenv import load_dotenv

from opencopilot import OpenCopilot

load_dotenv()

copilot = OpenCopilot(
    prompt_file="prompts/prompt_template.txt",
    copilot_name="rpm",
    auth_type=None,
    helicone_api_key=os.getenv("HELICONE_API_KEY")
)
copilot.add_local_files_dir("data")

copilot()