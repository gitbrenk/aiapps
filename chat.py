from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SYSTEM = "You are a friendly Python tutor. Keep answers short and practical."
history = []  # the whole conversation so far

while True:
    user_text = input("\nYou: ")
    if user_text.strip().lower() == "quit":
        break
    history.append({"role": "user", "content": user_text})

    print("Claude: ", end="")
    with client.messages.stream(
        model="claude-opus-5-5",
        max_tokens=4096,
        system=SYSTEM,
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # show words as they arrive
        reply = stream.get_final_message()

    history.append({"role": "assistant", "content": reply.content})