
import streamlit as st
from chatbot import get_answer

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="🎓"
)

st.title("🎓 AI Student Assistant Chatbot")
st.write("Mujh se kisi bhi topic par sawal poochhein!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat screen par dikhayein
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Naya sawal receive karein
if user_question := st.chat_input("Apna sawal yahan likhein..."):

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    # Purani conversation AI ko bhi bhejein
    history = st.session_state.messages[:-1]

    with st.chat_message("assistant"):
        with st.spinner("AI soch raha hai..."):
            answer = get_answer(user_question, history)
            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
