import uuid

import typer

from opencopilot.scripts import chat as chat_script

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command(help="Print info")
def info():
    print("OpenCopilot CLI. Currently just a convenience layer for chatting with the copilot.")


@app.command(help="Chat with the Copilot. Example: chat 'Hello, who are you?'")
def chat(message: str):
    print("Message:", message)
    conversation_id = uuid.uuid4()
    while message:
        print("Response: ", end="", flush=True)
        chat_script.conversation_stream(
            base_url="http://0.0.0.0:3000",
            conversation_id=conversation_id,
            message=message,
            stream=True)
        print()
        message = input("Message: ")


if __name__ == "__main__":
    app()
