import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai
from kaggle.api.kaggle_api_extended import KaggleApi


def tavilysearch(text,Boole):
    if Boole==True:
        tavily_client = TavilyClient(api_key="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")
        prompt=f"what is {text} company's key offerings and strategic focus areas?"

        # Step 2. Executing a simple search query
        response = tavily_client.search(prompt,max_tokens=100, search_depth="advanced")

        # Step 3. That's it! You've done a Tavily Search!
        g=""
        for i in range(len(response['results'])):
            g+=response['results'][i]['content']
        return g
    else:
        tavily_client = TavilyClient(api_key="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")
        prompt=f"Can you provide an overview of recent trends, innovations, and key challenges in the {text} industry?"

        # Step 2. Executing a simple search query
        response = tavily_client.search(prompt,max_tokens=100, search_depth="advanced")

        # Step 3. That's it! You've done a Tavily Search!
        g=""
        for i in range(len(response['results'])):
            g+=response['results'][i]['content']
        return g

def geminillm(prompt):
    
    genai.configure(api_key="AIzaSyA96f_-FzE6O5ad1c7L6Cs2rXYNYAXltEk")
    generation_config={"temperature": 1.0, "top_p":1, "top_k":1, "max_output_tokens":2048}
    model=genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config, system_instruction="Generate a response listing three specific use cases on how integrating AI/ML into a company can enhance customer satisfaction. Ensure each use case: Starts with a clear subheading designed to facilitate dataset searches on platforms like Kaggle, Hugging Face, or GitHub. Generate use case subheadings that incorporate relevant keywords beyond the example terms like customer satisfaction, sentiment analysis, recommendation engine, or predictive customer service. Describes the use case and its benefits in terms of customer satisfaction. Includes a real-world example (if applicable) of a company that successfully implemented this use case.")
    gen_res=model.generate_content([prompt])

    return gen_res.text

def text_for_dataset(text):
    genai.configure(api_key="AIzaSyA96f_-FzE6O5ad1c7L6Cs2rXYNYAXltEk")
    generation_config={"temperature": 1.0, "top_p":1, "top_k":1, "max_output_tokens":2048}
    model2=genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config, system_instruction="""Analyze each use case provided and recommend relevant dataset names for each use case for searching, based solely on the use case's key requirements. Respond with just the names of the datasets without additional explanations or descriptions. The response format should be:
                                                                                                                1.[Dataset Name]
                                                                                                                2.[Dataset Name]
                                                                                                                3.[Dataset Name]"""
                                                                                                                )
    gen_res=model2.generate_content([text])
    return gen_res.text

def dataset_links(text):
    k=text.split("\n")
    k.remove("")
    for i in range(len(k)):
        k[i]=k[i].split(". ")[1]
    api = KaggleApi()
    api.authenticate()  # Authenticate the API
    result = []

    # Fetch datasets using the Kaggle API
    for i in k:
        datasets = api.dataset_list(search=i, sort_by='hottest')
        for dataset in datasets[:2]:
            name = dataset.ref  # Reference to the dataset
            title = dataset.title  # Title of the dataset
            url = f"https://www.kaggle.com/datasets/{name}"  # URL to access the dataset
            result.append((title, url))
    return result

def determine(text):
    fields = [
    "technology",
    "healthcare",
    "finance",
    "e-commerce",
    "education",
    "automotive",
    "entertainment",
    "travel and hospitality",
    "real estate",
    "agriculture",
    "retail",
    "human resources",
    "supply chain","logistics",
    "energy",
    "telecommunications",
    "media","publishing",
    "environmental services",
    "social media",
    "security",
    "non-profit and social impact"
    ]
    k=text.lower()
    if k in fields:
        return False
    return True

st.title("Market Research and AI Use Case Generation Agent")
st.markdown("***Give me a company or an industry and I will tell you how it can do better using AI.***")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Company or industry?"):

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('Loading'):
        research=tavilysearch(prompt,determine(prompt))
        response=geminillm(research)

        dataset_text=text_for_dataset(prompt)
        links=dataset_links(dataset_text)

        response_links = ""

        for title, url in links:
            response_links = response_links + f"- {title}: {url}" + "\n"

    
    with st.chat_message("assistant"):
        st.markdown(response + "\nDatasets for Use Case\n"+ response_links)
        st.download_button("Download Dataset Ref File", response_links, file_name="dataset_ref.txt", mime="text/plain")

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response + "\nDatasets for Use Case\n"+ response_links})
    
