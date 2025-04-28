import pyfiglet

from classes.dunder_bot import DunderBot


def run_bot():
    dunder_bot = DunderBot()
    f = pyfiglet.figlet_format("Dunder Bot", font="slant")
    print(f)
    print("🤖 DunderBot is here! Type your question below. Type 'exit' or 'quit' to leave.\n")
    while True:
        try:
            user_input = input("🟢 You: ").strip()

            # Exit condition
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Goodbye from DunderBot!")
                break

            elif user_input.lower() == "clear":
                import os
                os.system("cls" if os.name == "nt" else "clear")
                continue

            elif user_input == "":
                continue  # Ignore blank inputs

            # Process the query and stream the response
            print("\n🤖 DunderBot:")
            for chunk in dunder_bot.answer_me_this(user_query=user_input, number_of_results=10):
                print(chunk, end="", flush=True)
            print("\n")

        except KeyboardInterrupt:
            print("\n🛑 Ctrl+C detected. Exiting DunderBot.")
            break
        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")