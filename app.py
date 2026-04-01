from datetime import datetime
import time
import streamlit as st
import pandas as pd
from utils.excel import gerar_excel_em_memoria, gerar_excel_comparativo
from services.ifood import get_token, extrair_cardapio_ifood, mapear_codigos_atuais, atualizar_item
from services.vuca import logar_vuca, extrair_cardapio_vuca
from services.comparison import compare_menus


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestor de PDV", page_icon="🍔", layout="wide")
st.title("🍔 Gestor de Códigos PDV")

# --- SIDEBAR: CREDENCIAIS VUCA ---
st.sidebar.header("🔑 Credenciais da API do iFood")
st.sidebar.markdown("Insira os dados da loja para conectar.")
client_id = st.sidebar.text_input("Client ID", type="password")
client_secret = st.sidebar.text_input("Client Secret", type="password")
merchant_id = st.sidebar.text_input("Merchant ID (ID da Loja)")

# --- SIDEBAR: CREDENCIAIS VUCA ---
st.sidebar.header("🔑 Credenciais para login no Vuca")
st.sidebar.markdown("Insira os dados da loja para conectar.")
v_instancia = st.sidebar.text_input("Instância")
v_id_unidade = st.sidebar.text_input("ID da unidade")
v_login = st.sidebar.text_input("Login")
v_senha = st.sidebar.text_input("Senha", type="password")

tab1, tab2, tab3, tab4 = st.tabs(["📥 1. Baixar planilha iFood","📤 2. Atualizar PDV's no iFood", "📥 3. Baixar planilha Vuca", "🔍 4. Comparação"])

with tab1:
    st.header("Baixar Cardápio Atual")
    st.write("Gere a planilha bloqueada contendo o cardápio atual do iFood.")
    
    if st.button("Gerar Planilha iFood"):
        if not client_id or not client_secret or not merchant_id:
            st.warning("Preencha todas as credenciais na barra lateral primeiro.")
        else:
            with st.spinner("Autenticando e montando a planilha. Aguarde..."):
                try:
                    token = get_token(client_id, client_secret)
                    if token:
                        df_cardapio = extrair_cardapio_ifood(token, merchant_id)
                        excel_data = gerar_excel_em_memoria(df_cardapio)
                        
                        data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
                        st.success("Planilha gerada com sucesso!")
                        st.download_button(
                            label="📥 Clique aqui para Baixar o Excel",
                            data=excel_data,
                            file_name=f"Cardapio_iFood_{merchant_id}_{data_str}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"Erro fatal: {e}")

with tab2:
    st.header("Atualizar Códigos PDV")
    st.write("Faça o upload da planilha editada. O sistema atualizará apenas o que foi alterado.")
    
    arquivo_upload = st.file_uploader("Selecione a planilha Excel", type=["xlsx"])
    
    if arquivo_upload is not None:
        if st.button("🚀 Iniciar Atualização no iFood"):
            if not client_id or not client_secret or not merchant_id:
                st.warning("Preencha todas as credenciais na barra lateral primeiro.")
            else:
                try:
                    token = get_token(client_id, client_secret)
                    if not token:
                        st.stop()
                        
                    st.info("📥 Baixando cardápio atual para evitar atualizações redundantes...")
                    mapa_atual = mapear_codigos_atuais(token, merchant_id)
                    
                    df = pd.read_excel(arquivo_upload, dtype={'Código PDV (externalCode)': str, 'ID iFood': str})
                    
                    pulados = 0
                    atualizados = 0
                    erros = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_linhas = len(df)
                    
                    for index, row in df.iterrows():
                        id_ifood = row['ID iFood']
                        novo_codigo = row['Código PDV (externalCode)']
                        nivel = row['Nível']
                        nome = row['Item / Opcional']
                        
                        if pd.isna(id_ifood) or pd.isna(novo_codigo) or str(novo_codigo).lower() == 'nan':
                            continue
                            
                        novo_codigo = str(novo_codigo).strip()
                        id_ifood = str(id_ifood).strip()
                    
                        
                        codigo_no_ifood = mapa_atual.get(id_ifood)
                        
                        if codigo_no_ifood == novo_codigo:
                            pulados += 1
                        else:
                            status_text.text(f"Atualizando: {nome[:70]}... ({codigo_no_ifood} ➡️ {novo_codigo})")
                            resp = atualizar_item(token, merchant_id, id_ifood, novo_codigo, nivel)
                            
                            if resp.status_code == 200:
                                mapa_atual[id_ifood] = novo_codigo
                                atualizados += 1
                            elif resp.status_code == 429:
                                st.warning("Limite da API atingido (Rate Limit). Pausando por 60 segundos...")
                                time.sleep(60)
                                resp = atualizar_item(token, merchant_id, id_ifood, novo_codigo, nivel)
                                if resp.status_code == 200:
                                    atualizados += 1
                                else:
                                    erros += 1
                            else:
                                erros += 1
                            
                            time.sleep(0.4) # Respeito ao Rate Limit do iFood
                        
                        progress_bar.progress((index + 1) / total_linhas)

                    status_text.text("Processamento concluído!")
                    st.success("✅ Atualização Finalizada!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⏭️ Pulados (Já estavam certos)", pulados)
                    col2.metric("✅ Atualizados", atualizados)
                    col3.metric("❌ Erros", erros)
                    
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")

with tab3:
    delivery = st.radio(
    "Plataforma de delivery",
    options=["ifood", "accon", "anotaai", "delivery_direto", "nnfood", "cardapioWeb", "keeta"],
    format_func=lambda x: {
        "ifood": "iFood",
        "accon": "Accon",
        "anotaai": "Anota AI",
        "delivery_direto": "Delivery Direto",
        "nnfood": "99Food",
        "cardapioWeb": "Cardápio Web",
        "keeta": "Keeta"
    }[x],
    index=0,
    horizontal=True
    )

    st.header("Baixar Planilha do Vuca")
    
    if st.button("Gerar Planilha Vuca"):
        if not v_instancia or not v_login or not v_senha or not v_id_unidade:
            st.warning("Preencha todas as credenciais na barra lateral primeiro.")
        else:
            with st.spinner("Fazendo login e extraindo informações do cardápio..."):
                try:
                    session, url_login = logar_vuca(v_login, v_senha, v_instancia, v_id_unidade, delivery)
                    st.success("Login no Vuca realizado com sucesso!")
                    itens_vuca = extrair_cardapio_vuca(session, url_login, v_id_unidade, delivery)
                    df_vuca = pd.DataFrame(itens_vuca)
                    excel_data_vuca = gerar_excel_em_memoria(df_vuca)
                    
                    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
                    st.success("Planilha do Vuca gerada com sucesso!")
                    st.download_button(
                        label="📥 Clique aqui para Baixar o Excel do Vuca",
                        data=excel_data_vuca,
                        file_name=f"Cardapio_Vuca_{delivery}_{v_id_unidade}_{data_str}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                        
                except Exception as e:
                    st.error(f"Erro ao logar no Vuca: {e}")

with tab4:
    st.header("🔍 Comparação de Cardápios")
    st.write("Compare os códigos PDV entre o VUCA e o Marketplace.")
    
    plataforma = st.selectbox(
        "Selecione a plataforma para comparar com o VUCA:",
        options=["ifood"],
        format_func=lambda x: {"ifood": "iFood"}[x]
    )
    
    if st.button("🚀 Iniciar Comparação"):
        # Verificar todas as credenciais necessárias
        if not all([client_id, client_secret, merchant_id, v_instancia, v_id_unidade, v_login, v_senha]):
            st.warning("Preencha todas as credenciais (iFood e VUCA) na barra lateral primeiro.")
        else:
            with st.spinner("Realizando comparação..."):
                try:
                    # 1. Obter cardápio iFood
                    token = get_token(client_id, client_secret)
                    if not token:
                        st.error("Falha na autenticação com iFood.")
                        st.stop()
                    df_ifood = extrair_cardapio_ifood(token, merchant_id)
                    
                    # 2. Obter cardápio VUCA
                    # Usamos a plataforma selecionada no rádio da Tab 3 ou fixa se preferir, 
                    # mas o plano sugere passar o parâmetro de delivery.
                    # Vou usar 'ifood' fixo para a comparação com ifood, ou o que estiver no radio.
                    session, url_login = logar_vuca(v_login, v_senha, v_instancia, v_id_unidade, plataforma)
                    itens_vuca = extrair_cardapio_vuca(session, url_login, v_id_unidade, plataforma)
                    df_vuca = pd.DataFrame(itens_vuca)
                    
                    # 3. Comparar
                    df_comparacao = compare_menus(df_vuca, df_ifood, mkt_name="iFood")
                    
                    # 4. Métricas e Resumo
                    total = len(df_comparacao)
                    
                    # Mapeamento para métricas simplificadas
                    # Status: "OK", "Nome Divergente", "PDV Incorreto", "Faltando no VUCA"
                    count_ok = len(df_comparacao[df_comparacao['Status'] == "OK"])
                    count_divergente = len(df_comparacao[df_comparacao['Status'].isin(["Nome Divergente", "PDV Incorreto"])])
                    count_faltando = len(df_comparacao[df_comparacao['Status'] == "Faltando no VUCA"])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total de Itens", total)
                    col2.metric("✅ OK", count_ok)
                    col3.metric("⚠️ Divergentes", count_divergente)
                    col4.metric("❌ Faltando", count_faltando)
                    
                    # 5. Download do Excel
                    excel_comparativo = gerar_excel_comparativo(df_comparacao)
                    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
                    st.download_button(
                        label="📥 Baixar Relatório de Comparação (Excel)",
                        data=excel_comparativo,
                        file_name=f"Comparacao_{plataforma}_{merchant_id}_{data_str}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # 6. Exibir Tabela (opcionalmente filtrada ou completa)
                    st.subheader("Detalhes da Comparação")
                    st.dataframe(df_comparacao, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Erro durante a comparação: {e}")
                    