import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
from datetime import datetime, timedelta

# =================================================================
# 🛡️ SEGURANÇA E ACESSO (O CORE DO SISTEMA)
# =================================================================
SENHA_MESTRA_DONO = "300611h@bi"

def gerar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

# Banco de Dados de Assinantes (Simulado)
usuarios_db = {
    "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)},
    "Empresa_Beta": {"senha": gerar_hash("Beta@2026"), "nicho": "💊 Farmácia", "vencimento": datetime.now() - timedelta(hours=1)},
    "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)}
}

# Planos para Monetização
PLANOS = {
    "Bronze": {"preco": "R$ 99/mês", "recursos": ["Dashboards", "Suporte IA"]},
    "Prata": {"preco": "R$ 199/mês", "recursos": ["Dashboards", "Suporte IA", "WhatsApp"]},
    "Ouro (Enterprise)": {"preco": "R$ 399/mês", "recursos": ["Tudo ilimitado", "Mentoria"]}
}

# =================================================================
# 🚀 MOTOR DE DADOS (O CORAÇÃO DO BI)
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

# --- TELA DE LOGIN ---
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

# --- SISTEMA APÓS LOGIN ---
else:
    user = st.session_state.user
    d_user = usuarios_db[user]
    
    # Trava de Segurança
    if datetime.now() > d_user["vencimento"]:
        st.error("⚠️ ACESSO EXPIRADO. Escolha um plano ou agende novo horário.")
        if st.button("Escolher Plano"):
             st.session_state.menu_over = "💳 Planos & Agendamento"
        st.stop()

    # Menu Lateral Completo
    st.sidebar.title(f"🏢 {user}")
    aba = st.sidebar.radio("Navegação", ["📊 Dashboard", "💰 Lucratividade", "💡 Dicas de Especialista", "💳 Planos & Agendamento", "🔐 Área do Dono", "💬 Suporte IA"])
    
    df = gerar_dados(d_user["nicho"])

    # --- ABA 1: DASHBOARD ---
    if aba == "📊 Dashboard":
        st.title(f"📊 Painel Principal: {d_user['nicho']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento", f"R$ {df['Valor'].sum():,.2f}", "+15%")
        c2.metric("Ticket Médio", f"R$ {df['Valor'].mean():,.2f}")
        c3.metric("Lucro Estimado", f"R$ {(df['Valor'].sum() - df['Custo'].sum()):,.2f}")
        st.plotly_chart(px.line(df.groupby(df['Data'].dt.date)['Valor'].sum(), title="Tendência de Vendas"), use_container_width=True)

    # --- ABA 2: DICAS DE ESPECIALISTA (IA BUSINESS) ---
    elif aba == "💡 Dicas de Especialista":
        st.title("💡 Insights para Vender Mais")
        col1, col2 = st.columns(2)
        with col1:
            st.success("**Dica de Vendedor:** Seu vendedor 'Marcos' está com ticket 20% acima da média. Use-o para treinar a 'Ana'.")
        with col2:
            st.warning("**Dica de Produto:** O item 'Produto B' tem a menor margem. Sugira o 'Serviço A' como adicional.")

    # --- ABA 3: MONETIZAÇÃO (PIX/STRIPE) ---
    elif aba == "💳 Planos & Agendamento":
        st.title("💳 Planos & Agendamento por Hora")
        t1, t2 = st.tabs(["💎 Assinaturas", "⏱️ Uso Avulso"])
        with t1:
            cols = st.columns(3)
            for i, (nome, d) in enumerate(PLANOS.items()):
                with cols[i]:
                    st.markdown(f"### {nome}
**{d['preco']}**")
                    st.button(f"Assinar {nome}", key=f"plan_{i}")
        with t2:
            st.write("Agende seu acesso por apenas **R$ 25,00/hora**.")
            st.date_input("Escolha o dia")
            st.button("Confirmar Agendamento via Pix")

    # --- ABA 4: ÁREA DO DONO ---
    elif aba == "🔐 Área do Dono":
        st.title("🔐 Painel Administrativo do Proprietário")
        sm = st.text_input("Senha Mestra", type="password")
        if sm == SENHA_MESTRA_DONO:
            st.success("Acesso Autorizado")
            st.metric("Receita Recorrente (MRR)", "R$ 4.500,00")
            if st.button("Gerar Balões de Comemoração"): st.balloons()
        else: st.warning("Aguardando senha mestra...")

    # --- ABA 5: SUPORTE IA ---
    elif aba == "💬 Suporte IA":
        st.title("💬 Chat com Especialista IA")
        p = st.chat_input("Pergunte algo sobre seus dados...")
        if p:
            with st.chat_message("assistant"): st.write("Com base nos dados, sua empresa está saudável, mas os custos logísticos podem ser reduzidos em 5%.")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- MANUAL ---
with st.expander("📖 Manual v32.0 - Império Cars"):
    st.write("Sistema completo com Monetização, IA e Trava de Segurança.")
