import streamlit as st
import json


st.set_page_config(page_title="ChatBot", page_icon=":material/stars:", layout="centered", initial_sidebar_state="auto")
st.logo("images/banner.jpg", link="",icon_image="images/logo.jpg")
# Help: https://docs.streamlit.io/develop/api-reference/media/st.logo
pages: list = []
if "messages" not in st.session_state:
        st.session_state.messages = []


# Main page logic
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("✨ Dororo AI", divider="red")
    st.subheader(" Ask Dororo AI anything ")

    # Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt = st.chat_input("Message Dodoro...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "response"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


    # Sidebar
    if 'creativity' not in st.session_state:
        st.session_state["creativity"] = 1

    st.session_state["creativity"] = st.sidebar.slider(label="**Creativity**", 
                                                        min_value=1, max_value= 5, 
                                                        value=st.session_state["creativity"], 
                                                        help="This increases creativity of responce but also decreases accuracy")

# History page logic
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="red")
 
    # Stores history in History.json file
    with open('History.json', 'w') as f:
        json.dump(st.session_state.messages, f)

    retrieved_dict = {}
    with open('History.json', 'r') as f:
        retrieved_dict = json.load(f)

    for message in retrieved_dict:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Pages
main_page = st.Page(ChatBot, title="ChatBot", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page, ])

pg = st.navigation(pages=pages)
pg.run()
