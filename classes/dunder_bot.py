from utils.langchain import format_query_optimizer_prompt, format_response_prompt, generate_json_response, initialize_chat_model, retrieve_documents


def stream_response(prompt, chat_model):
    for chunk in chat_model.stream(prompt):
        yield chunk.content


class DunderBot:
    def __init__(self, llm="openai", collection="openai_embeddings"):
        self.llm = llm
        self.collection = collection
        self.chat_model = initialize_chat_model(llm=llm)

    def answer_me_this(self, user_query, number_of_results=10):
        context_documents = retrieve_documents(
            user_query=user_query, number_of_results=number_of_results)
        prompt = format_response_prompt(user_query=user_query,
                                        context_documents=context_documents)
        return stream_response(prompt=prompt, chat_model=self.chat_model)

    def answer_this_with_expertise(self, user_query):
        # step 1: User the expert to create a optimized query
        print("answer_this_with_expertise - Step 1")
        query_optimizer_prompt = format_query_optimizer_prompt(user_query=user_query)
        optmized_query = generate_json_response(
            query_optimizer_prompt, self.chat_model)
        # validate the query
        required_keys = ["user_query"]

        for key in required_keys:
            if key not in optmized_query:
                raise ValueError(
                    f"Optimized query missing required field: {key}")

        # step 2: retrive documents based on query
        print("answer_this_with_expertise - Step 2")
        context_documents = retrieve_documents(
            user_query=optmized_query["user_query"], filter=optmized_query["filter"], number_of_results=optmized_query["number_of_results"])

        # step 3: format prompt using the retrived documents
        print("answer_this_with_expertise - Step 3")
        prompt = format_response_prompt(user_query=user_query,
                                        context_documents=context_documents)

        # step 4: Augment the reponse and send it back
        print("answer_this_with_expertise - Step 4")
        return stream_response(prompt=prompt, chat_model=self.chat_model)
