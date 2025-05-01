import streamlit as st
from docx import Document
from num2words import num2words
import tempfile
import os
import locale
from datetime import datetime

def ajusta_data(data):
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    # data_obj = datetime.strftime(data, "%Y/%m/%d")

    # data_obj = datetime.strptime(data, "%Y/%m/%d")

    return data.strftime("%d de %B de %Y")


st.set_page_config(page_title='Gerador de Declaração de Isenção')
st.title("Gerador de Declaração de Isenção de IRPF para precatórios e RPV federais")

@st.dialog("Não salvamos seus dados")
def nao_salvo():
    st.text("Não salvamos seus dados. O arquivo gerado é temporário e não é armazenado em nosso servidor.")
    if st.button("Fechar"):
        st.session_state.modal_exibido = True
        st.rerun()

# Verifica se o modal já foi exibido nesta sessão
if "modal_exibido" not in st.session_state:
    st.session_state.modal_exibido = False

if not st.session_state.modal_exibido:
    nao_salvo()


with st.form("formulario"):
    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    cidade = st.text_input("Cidade")
    uf = st.text_input("UF")
    cpf_cnpj = st.text_input("CPF/CNPJ")
    processo = st.text_input("Número do Processo")
    vara_orgao = st.text_input("Vara/Órgão")
    secao = st.text_input("Seção/Subseção Judiciária")
    col1, col2 = st.columns([3, 1])
    with col1:
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    with col2:
        st.text("")
        st.text("")
        valor_desatualizado = st.checkbox("Valor desatualizado")
    
    local = st.text_input("Local")
    data = st.date_input("Data")
    submit = st.form_submit_button("Gerar Documento")

if submit:
    valor_extenso = num2words(valor, lang='pt_BR', to='currency')

    mais_correcores = ""
    if valor_desatualizado:
        mais_correcores = "mais correções "

    
    dados = {
        "nome": nome,
        "endereço": endereco,
        "cidade": cidade,
        "UF": uf,
        "CPF/CNPJ": cpf_cnpj,
        "processo": processo,
        "vara/órgão": vara_orgao,
        "seção": secao,
        "valor": f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "valor por extenso": valor_extenso,
        "mais correções": mais_correcores,
        "local": local,
        "data": ajusta_data(data=data)
    }

    doc = Document("isencao_template.docx")

    for p in doc.paragraphs:
        for chave, valor_str in dados.items():
            if f"{{{chave}}}" in p.text:
                p.text = p.text.replace(f"{{{chave}}}", valor_str)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "rb") as file:
        st.download_button(
            label="📄 Baixar Declaração Preenchida",
            data=file,
            file_name="declaracao_isencao.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    os.remove(tmp_path)
