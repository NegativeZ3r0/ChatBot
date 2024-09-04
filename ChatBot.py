import streamlit as st


# ToDo: st.logo("images/banner.jpg", icon_image="images/logo.png")
# Help: https://docs.streamlit.io/develop/api-reference/media/st.logo

st.set_page_config(page_title="ChatBot", page_icon=":material/stars:")
# st.session_state: dict = {}
pages: list = []

# each page has it's logic in the following fuctions.
def ChatBot() -> None:
    ''' Stuff you see on main page '''
    # not sure this. st.sidebar.title("")
    st.header("✨ Dororo AI", divider="red")
    st.subheader(" Ask Dororo AI anything ")

    #Display a single-line text input widget.

    prompt = st.chat_input("Message Dodoro...")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")
    

    st.sidebar.slider("Level of Creativity", 1, 5, key="size") # parameter that controls the randomness or creativity of the generated text.

def history() -> None:
    ''' Stuff you see on second page '''
    st.header("🕔 History", divider="red")
    st.subheader(" Second Page ")


# Pages. note that function names are passed to st.pages() as first parameter
main_page = st.Page(ChatBot, title="ChatBot", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page, ])

pg = st.navigation(pages=pages)
pg.run()
    
