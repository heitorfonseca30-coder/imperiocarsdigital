def instalar_dependencias(): pacotes = ["streamlit", "pandas", "numpy", "plotly"] for pacote in pacotes: try: import(pacote) except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar_dependencias()

import streamlit as st import pandas as pd import numpy as np import plotly.express as px import hashlib from datetime import datetime, timedelta

=================================================================
🛡️ CONFIGURAÇÕES DE SEGURANÇA E ACESSO (Sua Senha Mestra)
=================================================================
SENHA_MESTRA_DONO = "300611h@bi"

def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

Banco de Dados de Usuários (SaaS Multitenancy)
usuarios_db = { "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2)}, "Empresa_Beta": {"senha": gerar_hash("Beta@2026"), "nicho": "💊 Farmácia", "vencimento": datetime.now() - timedelta(hours=1)}, "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30)} }

=================================================================
🚀 MOTOR DE DADOS E SIMULAÇÃO (PITCH DE VENDAS)
=================================================================
@st.cache_data def gerar_dados(nicho, is_demo=False): np.random.seed(42 if not is_demo else None) datas = [datetime.now() - timedelta(days=x) for x in range(30)]

configs = {
    "🛒 Supermercado": (['Arroz', 'Feijão', 'Leite', 'Carne'], [28.0, 9.0, 5.0, 45.0]),
    "💊 Farmácia": (['Amoxicilina', 'Dipirona', 'Vitamina C', 'Fraldas'], [50.0, 6.0, 25.0, 60.0]),
    "🍔 Restaurante": (['Prato Feito', 'Burger', 'Cerveja', 'Suco'], [32.0, 38.0, 12.0, 10.0]),
    "🚗 Oficina": (['Troca Óleo', 'Revisão', 'Pastilha', 'Mão de Obra'], [220.0, 500.0, 280.0, 180.0])
}

itens, precos = configs.get(nicho, (['Item Genérico'], [10.0]))
dados = []
for d in datas:
    for _ in range(np.random.randint(5, 15)):
        idx = np.random.randint(0, len(itens))
        val = precos[idx] * np.random.uniform(0.9, 1.1)
        dados.append({
            "Data": d, "Produto": itens[idx], "Valor": val,
            "Custo": val * 0.65, "Vendedor": np.random.choice(["Marcos", "Ana", "Carlos"])
        })
return pd.DataFrame(dados)
=================================================================
🖥️ INTERFACE DO PORTAL BI (SaaS v31.0)
=================================================================
st.set_page_config(page_title="Portal BI SaaS v31.0", layout="wide", page_icon="📊")

if 'logado' not in st.session_state: st.session_state.logado = False st.session_state.user = None

--- TELA DE LOGIN ---
if not st.session_state.logado: st.title("📊 Portal BI SaaS - Login Seguro") col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Acesso do Cliente")
    u = st.text_input("Usuário da Empresa")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar no Sistema"):
        if u in usuarios_db and gerar_hash(p) == usuarios_db[u]["senha"]:
            st.session_state.logado = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("❌ Usuário ou Senha incorretos.")

with col2:
    st.info("💡 **DICA DO DONO:** Para demonstrações rápidas, use sua Senha Mestra na Área do Dono no menu lateral.")
--- SISTEMA APÓS LOGIN ---
else: user = st.session_state.user dados_u = usuarios_db[user] agora = datetime.now()

# --- TRAVA DE EXPIRAÇÃO (SEGURANÇA TEMPORAL) ---
if agora > dados_u["vencimento"]:
    st.error(f"🛑 ACESSO EXPIRADO: Seu plano encerrou em {dados_u['vencimento'].strftime('%d/%m %H:%M')}")
    st.warning("Renove sua assinatura para continuar visualizando os dados.")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()
    st.stop()

# --- MENU LATERAL ---
st.sidebar.header(f"🏢 {user}")
tempo_rest = dados_u["vencimento"] - agora
st.sidebar.info(f"⏳ Tempo Restante: {tempo_rest.seconds // 60} minutos")

menu = st.sidebar.radio("Navegação", [
    "📊 Dashboard Geral", 
    "💰 Lucratividade Real", 
    "💡 Dicas de Especialista", 
    "💳 Planos & Pagamentos",
    "💬 Suporte IA",
    "🔐 Área do Dono (Admin)"
])

df = gerar_dados(dados_u["nicho"])

# --- ABAS DO SISTEMA ---
if menu == "📊 Dashboard Geral":
    st.title(f"📊 Gestão Inteligente: {dados_u['nicho']}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Vendas (30d)", f"R$ {df['Valor'].sum():,.2f}", "+8.5%")
    m2.metric("Ticket Médio", f"R$ {df['Valor'].mean():,.2f}")
    m3.metric("Lucro Líquido", f"R$ {(df['Valor'].sum()-df['Custo'].sum()):,.2f}", "🔥")
    
    fig = px.bar(df.groupby("Vendedor")["Valor"].sum().reset_index(), x="Vendedor", y="Valor", title="Ranking de Vendedores")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "💰 Lucratividade Real":
    st.title("💰 Onde está o seu dinheiro?")
    df['Lucro'] = df['Valor'] - df['Custo']
    resumo = df.groupby("Produto")[["Valor", "Custo", "Lucro"]].sum().sort_values(by="Lucro", ascending=False)
    st.dataframe(resumo.style.format("R$ {:.2f}"), use_container_width=True)
    st.plotly_chart(px.pie(df, values='Lucro', names='Produto', title='Distribuição de Lucro por Produto'))

elif menu == "💡 Dicas de Especialista":
    st.title("💡 Consultoria Estratégica Automática")
    top_prod = df.groupby("Produto")["Valor"].sum().idxmax()
    st.success(f"📌 **Dica de Ouro:** O item '{top_prod}' é seu carro-chefe. Crie um combo com o item menos vendido para girar estoque!")
    st.info("🚀 **Estratégia:** Seus custos estão em 65%. Reduza 5% na logística para aumentar seu lucro anual em R$ 12.000,00.")

elif menu == "💳 Planos & Pagamentos":
    st.title("💳 Gestão de Assinatura")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Plano Bronze (R$ 199/mês)"); st.write("Relatórios Básicos")
    with c2: st.button("Plano Prata (R$ 399/mês)"); st.write("BI + Alertas WhatsApp")
    with c3: st.button("Plano Ouro (R$ 799/mês)"); st.write("IA + Consultoria VIP")
    st.divider()
    st.write("📅 **Agendamento por Hora:** R$ 50,00 por acesso avulso.")

elif menu == "💬 Suporte IA":
    st.title("💬 Chatbot de Suporte Técnico")
    msg = st.chat_input("Como posso ajudar?")
    if msg:
        with st.chat_message("assistant"):
            st.write(f"Olá! Sou a IA do Portal BI. Analisando sua conta {user}, vi que você está próximo do limite de faturamento do plano atual. Deseja fazer um upgrade?")

elif menu == "🔐 Área do Dono (Admin)":
    st.title("🔐 Painel do Proprietário (SaaS)")
    s_mestra = st.sidebar.text_input("Senha Mestra Administrativa", type="password")
    
    if s_mestra == SENHA_MESTRA_DONO:
        st.success("Acesso Admin Liberado!")
        st.subheader("💰 Meu Faturamento Direto")
        d1, d2 = st.columns(2)
        d1.metric("Total Acumulado", "R$ 12.540,00", "+R$ 1.200 hoje")
        d2.metric("Assinantes Ativos", "24 empresas", "Meta: 50")
        
        st.divider()
        st.subheader("🚀 Modo Demonstração (Simulador de Vendas)")
        n_demo = st.selectbox("Simular qual comércio?", ["🛒 Supermercado", "💊 Farmácia", "🍔 Restaurante", "🚗 Oficina"])
        if st.button("Ativar Demonstração em Tempo Real"):
            st.balloons()
            st.session_state.demo_ativa = True
            st.info(f"Simulação de '{n_demo}' ativa para apresentação ao cliente!")
    else:
        st.warning("Insira a Senha Mestra correta no menu lateral para ver seus ganhos.")

# Botão Sair
if st.sidebar.button("Encerrar Sessão"):
    st.session_state.logado = False
    st.rerun()
=================================================================
📖 MANUAL E CHANGELOG v31.0
=================================================================
with st.expander("📖 Manual do Sistema & Changelog v31.0"): st.write(f""" Histórico de Versões: - v31.0 (ATUAL): Consolidação Total (Segurança + IA + Pagamentos + Simulador + Trava). [CITE:turn75file1] - v30.0: Correção de erro de instalação automática (ModuleNotFoundError). [CITE:turn73file1] - v29.0: Bloco mestre otimizado para Replit/Desktop. [CITE:turn68file1]

**Seus Acessos:**
- Sua Senha Mestra: `{SENHA_MESTRA_DONO}` [CITE:turn61file3]
- Usuário Teste: `User_Teste` | Senha: `123` [CITE:turn68file1]
""")
finish view
