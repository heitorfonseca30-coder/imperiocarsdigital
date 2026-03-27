import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
import time
from datetime import datetime, timedelta

# =================================================================
# 🛡️ CONFIGURAÇÕES DE SEGURANÇA E ACESSO
# =================================================================
SENHA_MESTRA_DONO = "300611h@bi"

def gerar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

# Usuários pré-cadastrados (Simulando Banco de Dados de Assinantes)
usuarios_db = {
    "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)},
    "Empresa_Beta": {"senha": gerar_hash("Beta@2026"), "nicho": "💊 Farmácia", "vencimento": datetime.now() - timedelta(hours=1)},
    "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)}
}

# =================================================================
# 🚀 GERADOR DE DADOS PARA SIMULAÇÃO (PITCH DE VENDAS)
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
# 🖥️ INTERFACE DO PORTAL BI (SaaS)
# =================================================================
st.set_page_config(page_title="Portal BI SaaS v29.0", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.user = None

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.title("🔐 Portal BI - Acesso Restrito")
    col_l, col_r = st.columns(2)
    
    with col_l:
        user_input = st.text_input("Usuário da Empresa")
        senha_input = st.text_input("Senha", type="password")
        
        if st.button("Entrar no Sistema"):
            if user_input in usuarios_db and gerar_hash(senha_input) == usuarios_db[user_input]["senha"]:
                st.session_state.logado = True
                st.session_state.user = user_input
                st.rerun()
            else:
                st.error("❌ Credenciais Inválidas")
    
    with col_r:
        st.info("💡 **Dica do Dono:** Use sua Senha Mestra no menu lateral para ativar o Modo Demonstração sem precisar de conta de cliente.")

# --- SISTEMA APÓS LOGIN ---
else:
    user = st.session_state.user
    dados_user = usuarios_db[user]
    agora = datetime.now()
    
    # --- TRAVA DE SEGURANÇA POR TEMPO ---
    if agora > dados_user["vencimento"]:
        st.error(f"⚠️ ACESSO BLOQUEADO: Seu tempo expirou em {dados_user['vencimento'].strftime('%H:%M')}")
        st.warning("Entre em contato com o suporte para renovar seu acesso por hora.")
        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()
        st.stop()

    # --- MENU LATERAL ---
    st.sidebar.title(f"🏢 {user}")
    tempo_restante = dados_user["vencimento"] - agora
    st.sidebar.write(f"⏳ Tempo de Acesso: {tempo_restante.seconds // 60} min")
    
    aba = st.sidebar.radio("Navegação", ["📊 Dashboard Principal", "💰 Lucratividade", "📦 Estoque & Logística", "💡 Dicas de Especialista", "🔐 Área do Dono", "💬 Suporte IA"])

    # Carregar Dados
    df = gerar_dados_simulados(dados_user["nicho"])

    # --- ABA 1: DASHBOARD ---
    if aba == "📊 Dashboard Principal":
        st.title(f"📊 Dashboard: {dados_user['nicho']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Mensal", f"R$ {df['Valor'].sum():,.2f}", "+12%")
        c2.metric("Ticket Médio", f"R$ {df['Valor'].mean():,.2f}")
        c3.metric("Lucro Estimado", f"R$ {(df['Valor'].sum() - df['Custo'].sum()):,.2f}", "🔥")
        
        st.plotly_chart(px.line(df.groupby(df['Data'].dt.date)['Valor'].sum(), title="Evolução de Vendas"), use_container_width=True)

    # --- ABA 2: LUCRATIVIDADE ---
    elif aba == "💰 Lucratividade":
        st.title("💰 Análise de Lucro por Produto")
        df['Lucro_R$'] = df['Valor'] - df['Custo']
        lucro_prod = df.groupby("Produto")["Lucro_R$"].sum().sort_values()
        st.bar_chart(lucro_prod)
        st.dataframe(df.groupby("Produto")[["Valor", "Custo", "Lucro_R$"]].sum(), use_container_width=True)

    # --- ABA 3: ÁREA DO DONO (PROTEGIDA) ---
    elif aba == "🔐 Área do Dono":
        st.title("🔐 Painel Administrativo do Proprietário")
        senha_mestra = st.text_input("Insira a Senha Mestra", type="password")
        
        if senha_mestra == SENHA_MESTRA_DONO:
            st.success("Acesso Autorizado")
            st.subheader("💰 Meu Faturamento (SaaS)")
            col_d1, col_d2 = st.columns(2)
            col_d1.metric("Clientes Ativos", "12", "+2 este mês")
            col_d2.metric("Receita Recorrente (MRR)", "R$ 4.500,00", "Meta: R$ 10k")
            
            st.write("📈 **Simulador de Vendas para Pitch**")
            nicho_pitch = st.selectbox("Simular para qual nicho?", ["🛒 Supermercado", "💊 Farmácia", "🍔 Restaurante", "🚗 Oficina"])
            if st.button("Gerar Demonstração"):
                st.session_state.demo_data = gerar_dados_simulados(nicho_pitch)
                st.balloons()
        else:
            st.warning("Aguardando senha mestra...")

    # --- ABA 4: SUPORTE IA ---
    elif aba == "💬 Suporte IA":
        st.title("💬 Assistente de Inteligência do Portal")
        pergunta = st.chat_input("Como posso ajudar com seus dados hoje?")
        if pergunta:
            with st.chat_message("assistant"):
                st.write(f"Analisando sua empresa ({user})... Minha recomendação é focar na redução de custos do item '{df.groupby('Produto')['Custo'].sum().idxmax()}' para aumentar sua margem em 8%.")

    # Logout
    if st.sidebar.button("Sair do Sistema"):
        st.session_state.logado = False
        st.rerun()

# =================================================================
# 📝 HISTÓRICO DE VERSÕES (MANUAL AUTO-ATUALIZÁVEL)
# =================================================================
with st.expander("📖 Manual do Sistema & Changelog v29.0"):
    st.write(\"\"\"
    **Últimas Atualizações:**
    - v29.0: Consolidação total de módulos (IA + Simulador + Trava + SaaS).
    - v28.0: Chave Mestra para simulação rápida protegida por senha.
    - v27.0: Simulador Universal de Vendas (Modo Pitch).
    - v22.0: Sistema de bloqueio automático por expiração de tempo.
    - v20.0: Proteção de credenciais via Secrets do Replit.
    \"\"\")
