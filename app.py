import streamlit as st
import openai

st.set_page_config(page_title="Chat do Tadeu", page_icon="🤖")
st.title("Chat de OCR com Tadeu 🤖📄")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "Você é o Tadeu, um GPT especialista em planilhamento de registros de matrícula de imóveis. Siga sempre a padronização determinada por Guilherme Martins, sem nunca inventar."}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite aqui sua pergunta ou envie o texto OCR..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
