import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
from datetime import datetime, timedelta

# =================================================================
# 🎨 DESIGN PREMIUM (COMPUTADOR & CELULAR)
# =================================================================
st.set_page_config(page_title="Império Cars Digital - Portal BI", layout="wide", page_icon="🏎️")

# Estilo CSS Puro (Sem barras invertidas)
st.markdown("""
    
    .stApp { background-color: #f4f7f6; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #1E3A8A; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1E3A8A; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 🛡️ SEGURANÇA E ACESSO
# =================================================================
SENHA_MESTRA_DONO = "300611h@bi"
def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

usuarios_db = {
    "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)},
    "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)}
}

# =================================================================
# 🚀 MOTOR DE DADOS & INTERFACE
# =================================================================
if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.user = None

if not st.session_state.logado:
    st.title("🏎️ Império Cars Digital - Acesso Seguro")
    col1, col2 = st.columns(2)
    with col1:
        u_in = st.text_input("Usuário")
        s_in = st.text_input("Senha", type="password")
        if st.button("Entrar no Painel"):
            if u_in in usuarios_db and gerar_hash(s_in) == usuarios_db[u_in]["senha"]:
                st.session_state.logado = True
                st.session_state.user = u_in
                st.rerun()
            else: st.error("❌ Credenciais Inválidas")
else:
    user = st.session_state.user
    d_user = usuarios_db[user]
    
    st.sidebar.title(f"🏢 {user}")
    aba = st.sidebar.radio("Navegação", ["📊 Dashboard", "🏆 Ranking", "💡 Dicas", "💳 Planos", "🔐 Área do Dono"])
    
    df = pd.DataFrame({
        "Data": [datetime.now() - timedelta(days=x) for x in range(30)],
        "Vendas": np.random.randint(2000, 8000, 30),
        "Vendedor": np.random.choice(["Marcos", "Ana", "Carlos"], 30)
    })

    if aba == "📊 Dashboard":
        st.title(f"📊 Painel: {d_user['nicho']}")
        c1, c2 = st.columns(2)
        with c1: st.metric("Faturamento Total", f"R$ {df['Vendas'].sum():,.2f}")
        with c2: st.metric("Ticket Médio", f"R$ {df['Vendas'].mean():,.2f}")
        st.plotly_chart(px.area(df, x="Data", y="Vendas", title="Fluxo Financeiro"), use_container_width=True)

    elif aba == "🏆 Ranking":
        st.title("🏆 Ranking de Vendedores")
        rank = df.groupby("Vendedor")["Vendas"].sum().sort_values(ascending=False)
        st.bar_chart(rank)

    elif aba == "💡 Dicas":
        st.title("💡 Insights IA")
        st.success("Dica: Foque em aumentar o ticket médio oferecendo serviços complementares hoje.")

    elif aba == "💳 Planos":
        st.title("💳 Planos de Assinatura")
        p1, p2, p3 = st.columns(3)
        with p1: st.markdown("### Bronze
**R$ 99**"); st.button("Assinar Bronze")
        with p2: st.markdown("### Prata
**R$ 199**"); st.button("Assinar Prata")
        with p3: st.markdown("### Ouro
**R$ 399**"); st.button("Assinar Ouro")

    elif aba == "🔐 Área do Dono":
        st.title("🔐 Painel Admin")
        sm = st.text_input("Senha Mestra", type="password")
        if sm == SENHA_MESTRA_DONO:
            st.success("Acesso Autorizado"); st.metric("Receita SaaS", "R$ 4.500,00")
            if st.button("Soltar Balões"): st.balloons()
        else: st.warning("Aguardando senha mestra...")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False; st.rerun()

with st.expander("📖 Manual v35.1"):
    st.write("Portal Sincronizado e Purificado de Erros.")
