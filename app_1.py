import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Usando secrets (mais seguro)
URL_NEON = st.secrets["database_url"]

engine = create_engine(URL_NEON)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Itinerario(Base):
    __tablename__ = 'itinerario'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

Base.metadata.create_all(engine)

st.set_page_config(page_title="Cadastro de Itinerário", page_icon="✈️")
st.title("Cadastro de Itinerário 2026")
st.info("Os dados serão salvos diretamente no PostgreSQL da nuvem Neon")

with st.form("formulario", clear_on_submit=True):
    nome_input = st.text_input("Nome do Itinerário")
    desc_input = st.text_area("Descrição do Itinerário")
    botao = st.form_submit_button("Salvar Dados")

if botao:
    if nome_input.strip() and desc_input.strip():
        with Session() as session:
            novo_registro = Itinerario(nome=nome_input, descricao=desc_input)
            session.add(novo_registro)
            session.commit()

        st.success(f"Sucesso! O itinerário '{nome_input}' foi salvo!")
    else:
        st.error("Por favor, preencha todos os campos corretamente!")

st.divider()
st.subheader("Registros Atuais")

with Session() as session:
    dados = session.query(Itinerario).all()

if dados:
    for item in dados:
        st.write(f"{item.nome}: {item.descricao}")
else:
    st.info("Nenhum itinerário encontrado.")