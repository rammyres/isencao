import streamlit as st
from docx import Document
from num2words import num2words
import tempfile
import os

st.title("Gerador de Declaração de Isenção de IRRF")
st.set_page_config(page_title='Gerador de Declaração de Isenção de IRRF')

with st.form("formulario"):
    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    cidade = st.text_input("Cidade")
    uf = st.text_input("UF")
    cpf_cnpj = st.text_input("CPF/CNPJ")
    processo = st.text_input("Número do Processo")
    vara_orgao = st.text_input("Vara/Órgão")
    secao = st.text_input("Seção/Subseção Judiciária")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    local = st.text_input("Local")
    data = st.date_input("Data")
    submit = st.form_submit_button("Gerar Documento")

if submit:
    valor_extenso = num2words(valor, lang='pt_BR', to='currency')

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
        "local": local,
        "data": data.strftime("%d/%m/%Y")
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
