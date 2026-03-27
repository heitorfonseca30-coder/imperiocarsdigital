import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
from datetime import datetime, timedelta

# =================================================================
# 🎨 DESIGN PREMIUM (OTIMIZADO PARA TELAS GRANDES)
# =================================================================
st.set_page_config(page_title="Império Cars Digital - Portal BI", layout="wide", page_icon="🏎️")

# Estilo CSS para Cards, Botões e Layout Desktop
st.markdown(\"\"\"
    
    .stApp { background-color: #f4f7f6; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #1E3A8A; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1E3A8A; color: white; font-weight: bold; height: 3em; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
\"\"\", unsafe_allow_html=True)

# =================================================================
# 🛡️ SEGURANÇA E ACESSO
# =================================================================
SENHA_MESTRA_DONO = \"300611h@bi\"
def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

usuarios_db = {
    \"Empresa_Alpha\": {\"senha\": gerar_hash(\"Alpha@2026\"), \"nicho\": \"🛒 Supermercado\", \"vencimento\": datetime.now() + timedelta(hours=2)},
    \"User_Teste\": {\"senha\": gerar_hash(\"123\"), \"nicho\": \"🍔 Restaurante\", \"vencimento\": datetime.now() + timedelta(minutes=30)}
}

# =================================================================
# 🚀 MOTOR DE DADOS & INTERFACE
# =================================================================
if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.user = None

if not st.session_state.logado:
    st.title(\"🏎️ Império Cars Digital - Portal Desktop\")
    st.write(\"Bem-vindo ao seu centro de comando empresarial.\")
    col1, col2 = st.columns([1, 1])
    with col1:
        u_in = st.text_input(\"Usuário da Empresa\")
        s_in = st.text_input(\"Senha\", type=\"password\")
        if st.button(\"Acessar Painel de Controle\"):
            if u_in in usuarios_db and gerar_hash(s_in) == usuarios_db[u_in][\"senha\"]:
                st.session_state.logado = True
                st.session_state.user = u_in
                st.rerun()
            else: st.error(\"❌ Credenciais Inválidas\")
else:
    user = st.session_state.user
    d_user = usuarios_db[user]
    
    # Menu Lateral Desktop
    st.sidebar.markdown(f\"# 🏢 {user}\")
    aba = st.sidebar.radio(\"Navegação do Sistema\", [\"📊 Dashboard Principal\", \"🏆 Ranking Vendedores\", \"💡 Dicas de Especialista\", \"💳 Planos & Assinaturas\", \"🔐 Área do Dono\", \"💬 Suporte IA\"])
    
    # Gerador de Dados para Gráficos
    df = pd.DataFrame({
        \"Data\": [datetime.now() - timedelta(days=x) for x in range(30)],
        \"Vendas\": np.random.randint(2000, 8000, 30),
        \"Lucro\": np.random.randint(500, 2000, 30),
        \"Vendedor\": np.random.choice([\"Marcos\", \"Ana\", \"Carlos\"], 30)
    })

    # --- ABA 1: DASHBOARD ---
    if aba == \"📊 Dashboard Principal\":
        st.title(f\"📊 Dashboard: {d_user['nicho']}\")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(\"Faturamento Total\", f\"R$ {df['Vendas'].sum():,.2f}\", \"+18%\")
        with c2: st.metric(\"Ticket Médio Mensal\", f\"R$ {df['Vendas'].mean():,.2f}\")
        with c3: st.metric(\"Lucro Líquido\", f\"R$ {df['Lucro'].sum():,.2f}\", \"🔥\")
        st.plotly_chart(px.area(df, x=\"Data\", y=\"Vendas\", title=\"Fluxo Financeiro Diário\", color_discrete_sequence=['#1E3A8A']), use_container_width=True)

    # --- ABA 2: RANKING VENDEDORES ---
    elif aba == \"🏆 Ranking Vendedores\":
        st.title(\"🏆 Ranking de Produtividade\")
        rank = df.groupby(\"Vendedor\")[\"Vendas\"].sum().sort_values(ascending=False)
        st.bar_chart(rank)
        st.info(f\"Parabéns para **{rank.idxmax()}**, o destaque do mês!\")

    # --- ABA 3: DICAS (ESTÉTICA COM CARDS) ---
    elif aba == \"💡 Dicas de Especialista\":
        st.title(\"💡 Insights Estratégicos\")
        col1, col2 = st.columns(2)
        with col1: st.success(\"### 📈 Meta de Vendas\
Seu faturamento superou a meta em 12%. Ótimo momento para expansão!\")
        with col2: st.warning(\"### 📉 Alerta de Custos\
Atenção: Os custos operacionais subiram. Verifique a logística.\")

    # --- ABA 4: PLANOS ---
    elif aba == \"💳 Planos & Assinaturas\":
        st.title(\"💳 Planos Disponíveis\")
        p1, p2, p3 = st.columns(3)
        with p1: st.markdown(\"### Bronze\
**R$ 99/mês**\
✅ Dashboards\"); st.button(\"Assinar Bronze\")
        with p2: st.markdown(\"### Prata\
**R$ 199/mês**\
✅ WhatsApp + IA\"); st.button(\"Assinar Prata\")
        with p3: st.markdown(\"### Ouro\
**R$ 399/mês**\
✅ VIP + Mentoria\"); st.button(\"Assinar Ouro\")

    # --- ABA 5: ÁREA DO DONO ---
    elif aba == \"🔐 Área do Dono\":
        st.title(\"🔐 Painel Admin\")
        sm = st.text_input(\"Senha Mestra\", type=\"password\")
        if sm == SENHA_MESTRA_DONO:
            st.success(\"Acesso Autorizado\"); st.metric(\"Receita SaaS\", \"R$ 4.500,00\")
            if st.button(\"Soltar Balões\"): st.balloons()
        else: st.warning(\"Aguardando senha mestra...\")

    # --- ABA 6: SUPORTE IA ---
    elif aba == \"💬 Suporte IA\":
        st.title(\"💬 Chat de Suporte\")
        if st.chat_input(\"Dúvida?\"): st.write(\"IA: Analisando dados... Recomendo focar em retenção de clientes hoje.\")

    if st.sidebar.button(\"Sair do Sistema\"):
        st.session_state.logado = False; st.rerun()

with st.expander(\"📖 Manual v35.0 - Império Cars\"):
    st.write(\"Versão Sincronizada: Otimizada para Celular e Computador.\")
