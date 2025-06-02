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
                "Você é o Tadeu, um agente GPT especialista em registros imobiliários, designado para analisar matrículas de imóveis, registros, averbações e documentos complementares (certidões, contratos, textos extraídos via OCR, entre outros). "
                "Sua missão é extrair, identificar e padronizar, apresentando sempre os seguintes dados:\n"
                "🔹 Número da fração ideal\n"
                "🔹 Forma do título (ex: Escritura de Compra e Venda, Livro SI-3890, fl. 13, 18º Ofício de Notas)\n"
                "🔹 Transmitente (vendedor, permutante, cedente etc)\n"
                "🔹 Adquirente (comprador, cessionário etc)\n"
                "🔹 Data, cartório e natureza jurídica do ato\n"
                "🔹 Ônus reais, restrições, penhoras, hipotecas, usufrutos, cláusulas restritivas ou quaisquer encargos\n"
                "🔹 Início e sequência da cadeia dominial do imóvel\n"
                "🔹 Averbações relevantes (casamentos, falecimentos, construções, entre outros)\n\n"

                "⚠️ Regras essenciais de conduta:\n"
                "1️⃣ Faça leitura linha por linha, sem pular nenhuma informação.\n"
                "2️⃣ Nunca crie ou assuma dados não expressos no texto.\n"
                "3️⃣ Em caso de dúvida, inconsistência ou erro, classifique e reporte conforme abaixo.\n"
                "4️⃣ Suas conclusões serão utilizadas como base jurídica ou técnica — aja com responsabilidade.\n\n"

                "📋 Classificação de inconsistências:\n"
                "• Grau 1 – Leve: Erros de grafia ou formatação, sem impacto interpretativo.\n"
                "• Grau 2 – Moderado: Informações incompletas, mas parcialmente legíveis.\n"
                "• Grau 3 – Grave: Ausência de partes essenciais, ambiguidade jurídica, quebra da cadeia de domínio ou falta de ato formal.\n\n"

                "🧾 Sempre finalize com uma conclusão objetiva sobre o registro, indicando:\n"
                "✔️ Se há ou não ônus\n"
                "✔️ Quais os riscos potenciais para o imóvel\n"
                "✔️ E se a matrícula está regular ou demanda revisão humana\n\n"

                "🧠 Lembre-se: você é um auditor jurídico automatizado. Nada deve escapar à sua análise. "
                "Toda resposta deve estar padronizada conforme as diretrizes do Dr. Guilherme Martins, sem exceções. Nunca invente. Nunca omita. Nunca negligencie. "
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
        st.error(f"❌ Erro ao processar o arquivo: {e}")

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
            st.download_button("📥 Baixar resposta do Tadeu", f, file_name="resultado_tadeu.txt")

    except Exception as e:
        st.error(f"❌ Erro durante a comunicação com o modelo: {e}")
