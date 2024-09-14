import streamlit as st
import json
import os
import google.generativeai as genai


st.set_page_config(page_title="Dororo AI", page_icon="images/logo.png", layout="centered", initial_sidebar_state="auto") # Srujan choose this "Dororo AI" name
st.logo("images/banner.png", icon_image="images/logo.png")

GOOGLE_API_KEY = "***********************************" # Replace with Google_Api_Key 
genai.configure(api_key=GOOGLE_API_KEY)
geminiModel=genai.GenerativeModel("gemini-1.5-flash") 

if "history" not in st.session_state:
    st.session_state.history: list[dict] = []   # List for storing history messages

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []   # List to store messages for main page

if "creativity" not in st.session_state:
        st.session_state.creativity = 0


def replace_key_in_dict_list(dict_list):
    """
    Takes a list of dictionaries and returns a new list of dictionaries where
    the key 'contents' is replaced with 'name parts'.
    
    :param dict_list: List of dictionaries, each containing a key 'contents'
    :return: New list of dictionaries with 'contents' replaced by 'name parts'
    """
    # Create a new list to hold the modified dictionaries
    new_list = []

    # Define the prefix to be stripped
    prefix1 = '**You**:'
    prefix1_len = len(prefix1)
    prefix2 = '**Dororo**:'
    prefix2_len = len(prefix2)
    
    for d in dict_list:
        # Create a new dictionary for each entry
        new_dict = {}
        for key, value in d.items():
            # Replace 'contents' with 'name parts'
            if value == 'assistant':
                new_dict['role'] = "model"
            elif key == 'contents':
                # Remove the prefix if it exists
                if value.startswith(prefix1):
                    value = value[prefix1_len:].strip()
                elif value.startswith(prefix2):
                    value = value[prefix2_len:].strip()
                new_dict['parts'] = value
            else:
                new_dict[key] = value
        # Append the new dictionary to the new list
        new_list.append(new_dict)
    
    return new_list

chat = geminiModel.start_chat(history=replace_key_in_dict_list(st.session_state.messages))


# Main page
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("✨ Dororo AI", divider="orange")
    st.subheader(" Ask Dororo AI anything ")

    sidebar()

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["contents"])

    # Chat 
    prompt: str = st.chat_input("Message Dodoro...")
    if prompt:
        prompt = f"**You**: {prompt}"
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "contents": prompt})

        response = chat.send_message(prompt, 
                                    generation_config=genai.types.GenerationConfig(
                                    candidate_count=1,
                                    temperature=st.session_state.creativity,
                                    ),)

        response = f"**Dororo**: \n{response.text}"

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "contents": response})

        st.session_state.history.extend([{"role": "user", "contents": prompt}, {"role": "assistant", "contents": response}])


def sidebar() -> None:
    ''' Stuff you see in the sidebar on the main page '''

    st.session_state.creativity = st.sidebar.slider(label="**Creativity**", 
                                                    min_value=0.0, max_value= 2.0, step=0.1,
                                                    value=float(st.session_state.creativity), 
                                                    help="This increases creativity of responce but also decreases accuracy")
    
    if st.sidebar.button("Clear", use_container_width=True):
        st.session_state.messages.clear()

# History page
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="red")

    # Sidebar for history page
    if st.sidebar.button("Delete", use_container_width=True):
        st.session_state.history.clear()
        st.session_state.messages.clear()

    if st.session_state.history:
        # Display Chat stored in st.session_state.history
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["contents"])
    else:
        st.subheader("Nothing to show.")


# Pages
pages: list = []
main_page = st.Page(ChatBot, title="Dororo AI", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page])

pg = st.navigation(pages=pages)
pg.run()
