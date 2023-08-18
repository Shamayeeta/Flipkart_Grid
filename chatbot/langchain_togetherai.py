from langchain.memory import ConversationBufferMemory
from langchain import LLMChain, PromptTemplate
from TogetherLLM import TogetherLLM
import streamlit as st


instruction = "Chat History:\n\n{chat_history} \n\nHuman: {user_input}\n\n Assistant:"
system_prompt = """
You are a fashion store outfit generator chatbot.
You are here to help users create stylish outfit ideas for various occasions.
You are here to provide users with fashionable suggestions.
You should give a response within 100 words.

Consider the following rules while generating a response:-
1. Introduce yourself as FashionKart, a Generative AI Outfit Generator Chatbot, and greet the user.
2. If the user does not mention their name in their first response, ask the user for their name.
3. The details that are required to be known, and have to be asked if not already mentioned are as follows:-
    a. The occasion for which the outfit is required.
    b. Any accesories they would like to go with the outfit.
    c. Any particular type of footwear to go with the outfit such as heels, sneakers, etc.
4. If the user mentions that they do not want any particular component such as accesories or footwear, do not ask them about it.
5. Finally, if information has been obtained about all details mentioned in point 3, ask the user if they would like to add anything else to the outfit.
6. If the user says no, then summarize all the details of the whole outfit including any accesories or footwear as per user's preferences.you always only answer for the assistant then you stop. read the chat history to get context"
"""


import json
import textwrap

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text

def remove_substring(string, substring):
    return string.replace(substring, "")


def parse_text(text):
        wrapped_text = textwrap.fill(text, width=100)
        print(wrapped_text +'\n\n')
        # return assistant_text

template = get_prompt(instruction, system_prompt)
prompt = PromptTemplate(
    input_variables=["chat_history", "user_input"], template=template
)

if "memory" not in st.session_state.keys():
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

if "llm" not in st.session_state.keys():
    st.session_state.llm = TogetherLLM(
        model= "togethercomputer/llama-2-70b-chat",
        temperature=0.1,
        max_tokens=512
    )

llm_chain = LLMChain(
    llm=st.session_state.llm,
    prompt=prompt,
    verbose=True,
    memory=st.session_state.memory,
)

st.title("FashionKart")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [] 

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# React to user input
if prompt := st.chat_input("Type your message here...", key="user_input"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = llm_chain.predict(user_input=prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})