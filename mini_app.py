=================================================================
 DESIGN & ESTÉTICA PREMIUM (EDIÇÃO IMPÉRIO CARS)
=================================================================
st.set_page_config(page_title="Império Cars Digital - Portal BI v41.0", layout="wide", page_icon="🏎️")

st.markdown("""

.stApp { background-color: #f0f2f6; }
.stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1E3A8A; }
.stButton>button { width: 100%; border-radius: 10px; background-color: #1E3A8A; color: white; font-weight: bold; height: 3.5em; }
.sidebar .sidebar-content { background: #1E3A8A; color: white; }
.status-badge { padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

=================================================================
 SEGURANÇA E ACESSO
=================================================================
SENHA_MESTRA_DONO = "300611h@bi" def gerar_hash(senha): return hashlib.sha256(str.encode(senha)).hexdigest()

if 'db_usuarios' not in st.session_state: st.session_state.db_usuarios = { "Empresa_Alpha": {"senha": gerar_hash("Alpha@2026"), "nicho": "🛒 Supermercado", "vencimento": datetime.now() + timedelta(hours=2), "webhook_cliente": ""}, "User_Teste": {"senha": gerar_hash("123"), "nicho": "🍔 Restaurante", "vencimento": datetime.now() + timedelta(minutes=30), "webhook_cliente": ""} }

=================================================================
 MOTOR DE DADOS (BI + INTELIGÊNCIA DE PRODUTO)
=================================================================
def gerar_dados_bi(nicho): np.random.seed(42) datas = [datetime.now() - timedelta(days=x) for x in range(30)] itens = ['Arroz 5kg', 'Feijão 1kg', 'Óleo de Soja', 'Carne Alcatra', 'Leite Integral', 'Pão Francês'] dados = [] for d in datas: for _ in range(np.random.randint(5, 12)): prod = np.random.choice(itens) # Simulação de margens variadas (incluindo prejuízo proposital para demonstração) custo_base = 25.0 if prod == 'Carne Alcatra' else 8.0 venda_base = 22.0 if prod == 'Carne Alcatra' else 12.0 # Prejuízo na carne proposital

        v_venda = venda_base * np.random.uniform(0.95, 1.1)
        v_custo = custo_base * np.random.uniform(0.98, 1.05)
        
        dados.append({
            "Data": d, "Produto": prod, "Valor": v_venda, 
            "Custo": v_custo, "Lucro": v_venda - v_custo, "Vendedor": "Equipe"
        })
return pd.DataFrame(dados)
def analisar_rentabilidade(df_vendas): resumo = df_vendas.groupby("Produto").agg({ "Valor": "mean", "Custo": "mean", "Lucro": "sum" }).reset_index()

resumo["Status"] = resumo["Lucro"].apply(lambda x: "🟢 LUCRO" if x > 0 else "🔴 PREJUÍZO")
resumo["Margem (%)"] = ((resumo["Valor"] - resumo["Custo"]) / resumo["Valor"]) * 100
return resumo
=================================================================
🖥️ FLUXO DE NAVEGAÇÃO
=================================================================
if 'logado' not in st.session_state: st.session_state.logado = False st.session_state.user = None

if not st.session_state.logado: st.title("🏎️ Império Cars Digital - Portal BI v41.0") u_in = st.text_input("Usuário") s_in = st.text_input("Senha", type="password") if st.button("Entrar"): if u_in in st.session_state.db_usuarios and gerar_hash(s_in) == st.session_state.db_usuarios[u_in]["senha"]: st.session_state.logado = True st.session_state.user = u_in st.rerun() else: st.error("❌ Credenciais Inválidas") else: user = st.session_state.user aba = st.sidebar.radio("Navegação", ["📊 Dashboard Geral", "📦 Estoque & Lucratividade", "🔔 Central de Alertas", "🔐 Área do Dono"])

df_vendas = gerar_dados_bi(st.session_state.db_usuarios[user]["nicho"])
df_lucro_prod = analisar_rentabilidade(df_vendas)

# --- DASHBOARD ---
if aba == "📊 Dashboard Geral":
    st.title(f"📊 Dashboard: {user}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento", f"R$ {df_vendas['Valor'].sum():,.2f}")
    c2.metric("Lucro Líquido", f"R$ {df_vendas['Lucro'].sum():,.2f}")
    c3.metric("Ticket Médio", f"R$ {df_vendas['Valor'].mean():,.2f}")
    
    st.plotly_chart(px.bar(df_lucro_prod, x="Produto", y="Lucro", color="Status", 
                          title="Lucratividade Bruta por Item (30 dias)",
                          color_discrete_map={"🟢 LUCRO": "#10b981", "🔴 PREJUÍZO": "#ef4444"}), use_container_width=True)

# --- ESTOQUE & LUCRATIVIDADE (NOVA FUNÇÃO) ---
elif aba == "📦 Estoque & Lucratividade":
    st.title("📦 Gestão de Estoque e Inteligência de Lucro")
    st.write("Descubra quais produtos do seu estoque estão gerando lucro real ou trazendo prejuízo financeiro.")
    
    # Filtros e KPI Rápidos
    col_k1, col_k2 = st.columns(2)
    prejuizo_count = len(df_lucro_prod[df_lucro_prod["Lucro"] < 0])
    col_k1.metric("Produtos Monitorados", len(df_lucro_prod))
    col_k2.metric("Itens no Prejuízo", prejuizo_count, delta="- Crítico" if prejuizo_count > 0 else None, delta_color="inverse")

    st.markdown("---")
    
    # Filtro de Tabela
    filtro = st.selectbox("Filtrar Visão:", ["Todos os Itens", "Apenas Itens com Prejuízo", "Apenas Itens com Lucro"])
    if filtro == "Apenas Itens com Prejuízo": exibir_df = df_lucro_prod[df_lucro_prod["Lucro"] < 0]
    elif filtro == "Apenas Itens com Lucro": exibir_df = df_lucro_prod[df_lucro_prod["Lucro"] > 0]
    else: exibir_df = df_lucro_prod

    # Formatação Visual da Tabela
    st.dataframe(exibir_df.style.format({
        "Valor": "R$ {:.2f}", "Custo": "R$ {:.2f}", "Lucro": "R$ {:.2f}", "Margem (%)": "{:.1f}%"
    }).applymap(lambda x: 'color: #ef4444; font-weight: bold' if isinstance(x, str) and "🔴" in x 
                else 'color: #10b981; font-weight: bold' if isinstance(x, str) and "🟢" in x else '', subset=["Status"]), use_container_width=True)

    if prejuizo_count > 0:
        st.error(f"⚠️ Alerta Estratégico: O produto '{df_lucro_prod.sort_values('Lucro').iloc[0]['Produto']}' é o que mais gera prejuízo. Revise o preço de venda imediatamente.")
    else:
        st.success("✅ Parabéns! Toda a sua linha de produtos está operando com lucro.")

# --- CENTRAL DE ALERTAS ---
elif aba == "🔔 Central de Alertas":
    st.title("🔔 Notificações Automáticas")
    webhook = st.text_input("Seu Webhook do WhatsApp", value=st.session_state.db_usuarios[user]["webhook_cliente"])
    if st.button("Salvar"):
        st.session_state.db_usuarios[user]["webhook_cliente"] = webhook
        st.success("Configuração atualizada!")

# --- ÁREA DO DONO ---
elif aba == "🔐 Área do Dono":
    st.title("🔐 Painel Administrativo")
    sm = st.text_input("Senha Mestra", type="password")
    if sm == SENHA_MESTRA_DONO:
        st.success("Acesso Autorizado")
        st.write("Faturamento SaaS: R$ 4.500,00")
    else: st.warning("Digite a senha...")

if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()
finish view
