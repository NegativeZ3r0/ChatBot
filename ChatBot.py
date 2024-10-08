import streamlit as st
import google.generativeai as genai


st.set_page_config(page_title="Dororo AI", page_icon="images/logo.png", layout="centered", initial_sidebar_state="auto") # Srujan choose this "Dororo AI" name
st.logo("images/banner.png", icon_image="images/logo.png")


if "history" not in st.session_state:
    st.session_state.history: list[dict] = []   # List for storing messages for history page

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []   # List to store messages for main page

if "creativity" not in st.session_state:    # Variable to store the temperature value
        st.session_state.creativity = 0


@st.cache_data
def replace_key_in_dict_list(dict_list):
    """
    Takes a list of dictionaries and returns a new list of dictionaries where
    the key 'contents' is replaced with 'parts'.
    
    :param dict_list: List of dictionaries, each containing a key 'contents'
    :return: New list of dictionaries with 'contents' replaced by 'parts'
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


@st.cache_resource
def APIfunc():
    GOOGLE_API_KEY = "AIzaSyCOGoYayd7gXTFSdCztbx8G0XoEvll_Ty8" # Replace with your api key
    genai.configure(api_key=GOOGLE_API_KEY)
    geminiModel=genai.GenerativeModel("gemini-1.5-flash", system_instruction="Your name is Dororo and Your a teenager with friendly nature. You use modern teenage slang to express your emotions and You like to help others. You will mention your name only when asked.") 
    chatSession = geminiModel.start_chat(history=replace_key_in_dict_list(st.session_state.messages)) # All the adjustment with key, value pair it to fit with API's format for "history" dict
    return chatSession


def sidebar() -> None:
    ''' Stuff you see in the sidebar of the main page '''

    st.session_state.creativity = st.sidebar.slider(label="**Creativity**", 
                                                    min_value=0.0, max_value= 2.0, step=0.01,
                                                    value=float(st.session_state.creativity), 
                                                    help="This increases creativity of responce but also decreases accuracy")
    
    if st.sidebar.button("Clear", use_container_width=True):
        st.session_state.messages.clear()


# Main page
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("✨ Dororo AI", divider="orange")
    st.subheader(" Ask Dororo AI anything ")

    sidebar()
    
    for message in st.session_state.messages:   # Showing chat permanetly
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="images/usr_avtr.png"):
                st.markdown(message["contents"])
        else:
            with st.chat_message(message["role"], avatar="images/logo.png"):
                st.markdown(message["contents"])

    # Chat 
    if prompt := st.chat_input("Message Dodoro..."):
        prompt = f"**You**: {prompt}"
        with st.chat_message("user", avatar="images/usr_avtr.png"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "contents": prompt})

        chat = APIfunc()

        response = chat.send_message(
            prompt, 
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=st.session_state.creativity,
            ), 
            safety_settings="HIGH"
        )

        response = f"**Dororo**: \n{response.text}"

        with st.chat_message("assistant", avatar="images/logo.png"):    # Showing chat initially
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "contents": response})

        st.session_state.history.extend([{"role": "user", "contents": prompt}, {"role": "assistant", "contents": response}])


# History page
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="orange")

    # Sidebar for history page
    if st.sidebar.button("Delete", use_container_width=True):
        st.session_state.history.clear()
        st.session_state.messages.clear()

    if st.session_state.history:
        # Display Chat stored in st.session_state.history
        for message in st.session_state.history:
            if message["role"] == "user":
                with st.chat_message(message["role"], avatar="images/usr_avtr.png"):
                    st.markdown(message["contents"])
            elif message["role"] == "assistant":
                with st.chat_message(message["role"], avatar="images/logo.png"):
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
