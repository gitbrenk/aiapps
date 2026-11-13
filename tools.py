from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from anthropic import beta_tool

load_dotenv()
client = anthropic.Anthropic()

@beta_tool
def get_current_time() -> str:
    """Get the current local date and time."""
    print("  [tool] get_current_time called")
    return datetime.now().strftime("%A %d %B %Y, %H:%M")

@beta_tool
def list_files() -> str:
    """List the files in the current project folder."""
    print("  [tool] list_files called")
    return "\n".join(p.name for p in Path(".").iterdir() if p.name != ".env")

question = input("Ask something: ")

runner = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=16000,
    tools=[get_current_time, list_files],
    messages=[{"role": "user", "content": question}],
)
final = runner.until_done()  # Claude calls tools as many times as it needs
print("\nClaude:", "".join(b.text for b in final.content if b.type == "text"))