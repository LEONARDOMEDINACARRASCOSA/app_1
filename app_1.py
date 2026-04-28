import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados (use secrets no futuro para segurança)
URL_NEON = "postgresql://neondb_owner:npg_7LbEpic8UAPv@ep-blue-forest-an24utd1-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Conexão com o banco de dados
engine = create_engine(URL_NEON)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Modelagem da tabela
class Itinerario(Base):
    __tablename__ = 'itinerario'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)  # Corrigido: Adicionado 'nome'
    descricao = Column(String, nullable=False)

# Criação da tabela no banco, se não existir
Base.metadata.create_all(engine)

# Configuração da página Streamlit
st.set_page_config(page_title="Cadastro de Itinerário", page_icon="✈️")
st.title("Cadastro de Itinerário 2026")
st.info("Os dados serão salvos diretamente no PostgreSQL da nuvem Neon")

# Formulário para inserir dados
with st.form("formulario", clear_on_submit=True):
    nome_input = st.text_input("Nome do Itinerário")  # Corrigido: 'text_input' para captura de dados
    desc_input = st.text_area("Descrição do Itinerário")  # Usado 'text_area' para maior descrição
    botao = st.form_submit_button("Salvar Dados")

# Ação ao pressionar o botão de salvar
if botao:
    if nome_input and desc_input:  # Verificando se ambos os campos foram preenchidos
        session = Session()  # Criando sessão de banco de dados

        novo_registro = Itinerario(nome=nome_input, descricao=desc_input)  # Corrigido: 'nome' estava ausente
        session.add(novo_registro)  # Adicionando o registro
        session.commit()  # Commitando a transação
        session.close()  # Fechando a sessão do banco

        st.success(f"Sucesso! O itinerário '{nome_input}' foi salvo com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos corretamente!")

# Atualização de dados em tempo real
st.divider()
st.subheader("Registros Atuais")

session = Session()  # Criando uma nova sessão para consulta
dados = session.query(Itinerario).all()  # Consultando todos os itinerários no banco
session.close()  # Fechando a sessão após a consulta

# Exibindo os registros encontrados
if dados:
    for item in dados:
        st.write(f"{item.nome}: {item.descricao}")
else:
    st.info("Nenhum itinerário encontrado.")