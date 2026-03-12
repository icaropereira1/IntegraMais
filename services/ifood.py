import requests
import pandas as pd
from config import URL_AUTH, URL_CATALOG_BASE, URL_CATALOG_BASE_V2

def get_token(cid, csec):
    payload = {"grantType": "client_credentials", "clientId": cid, "clientSecret": csec}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(URL_AUTH, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['accessToken']
    else:
        raise Exception(f"Erro de Autenticação: {response.text}")
    
def extrair_cardapio_ifood(token, m_id):
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Busca Catálogo
    r_catalogs = requests.get(f"{URL_CATALOG_BASE}/{m_id}/catalogs", headers=headers)
    if r_catalogs.status_code != 200:
        raise Exception(f"Erro ao listar catálogos: {r_catalogs.text}")
        
    catalogs = r_catalogs.json()
    if not catalogs:
        raise Exception("Nenhum catálogo encontrado para esta loja.")
    
    catalog_id = catalogs[0]['catalogId']

    # 2. Baixa Árvore
    url_categories = f"{URL_CATALOG_BASE}/{m_id}/catalogs/{catalog_id}/categories?includeItems=true"
    r_categories = requests.get(url_categories, headers=headers)
    categories = r_categories.json()

    # 3. Processamento
    rows = []
    ids_processados = set()

    for category in categories:
        cat_name = category.get('name', 'SEM CATEGORIA')
        for item in category.get('items', []):
            prod_id = item.get('id')
            
            if prod_id not in ids_processados:
                ids_processados.add(prod_id)
                rows.append({
                    "Nível": "PRODUTO",
                    "Categoria": cat_name,
                    "Produto Pai": item.get('name'),
                    "Grupo de opcionais": "",
                    "Item / Opcional": item.get('name'),
                    "Código PDV (externalCode)": item.get('externalCode', ''),
                    "Status": item.get('status', ''),
                    "ID iFood": prod_id
                })
            
            current_prod_name = item.get('name')

            for group in item.get('optionGroups', []):
                group_name = group.get('name')
                for option in group.get('options', []):
                    opt_id = option.get('id')
                    if opt_id not in ids_processados:
                        ids_processados.add(opt_id)
                        rows.append({
                            "Nível": "COMPLEMENTO",
                            "Categoria": cat_name,
                            "Produto Pai": current_prod_name,
                            "Grupo de opcionais": group_name, 
                            "Item / Opcional": f"{option.get('name')}",
                            "Código PDV (externalCode)": option.get('externalCode', ''),
                            "Status": option.get('status', ''),
                            "ID iFood": opt_id
                        })
    return pd.DataFrame(rows)

def mapear_codigos_atuais(token, m_id):
    headers = {"Authorization": f"Bearer {token}"}
    url_base_v2 = f"{URL_CATALOG_BASE_V2}/{m_id}"
    
    r_cat = requests.get(f"{url_base_v2}/catalogs", headers=headers)
    if r_cat.status_code != 200: raise Exception("Erro ao listar catálogos")
    catalog_id = r_cat.json()[0]['catalogId']
    
    url_tree = f"{url_base_v2}/catalogs/{catalog_id}/categories?includeItems=true"
    r_tree = requests.get(url_tree, headers=headers)
    categories = r_tree.json()
    
    mapa_atual = {}
    for cat in categories:
        for item in cat.get('items', []):
            item_id = item.get('id')
            item_code = item.get('externalCode', '')
            mapa_atual[item_id] = str(item_code) if item_code else ""
            
            for group in item.get('optionGroups', []):
                for option in group.get('options', []):
                    opt_id = option.get('id')
                    opt_code = option.get('externalCode', '')
                    mapa_atual[opt_id] = str(opt_code) if opt_code else ""
    return mapa_atual

def atualizar_item(token, m_id, id_obj, novo_codigo, nivel):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url_base_v2 = f"{URL_CATALOG_BASE_V2}/{m_id}"
    
    if nivel == 'PRODUTO':
        url = f"{url_base_v2}/items/externalCode"
        payload = {"itemId": str(id_obj), "externalCode": str(novo_codigo)}
    else: 
        url = f"{url_base_v2}/options/externalCode"
        payload = {"optionId": str(id_obj), "externalCode": str(novo_codigo)}
        
    return requests.patch(url, json=payload, headers=headers)