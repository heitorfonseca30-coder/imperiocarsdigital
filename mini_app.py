st.set_page_config(page_title="Imperio BI v41.6")

def make_hash(p): return hashlib.sha256(str.encode(p)).hexdigest()

if 'db' not in st.session_state: st.session_state.db = {"Empresa_Alpha": make_hash("Alpha@2026")}

if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged: st.title("Imperio Cars Digital") u = st.text_input("Usuario") p = st.text_input("Senha", type="password") if st.button("Entrar"): if u in st.session_state.db and make_hash(p) == st.session_state.db[u]: st.session_state.logged = True st.rerun() else: st.error("Erro") else: st.title("Dashboard Ativo") st.write("Bem-vindo ao seu portal de BI.") df = pd.DataFrame({"Vendas": [10, 20, 30], "Lucro": [5, 10, 15]}) st.bar_chart(df) if st.sidebar.button("Sair"): st.session_state.logged = False st.rerun()

finish view
