from utils.langchain import format_prompt, generate_response, initialize_chat_model, retrieve_documents


class DunderBot:
    def __init__(self, llm="openai", collection="openai_embeddings"):
        self.llm = llm
        self.collection = collection
        self.chat_model = initialize_chat_model(llm=llm)

    def answer_me_this(self, user_query, number_of_results=10):
        context_documents = retrieve_documents(
            user_query=user_query, number_of_results=number_of_results)
        prompt = format_prompt(user_query=user_query,
                               context_documents=context_documents)
        answer = generate_response(prompt=prompt, chat_model=self.chat_model)
        return answer
