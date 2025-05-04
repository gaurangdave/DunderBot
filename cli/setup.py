from utils.common import load_state, is_environment_ready, is_data_present, save_state
from utils.chromadb import drop_collection, create_collection
from utils.config import get_default_collection
from utils.data import convert_data_to_documents, convert_data_to_documents_by_lines
from utils.langchain import embed_and_store_documents
from halo import Halo


def run_setup():
    # step 0: check if required environment variables are present
    spinner = Halo(text='Checking environment variables...', spinner='dots')
    spinner.start()
    if (not is_environment_ready()):
        spinner.fail("Environment variables missing - Plese refer to docs")
        return
    spinner.succeed(text="Environment OK")

    # step 1: check if required data files are present
    spinner = Halo(text='Checking data files...', spinner='dots')
    spinner.start()
    if (not is_data_present()):
        spinner.fail("Missing data files...")
    spinner.succeed(text="Data files OK")

    # step 2: reset & drop the database
    spinner = Halo(
        text='Dropping existing ChromaDB collection...', spinner='dots')
    spinner.start()
    default_collection = get_default_collection()
    drop_collection(default_collection)
    spinner.succeed(text="Database dropped")

    # step 3: create new collection
    spinner = Halo(text='Creating new ChromaDB collection...', spinner='dots')
    spinner.start()
    create_collection(default_collection)
    spinner.succeed("Collection created")

    # step 4: prepare dataset
    spinner = Halo(text='Converting data to documents...', spinner='dots')
    spinner.start()
    documents = convert_data_to_documents_by_lines()
    spinner.succeed(f"Prepared {len(documents)} documents")

    # step 5: Upload the dataset to chromadb
    spinner = Halo(text='Embedding and storing documents...', spinner='dots')
    spinner.start()
    vector_db = embed_and_store_documents(documents, llm="openai")
    spinner.succeed("Documents stored successfully")

    # Step 6: Update the state
    spinner = Halo(text="Updating setup state...", spinner="dots")
    spinner.start()
    save_state("is_setup_complete", True)
    spinner.succeed("Setup complete")

    print("\n🎉🎉🎉 DunderBot setup complete and ready to roll! 🎉🎉🎉")


def reset_app():
    # Step 1: Just run the setup app, it will reset the database
    user_input = input(
        "\n🧨 WARNING: This will completely reset DunderBot.\n"
        "All memories, quotes, and embeddings will be wiped and rebuilt.\n"
        "It's like sending DunderBot to Scranton Training Camp all over again.\n"
        "Do you want to continue? (y/n): "
    ).strip()
    if user_input.lower() in {"y", "yes"}:
        run_setup()
        return
    print("\n🛑 Reset cancelled. DunderBot’s wisdom is safe for now.\n")


def initialize():
    # Step 1: Load current state
    current_state, _ = load_state()

    # Step 2: Check if the app is already initialized
    is_setup_complete = current_state["is_setup_complete"]
    if is_setup_complete:
        print("\n🟢 Looks like setup is already complete — nothing to do here!\n💡 Tip: If you want to start fresh, try running the `reset` command.")
    else:
        run_setup()
