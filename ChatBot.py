import streamlit as st
import json
import os


st.set_page_config(page_title="ChatBot", page_icon=":material/stars:", layout="centered", initial_sidebar_state="auto")
st.logo("images/banner.png", icon_image="images/logo.png")
# docs: https://docs.streamlit.io/develop/api-reference/media/st.logo

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []

# Main page
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("✨ Dororo AI", divider="red")
    st.subheader(" Ask Dororo AI anything ")

    sidebar()

    # Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt: str = st.chat_input("Message Dodoro...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response: str = "response"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        storeHistory(prompt, response)


# History page
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="red")
    retrieved_list: list[dict]

    # Sidebar for history page
    if os.path.exists("History.json") and st.sidebar.button("Delete", use_container_width=True):
        os.remove("History.json")
        
    # Display Chat stored in History.json
    if os.path.exists("History.json"):
        with open("History.json", 'r') as f:
            retrieved_list = json.load(f)

        for message in retrieved_list:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    else:
        st.subheader("Nothing to show.")


def sidebar() -> None:
    ''' Stuff you see in the sidebar on the main page '''
    if "creativity" not in st.session_state:
        st.session_state["creativity"]: dict = 1

    st.session_state["creativity"] = st.sidebar.slider(label="**Creativity**", 
                                                        min_value=1, max_value= 5, 
                                                        value=st.session_state["creativity"], 
                                                        help="This increases creativity of responce but also decreases accuracy")
    
    if st.sidebar.button("Clear", use_container_width=True):
        st.session_state.messages.clear()


def storeHistory(user_prompt: str, bot_response: str) -> None:
    ''' Function to create and store Chat history in History.json file '''
    existing_data: list

    if os.path.exists("History.json"):
        with open("History.json", 'r') as f:
            existing_data = json.load(f)

        existing_data.extend([{"role": "user", "content": user_prompt}, {"role": "assistant", "content": bot_response}])
        json_list = json.dumps(existing_data)
    
    else:
        json_list = json.dumps(st.session_state.messages)

    with open("History.json", 'w') as f:
        f.write(json_list)


# Pages
pages: list = []
main_page = st.Page(ChatBot, title="ChatBot", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page])

pg = st.navigation(pages=pages)
pg.run()
