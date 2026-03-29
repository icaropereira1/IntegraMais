import requests
import pandas as pd
from bs4 import BeautifulSoup

PARAMETROS_ADICIONAIS = {
    "ifood":          "id_item_cardapio",
    "accon":          "id_produto",
    "anotaai":        "id_produto",
    "delivery_direto":"id_produto",
    "nnfood":         "id_item_cardapio",
    "cardapioWeb":    "id_produto",
    "keeta":          "id_item_cardapio",
}

def formatar_codigo_produto(codigo, delivery):
    if delivery == "nnfood":
        return f"item_{codigo}"
    return codigo

def formatar_codigo_opcional(codigo, delivery):
    if delivery == "nnfood":
        return f"ad_{codigo}"
    return codigo

def logar_vuca(login, senha, instancia, id_unidade, delivery):
    url_login = f"https://{instancia}.vucasolution.com.br/retaguarda/"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR,pt;q=0.9"})
    session.get(f"{url_login}login.php")
    r = session.post(f"{url_login}usuarios/login.php", data={
        "auth_login": login, "auth_senha": senha,
        "url": f"/retaguarda/pg_aplicativos_cardapio_{delivery}.php?csv=1&form=1&id_unidade={id_unidade}"
    }, allow_redirects=True)
    
    if r.status_code != 200:
        raise Exception("Falha no login. Verifique as credenciais e tente novamente.")
    
    return session, url_login

def extrair_detalhes_adicionais(session, url_base, id_item, delivery, id_unidade):
    param = PARAMETROS_ADICIONAIS.get(delivery, "id_produto")

    if delivery == "cardapioWeb":
        url_ajax = f"{url_base}pg_aplicativos_cardapio_{delivery}.php?ajax=listarAdicionais&id_unidade={id_unidade}&{param}={id_item}"
    else:
        url_ajax = f"{url_base}pg_aplicativos_cardapio_{delivery}.php?ajax=listarAdicionais&{param}={id_item}"

    response = session.get(url_ajax)

    soup_ajax = BeautifulSoup(response.content, "html.parser")

    adicionais = []

    grupos = soup_ajax.find_all("fieldset", class_="box-registros")

    for grupo in grupos:
        nome_grupodeopcionais_sem_formatacao = grupo.find("legend")
        nome_grupodeopcionais_formatado = nome_grupodeopcionais_sem_formatacao.text.strip() if nome_grupodeopcionais_sem_formatacao else "Grupo de Opcionais Desconecido"

        tbody = grupo.find("tbody")
        if not tbody:continue                
        linhas_opcionais = tbody.find_all("tr")


        for tr in linhas_opcionais:
            colunas = tr.find_all("td")
            if len(colunas) >= 2:
                nome_opcional = colunas[0].get_text(strip=True)
                codigo_pdv_opcional = colunas[1].get_text(strip=True)
                
            adicionais.append({
            "nivel": "COMPLEMENTO",
            "categoria_grupoopcionais": nome_grupodeopcionais_formatado,
            "nome": nome_opcional,
            "codigo_pdv": codigo_pdv_opcional
            })           
    return adicionais

def extrair_cardapio_vuca(session, url_login, id_unidade, delivery):
    soup = BeautifulSoup(session.get(f"{url_login}pg_aplicativos_cardapio_{delivery}.php?csv=1&form=1&id_unidade={id_unidade}").content, "html.parser")
    itens = []
    categorias = []

    for row in soup.find_all("tr", class_=lambda x: x and "js-categorias" in x):
        
        categoria_id = row.get("data-id_categoria")

        legend_categoria_sem_formatacao = row.find ("legend")
        nome_categoria = legend_categoria_sem_formatacao.text.strip() if legend_categoria_sem_formatacao else None
        
        categorias.append({
        "id_categoria": categoria_id,
        "nome_categoria": nome_categoria
    })
    
    categoria_map = {categoria["id_categoria"]: categoria["nome_categoria"] for categoria in categorias}

    for row in soup.find_all("tr", class_=lambda x: x and "js-tr-" in x):
        item_vuca_id = row.get("data-id")

        # extraindo informações do item
        edita_vuca_semformatacao = row.get("class")
        codigo_edita_formatado = edita_vuca_semformatacao[0].replace("js-tr-", "")

        nome_item_vuca_semformatacao = row.find("td", {"data-th": "Produto"})
        nome_item_formatado = nome_item_vuca_semformatacao.text.strip() if nome_item_vuca_semformatacao else None

        codigopdv_item_vuca_semformatacao = row.find("td", {"data-th": "Código PDV"})
        pdvtemp = codigopdv_item_vuca_semformatacao.find("input") if codigopdv_item_vuca_semformatacao else None
        codigopdv_item_formatado = pdvtemp.get("value") if pdvtemp else None

        id_categoria_do_item_vuca = row.get("data-id_categoria")

        itens.append({
        "Nível": "PRODUTO",
        "Categoria": categoria_map.get(id_categoria_do_item_vuca, "Categoria Desconhecida"),
        "Produto Pai": nome_item_formatado,
        "Grupo de opcionais": "",
        "Item / Opcional": nome_item_formatado,
        "Código PDV": formatar_codigo_produto(codigopdv_item_formatado, delivery),
        "Link": f"{url_login}pg_produtos.php?form=1&edita={codigo_edita_formatado}"
        })

        id_para_adicionais = codigopdv_item_formatado if delivery in ["ifood","nnfood", "keeta"] else item_vuca_id

        lista_opcionais = extrair_detalhes_adicionais(session, url_login, id_para_adicionais, delivery, id_unidade)

        for opcional in lista_opcionais:
            itens.append({
            "Nível": "COMPLEMENTO",
            "Categoria": categoria_map.get(id_categoria_do_item_vuca, "Categoria Desconhecida"),
            "Produto Pai": nome_item_formatado,
            "Grupo de opcionais": opcional["categoria_grupoopcionais"],
            "Item / Opcional": opcional["nome"],
            "Código PDV": formatar_codigo_opcional(opcional["codigo_pdv"], delivery),
            "Link": f"{url_login}pg_produtos.php?form=1&edita={opcional['codigo_pdv']}"
            })

    df_temp = pd.DataFrame(itens)
    
    # Lógica de ordenação unificada
    df_temp['Sort_Key'] = df_temp['Código PDV']
    if delivery == "nnfood":
        # Para nnfood, extraímos o número de "item_123" ou "ad_123" para ordenação natural
        df_temp['Sort_Key'] = df_temp['Código PDV'].str.extract(r'(\d+)').astype(float)
    else:
        # Para outras plataformas, convertemos para numérico conforme comportamento original
        df_temp['Sort_Key'] = pd.to_numeric(df_temp['Código PDV'], errors='coerce')
        df_temp['Código PDV'] = df_temp['Sort_Key']

    # Criando referência do produto para agrupar complementos logo abaixo de seus respectivos produtos
    df_temp['PDV_Referencia'] = df_temp['Sort_Key'].where(df_temp['Nível'] == 'PRODUTO')
    df_temp['PDV_Referencia'] = df_temp.groupby(df_temp['Nível'].eq('PRODUTO').cumsum())['PDV_Referencia'].ffill()

    # Ordenando por: Referência do Produto (Crescente), Nível (Produto antes de Complemento), e Código PDV (Crescente)
    df_temp = df_temp.sort_values(by=['PDV_Referencia', 'Nível', 'Sort_Key'], ascending=[True, False, True])
    
    # Removendo colunas auxiliares
    df_temp = df_temp.drop(columns=['PDV_Referencia', 'Sort_Key'])
    
    return df_temp.to_dict('records')