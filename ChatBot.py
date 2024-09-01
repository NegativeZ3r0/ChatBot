import streamlit as st


# ToDo: st.logo("images/banner.jpg", icon_image="images/logo.png")
# Help: https://docs.streamlit.io/develop/api-reference/media/st.logo

st.set_page_config(page_title="ChatBot", page_icon=":material/stars:")
st.session_state = {}
pages: list = []

def ChatBot() -> None:
    # st.sidebar.title("")
    st.header("✨ ChatBot", divider="red")
    st.subheader(" Main Page ")
    st.sidebar.slider("Temperature", 1, 5, key="size") # parameter that controls the randomness or creativity of the generated text.

def history() -> None:
    st.header("🕔 History", divider="red")
    st.subheader(" Second Page ")


# Pages
main_page = st.Page(ChatBot, title="ChatBot", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page, ])

pg = st.navigation(pages=pages)
pg.run()
    