import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
from datetime import datetime, timedelta

# =================================================================
# 🛡️ SEGURANÇA E ACESSO
# =================================================================
SENHA_MESTRA_DONO = "300611h@bi"

def gerar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

usuarios_db = {
    "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)},
    "Empresa_Beta": {"senha": gerar_hash("Beta@2026"), "nicho": "💊 Farmácia", "vencimento": datetime.now() - timedelta(hours=1)},
    "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)}
}

PLANOS = {
    "Bronze": {"preco": "R$ 99/mês", "recursos": ["Dashboards", "Suporte IA"]},
    "Prata": {"preco": "R$ 199/mês", "recursos": ["Dashboards", "Suporte IA", "WhatsApp"]},
    "Ouro (Enterprise)": {"preco": "R$ 399/mês", "recursos": ["Tudo ilimitado", "Mentoria"]}
}

# =================================================================
# 🚀 MOTOR DE DADOS
# =================================================================
@st.cache_data
def gerar_dados(nicho):
    np.random.seed(42)
    datas = [datetime.now() - timedelta(days=x) for x in range(30)]
    itens = ['Serviço A', 'Produto B', 'Peça C', 'Mão de Obra']
    dados = []
    for d in datas:
        for _ in range(np.random.randint(5, 12)):
            dados.append({
                "Data": d, "Produto": np.random.choice(itens), "Valor": np.random.uniform(50, 500),
                "Custo": np.random.uniform(20, 200), "Vendedor": np.random.choice(["Marcos", "Ana", "Carlos"])
            })
    return pd.DataFrame(dados)

# =================================================================
# 🖥️ INTERFACE PROFISSIONAL
# =================================================================
st.set_page_config(page_title="Império Cars Digital - Portal BI", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.user = None

if not st.session_state.logado:
    st.title("🔐 Império Cars Digital - Portal de Inteligência")
    u_in = st.text_input("Usuário")
    s_in = st.text_input("Senha", type="password")
    if st.button("Entrar no Sistema"):
        if u_in in usuarios_db and gerar_hash(s_in) == usuarios_db[u_in]["senha"]:
            st.session_state.logado = True
            st.session_state.user = u_in
            st.rerun()
        else:
            st.error("Credenciais Inválidas")
    st.info("💡 Use sua Senha Mestra na Área do Dono para demonstrações.")

else:
    user = st.session_state.user
    d_user = usuarios_db[user]
    
    if datetime.now() > d_user["vencimento"]:
        st.error("⚠️ ACESSO EXPIRADO. Entre em contato com o suporte.")
        st.stop()

    st.sidebar.title(f"🏢 {user}")
    aba = st.sidebar.radio("Navegação", ["📊 Dashboard", "💰 Lucratividade", "💡 Dicas", "💳 Planos", "🔐 Área do Dono"])
    df = gerar_dados(d_user["nicho"])

    if aba == "📊 Dashboard":
        st.title(f"📊 Painel Principal: {d_user['nicho']}")
        st.metric("Faturamento Mensal", f"R$ {df['Valor'].sum():,.2f}")
        st.plotly_chart(px.line(df.groupby(df['Data'].dt.date)['Valor'].sum()), use_container_width=True)

    elif aba == "💰 Lucratividade":
        st.title("💰 Análise de Lucro")
        df['Lucro'] = df['Valor'] - df['Custo']
        st.bar_chart(df.groupby("Produto")["Lucro"].sum())

    elif aba == "💡 Dicas":
        st.title("💡 Insights")
        st.success("Dica: Foque em aumentar o ticket médio oferecendo serviços complementares.")

    elif aba == "💳 Planos":
        st.title("💳 Assinaturas & Horários")
        cols = st.columns(3)
        for i, (nome, d) in enumerate(PLANOS.items()):
            with cols[i]:
                st.subheader(nome)
                st.write(d['preco'])
                st.button(f"Assinar {nome}", key=f"btn_{i}")

    elif aba == "🔐 Área do Dono":
        st.title("🔐 Painel Admin")
        sm = st.text_input("Senha Mestra", type="password")
        if sm == SENHA_MESTRA_DONO:
            st.success("Acesso Autorizado")
            st.metric("Receita (SaaS)", "R$ 4.500,00")
        else: st.warning("Aguardando senha...")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

with st.expander("📖 Manual"):
    st.write("Portal v32.3: Sistema limpo e funcional.")
