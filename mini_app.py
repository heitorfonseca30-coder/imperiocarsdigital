st.set_page_config(page_title="Imperio BI v41.3", layout="wide")

st.markdown("""

.stApp { background-color: #f0f2f6; }
.stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; }
.stButton>button { width: 100%; border-radius: 10px; background-color: #1E3A8A; color: white; font-weight: bold; height: 3.5em; }
</style>
""", unsafe_allow_html=True)

MASTER_PASSWORD = "300611h@bi" def make_hash(p): return hashlib.sha256(str.encode(p)).hexdigest()

if 'db' not in st.session_state: st.session_state.db = { "Empresa_Alpha": {"pw": make_hash("Alpha@2026"), "nicho": "Varejo", "wh": ""}, "User_Teste": {"pw": make_hash("123"), "nicho": "Servicos", "wh": ""} }

def get_data(): np.random.seed(42) days = [datetime.now() - timedelta(days=x) for x in range(30)] prods = ['Produto A', 'Produto B', 'Produto C'] rows = [] for d in days: for _ in range(np.random.randint(5, 10)): p = np.random.choice(prods) v = np.random.uniform(50, 100) c = np.random.uniform(40, 110) rows.append({"Data": d, "Produto": p, "Valor": v, "Custo": c, "Lucro": v - c}) return pd.DataFrame(rows)

if 'logged' not in st.session_state: st.session_state.logged = False st.session_state.user = None

if not st.session_state.logged: st.title("Imperio Cars Digital - BI") u = st.text_input("Usuario") p = st.text_input("Senha", type="password") if st.button("Entrar"): if u in st.session_state.db and make_hash(p) == st.session_state.db[u]["pw"]: st.session_state.logged = True st.session_state.user = u st.rerun() else: st.error("Erro: Credenciais invalidas") else: u = st.session_state.user menu = st.sidebar.radio("Menu", ["Dashboard", "Estoque", "Alertas", "Dono"]) df = get_data()

if menu == "Dashboard":
    st.title(f"Dashboard: {u}")
    c1, c2 = st.columns(2)
    c1.metric("Vendas", f"R$ {df['Valor'].sum():,.2f}")
    c2.metric("Lucro", f"R$ {df['Lucro'].sum():,.2f}")
    st.plotly_chart(px.line(df.groupby('Data')['Valor'].sum(), title="Vendas Diarias"), use_container_width=True)

elif menu == "Estoque":
    st.title("Analise de Itens")
    res = df.groupby("Produto").agg({"Valor": "mean", "Custo": "mean", "Lucro": "sum"}).reset_index()
    res["Status"] = res["Lucro"].apply(lambda x: "LUCRO" if x > 0 else "PREJUIZO")
    st.dataframe(res.style.format({"Valor": "{:.2f}", "Custo": "{:.2f}", "Lucro": "{:.2f}"}), use_container_width=True)

elif menu == "Alertas":
    st.title("WhatsApp")
    hook = st.text_input("Webhook", value=st.session_state.db[u]["wh"])
    if st.button("Salvar"):
        st.session_state.db[u]["wh"] = hook
        st.success("Salvo!")

elif menu == "Dono":
    st.title("Admin")
    sp = st.text_input("Senha Mestra", type="password")
    if sp == MASTER_PASSWORD:
        st.success("Acesso Autorizado")
        st.write("Faturamento SaaS: R$ 4.500,00")

if st.sidebar.button("Sair"):
    st.session_state.logged = False
    st.rerun()
finish view
