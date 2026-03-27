=================================================================
DESIGN E ESTETICA PREMIUM (EDICAO IMPERIO CARS)
=================================================================
st.set_page_config(page_title="Imperio Cars Digital - Portal BI v41.1", layout="wide", page_icon="*")

st.markdown("""

.stApp { background-color: #f0f2f6; }
.stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; }
.stButton>button { width: 100%; border-radius: 10px; background-color: #1E3A8A; color: white; font-weight: bold; height: 3.5em; }
.sidebar .sidebar-content { background: #1E3A8A; color: white; }
.status-badge { padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

=================================================================
SEGURANCA E ACESSO
=================================================================
SENHA_MESTRA_DONO = "300611h@bi" def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

if 'db_usuarios' not in st.session_state: st.session_state.db_usuarios = { "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "Supermercado", "vencimento": datetime.now() + timedelta(hours=2), "webhook_cliente": ""}, "User_Teste": {"senha": gerar_hash("123"), "nicho": "Restaurante", "vencimento": datetime.now() + timedelta(minutes=30), "webhook_cliente": ""} }

=================================================================
MOTOR DE DADOS (BI + INTELIGENCIA DE PRODUTO)
=================================================================
def gerar_dados_bi(nicho): np.random.seed(42) datas = [datetime.now() - timedelta(days=x) for x in range(30)] itens = ['Arroz 5kg', 'Feijao 1kg', 'Oleo de Soja', 'Carne Alcatra', 'Leite Integral', 'Pao Frances'] dados = [] for d in datas: for _ in range(np.random.randint(5, 12)): prod = np.random.choice(itens) custo_base = 25.0 if prod == 'Carne Alcatra' else 8.0 venda_base = 22.0 if prod == 'Carne Alcatra' else 12.0 v_venda = venda_base * np.random.uniform(0.95, 1.1) v_custo = custo_base * np.random.uniform(0.98, 1.05) dados.append({ "Data": d, "Produto": prod, "Valor": v_venda, "Custo": v_custo, "Lucro": v_venda - v_custo, "Vendedor": "Equipe" }) return pd.DataFrame(dados)

def analisar_rentabilidade(df_vendas): resumo = df_vendas.groupby("Produto").agg({ "Valor": "mean", "Custo": "mean", "Lucro": "sum" }).reset_index() resumo["Status"] = resumo["Lucro"].apply(lambda x: "LUCRO" if x > 0 else "PREJUIZO") resumo["Margem (%)"] = ((resumo["Valor"] - resumo["Custo"]) / resumo["Valor"]) * 100 return resumo

=================================================================
FLUXO DE NAVEGACAO
=================================================================
if 'logado' not in st.session_state: st.session_state.logado = False st.session_state.user = None

if not st.session_state.logado: st.title("Imperio Cars Digital - Portal de BI") u_in = st.text_input("Usuario") s_in = st.text_input("Senha", type="password") if st.button("Entrar"): if u_in in st.session_state.db_usuarios and gerar_hash(s_in) == st.session_state.db_usuarios[u_in]["senha"]: st.session_state.logado = True st.session_state.user = u_in st.rerun() else: st.error("Credenciais Invalidas") else: user = st.session_state.user aba = st.sidebar.radio("Navegacao", ["Dashboard Geral", "Estoque e Lucratividade", "Central de Alertas", "Area do Dono"])

df_vendas = gerar_dados_bi(st.session_state.db_usuarios[user]["nicho"])
df_lucro_prod = analisar_rentabilidade(df_vendas)

if aba == "Dashboard Geral":
    st.title(f"Dashboard: {user}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento", f"R$ {df_vendas['Valor'].sum():,.2f}")
    c2.metric("Lucro Liquido", f"R$ {df_vendas['Lucro'].sum():,.2f}")
    c3.metric("Ticket Medio", f"R$ {df_vendas['Valor'].mean():,.2f}")
    st.plotly_chart(px.bar(df_lucro_prod, x="Produto", y="Lucro", color="Status", 
                          title="Lucratividade por Item",
                          color_discrete_map={"LUCRO": "#10b981", "PREJUIZO": "#ef4444"}), use_container_width=True)

elif aba == "Estoque e Lucratividade":
    st.title("Gestao de Estoque e Inteligencia de Lucro")
    prejuizo_count = len(df_lucro_prod[df_lucro_prod["Lucro"] < 0])
    col_k1, col_k2 = st.columns(2)
    col_k1.metric("Produtos Monitorados", len(df_lucro_prod))
    col_k2.metric("Itens no Prejuizo", prejuizo_count, delta="- Critico" if prejuizo_count > 0 else None, delta_color="inverse")
    st.dataframe(df_lucro_prod.style.format({"Valor": "R$ {:.2f}", "Custo": "R$ {:.2f}", "Lucro": "R$ {:.2f}", "Margem (%)": "{:.1f}%"}), use_container_width=True)

elif aba == "Central de Alertas":
    st.title("Notificacoes Automaticas")
    webhook = st.text_input("Seu Webhook do WhatsApp", value=st.session_state.db_usuarios[user]["webhook_cliente"])
    if st.button("Salvar"):
        st.session_state.db_usuarios[user]["webhook_cliente"] = webhook
        st.success("Configuracao atualizada!")

elif aba == "Area do Dono":
    st.title("Painel Administrativo")
    sm = st.text_input("Senha Mestra", type="password")
    if sm == SENHA_MESTRA_DONO:
        st.success("Acesso Autorizado")
        st.write("Faturamento SaaS: R$ 4.500,00")
    else: st.warning("Digite a senha...")

if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()
finish view
