CONFIGURACOES INICIAIS
st.set_page_config(page_title="Imperio BI v41.2", layout="wide")

st.markdown("""

.stApp { background-color: #f0f2f6; }
.stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; }
.stButton>button { width: 100%; border-radius: 10px; background-color: #1E3A8A; color: white; font-weight: bold; height: 3.5em; }
</style>
""", unsafe_allow_html=True)

SEGURANCA
SENHA_MESTRA_DONO = "300611h@bi" def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

if 'db_usuarios' not in st.session_state: st.session_state.db_usuarios = { "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "Varejo", "webhook": ""}, "User_Teste": {"senha": gerar_hash("123"), "nicho": "Servicos", "webhook": ""} }

MOTOR DE DADOS
def gerar_dados_bi(): np.random.seed(42) datas = [datetime.now() - timedelta(days=x) for x in range(30)] itens = ['Produto A', 'Produto B', 'Produto C'] dados = [] for d in datas: for _ in range(np.random.randint(5, 10)): prod = np.random.choice(itens) v_venda = np.random.uniform(50, 100) v_custo = np.random.uniform(40, 110) # Gera lucros e prejuizos dados.append({"Data": d, "Produto": prod, "Valor": v_venda, "Custo": v_custo, "Lucro": v_venda - v_custo}) return pd.DataFrame(dados)

LOGIN
if 'logado' not in st.session_state: st.session_state.logado = False st.session_state.user = None

if not st.session_state.logado: st.title("Imperio Cars Digital - BI") u_in = st.text_input("Usuario") s_in = st.text_input("Senha", type="password") if st.button("Entrar"): if u_in in st.session_state.db_usuarios and gerar_hash(s_in) == st.session_state.db_usuarios[u_in]["senha"]: st.session_state.logado = True st.session_state.user = u_in st.rerun() else: st.error("Erro: Credenciais invalidas") else: user = st.session_state.user aba = st.sidebar.radio("Menu", ["Dashboard", "Estoque Lucrativo", "Alertas", "Dono"]) df = gerar_dados_bi()

if aba == "Dashboard":
    st.title(f"Dashboard: {user}")
    c1, c2 = st.columns(2)
    c1.metric("Vendas", f"R$ {df['Valor'].sum():,.2f}")
    c2.metric("Resultado", f"R$ {df['Lucro'].sum():,.2f}")
    st.plotly_chart(px.line(df.groupby('Data')['Valor'].sum(), title="Vendas Diarias"), use_container_width=True)

elif aba == "Estoque Lucrativo":
    st.title("Analise de Itens")
    resumo = df.groupby("Produto").agg({"Valor": "mean", "Custo": "mean", "Lucro": "sum"}).reset_index()
    resumo["Status"] = resumo["Lucro"].apply(lambda x: "LUCRO" if x > 0 else "PREJUIZO")
    st.dataframe(resumo.style.format({"Valor": "{:.2f}", "Custo": "{:.2f}", "Lucro": "{:.2f}"}), use_container_width=True)

elif aba == "Alertas":
    st.title("Configurar WhatsApp")
    wh = st.text_input("Link Webhook", value=st.session_state.db_usuarios[user]["webhook"])
    if st.button("Salvar"):
        st.session_state.db_usuarios[user]["webhook"] = wh
        st.success("Salvo com sucesso!")

elif aba == "Dono":
    st.title("Area Administrativa")
    senha_m = st.text_input("Senha Mestra", type="password")
    if senha_m == SENHA_MESTRA_DONO:
        st.success("Bem-vindo, Dono!")
        st.write("Faturamento do Mes: R$ 4.500,00")

if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()
finish view
