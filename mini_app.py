import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
from datetime import datetime, timedelta

# =================================================================
# 🛡️ CONFIGURAÇÕES DE SEGURANÇA
# =================================================================
SENHA_MESTRA_DONO = "300611h@bi"

def gerar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

usuarios_db = {
    "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)},
    "Empresa_Beta": {"senha": gerar_hash("Beta@2026"), "nicho": "💊 Farmácia", "vencimento": datetime.now() - timedelta(hours=1)},
    "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)}
}

# =================================================================
# 🚀 GERADOR DE DADOS
# =================================================================
@st.cache_data
def gerar_dados_simulados(nicho_escolhido):
    np.random.seed(42)
    datas = [datetime.now() - timedelta(days=x) for x in range(30)]
    configs = {
        "🛒 Supermercado": (['Arroz', 'Feijão', 'Leite', 'Carne'], [28.0, 9.0, 5.0, 45.0]),
        "💊 Farmácia": (['Amoxicilina', 'Dipirona', 'Vitamina C', 'Fraldas'], [50.0, 6.0, 25.0, 60.0]),
        "🍔 Restaurante": (['Prato Feito', 'Burger', 'Cerveja', 'Suco'], [32.0, 38.0, 12.0, 10.0]),
        "🚗 Oficina": (['Troca Óleo', 'Revisão', 'Pastilha', 'Mão de Obra'], [220.0, 500.0, 280.0, 180.0])
    }
    itens, precos = configs.get(nicho_escolhido, (['Item'], [10.0]))
    dados = []
    for d in datas:
        for _ in range(np.random.randint(5, 15)):
            idx = np.random.randint(0, len(itens))
            dados.append({
                "Data": d, "Produto": itens[idx], "Valor": precos[idx] * np.random.uniform(0.9, 1.1),
                "Custo": precos[idx] * 0.6, "Vendedor": np.random.choice(["Marcos", "Ana", "Carlos"])
            })
    return pd.DataFrame(dados)

# =================================================================
# 🖥️ INTERFACE
# =================================================================
st.set_page_config(page_title="Portal BI SaaS v30.1", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.user = None

if not st.session_state.logado:
    st.title("🔐 Portal BI - Acesso Restrito")
    u_in = st.text_input("Usuário")
    s_in = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u_in in usuarios_db and gerar_hash(s_in) == usuarios_db[u_in]["senha"]:
            st.session_state.logado = True
            st.session_state.user = u_in
            st.rerun()
        else:
            st.error("Credenciais Inválidas")
else:
    user = st.session_state.user
    d_user = usuarios_db[user]
    if datetime.now() > d_user["vencimento"]:
        st.error("⚠️ ACESSO EXPIRADO")
        st.stop()

    st.sidebar.title(f"🏢 {user}")
    aba = st.sidebar.radio("Menu", ["📊 Dashboard", "💰 Lucro", "🔐 Área do Dono"])
    df = gerar_dados_simulados(d_user["nicho"])

    if aba == "📊 Dashboard":
        st.title(f"📊 Dashboard: {d_user['nicho']}")
        st.metric("Faturamento", f"R$ {df['Valor'].sum():,.2f}")
        st.plotly_chart(px.line(df.groupby(df['Data'].dt.date)['Valor'].sum(), title="Vendas Diárias"), use_container_width=True)

    elif aba == "💰 Lucro":
        st.title("💰 Análise de Lucro")
        df['Lucro'] = df['Valor'] - df['Custo']
        st.bar_chart(df.groupby("Produto")["Lucro"].sum())

    elif aba == "🔐 Área do Dono":
        st.title("🔐 Painel Admin")
        sm = st.text_input("Senha Mestra", type="password")
        if sm == SENHA_MESTRA_DONO:
            st.success("Acesso Autorizado")
            st.metric("Receita Mensal (SaaS)", "R$ 4.500,00")
        else:
            st.warning("Aguardando senha...")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

with st.expander("📖 Manual"):
    st.write("Portal v30.1: Sistema pronto para operação.")
