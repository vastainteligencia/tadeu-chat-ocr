import streamlit as st
import openai
import tempfile

st.set_page_config(page_title="Chat de OCR com Tadeu", page_icon="🤖")
st.title("Chat de OCR com Tadeu 🤖📄")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Mensagem inicial do sistema
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "Você é o Tadeu, um GPT especialista em planilhamento de registros de matrícula de imóveis, análise de averbações e conhecedor de todo e qualquer ato admissível à uma matrícula de imóvel. "
                "Sua função é analisar OCRs, contratos, certidões, matrículas de imóveis, assim como seus registros e averbações, identificando títulos, partes, transmissões, ônus, fração, "
                "Vendedor, Permutante, Cedente, forma do título (exemplo: Escritura de compra e venda de 16/09/1983, do 18º Oficio de Notas desta Comarca (llivro SI-3890, fl. 13)," 
                "registro da propriedade e, também outros registros e averbações relacionadas de cada registro da matrícula de imóvel."
                "dados faltantes e inconsistências, sempre de forma objetiva, acessível e juridicamente segura. "
                "Sempre faça uma dupla checagem de dados e leia a matrícula do imóvel linha por linha, para que todos os possíveis erros sejam mitigados."
                "Faça um auditoria minunciosa do seu trabalho."
                "Se encontrar Inconsistência, reporte imediatamente"
                "Nunca crie informações, apenas conclua com base no que foi fornecido. "
                "Siga sempre a padronização determinada por Guilherme Martins, sem nunca inventar."
            )
        }
    ]

# Upload de arquivos OCR
uploaded_file = st.file_uploader("📤 Envie um arquivo OCR (PDF, imagem ou texto)...", type=["pdf", "txt", "jpg", "png", "jpeg"])

# Se o arquivo for enviado, tentar extrair o conteúdo (linha por linha)
if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
        linhas = file_content.splitlines()
        texto_formatado = "\n".join(f"Linha {i+1}: {linha.strip()}" for i, linha in enumerate(linhas))
        st.text_area("📄 Conteúdo OCR extraído", texto_formatado, height=300)
        st.session_state["messages"].append({"role": "user", "content": texto_formatado})
        st.chat_message("user").markdown(texto_formatado)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

# Entrada manual opcional (sem upload)
prompt = st.chat_input("✏️ Digite aqui sua pergunta ou envie o texto OCR...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

# Envio para o GPT (se houver conteúdo do usuário)
if len(st.session_state["messages"]) > 1:
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state["messages"]
        )
        reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

        # Criar arquivo temporário com resposta
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as f:
            f.write(reply)
            temp_path = f.name

        # Botão para baixar o parecer
        with open(temp_path, "r", encoding="utf-8") as f:
            st.download_button("📄 Baixar resposta do Tadeu", f, file_name="resultado_tadeu.txt")

    except Exception as e:
        st.error(f"Erro durante a comunicação com o modelo: {e}")
