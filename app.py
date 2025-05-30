import streamlit as st
import openai
from openai import OpenAI

st.set_page_config(page_title="Chat de OCR com Tadeu", page_icon="🤖")
st.title("Chat de OCR com Tadeu 🤖📄")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Você é o Tadeu, um GPT especialista em planilhamento de registros de matrícula de imóveis. Siga sempre a padronização determinada por Guilherme Martins, sem nunca inventar."}
    ]

# Upload de arquivos
uploaded_file = st.file_uploader("📤 Envie um arquivo OCR (PDF, imagem ou texto)...", type=["pdf", "txt", "jpg", "png", "jpeg"])
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.text_area("📄 Conteúdo do arquivo:", file_content, height=200)

prompt = st.chat_input("Digite aqui sua pergunta ou envie o texto OCR...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

    # Salvar em arquivo de resposta
    with open("/mount/data/resultado_tadeu.txt", "w", encoding="utf-8") as f:
        f.write(reply)

    st.success("✅ Resposta salva!")
    with open("/mount/data/resultado_tadeu.txt", "rb") as f:
        st.download_button("⬇️ Baixar resposta do Tadeu", f, file_name="resultado_tadeu.txt")
