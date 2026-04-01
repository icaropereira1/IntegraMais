# iFood
URL_AUTH = "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token"
URL_CATALOG_BASE = "https://merchant-api.ifood.com.br/catalog/v1.0/merchants"
URL_CATALOG_BASE_V2 = "https://merchant-api.ifood.com.br/catalog/v2.0/merchants"

# Excel
COLUNAS_BLOQUEADAS = [
    "Nível", "Categoria", "Produto Pai", "Item / Opcional",
    "Status", "ID iFood", "Código PDV", "Código Editado", "Grupo de opcionais"
]
SENHA_PROTECAO_EXCEL = "xicaroehfoda"
COR_ZEBRA = "#F2F2F2"
COR_BLOQUEADO = "#F4F9FF"

# Comparação
COLUNAS_COMPARACAO = [
    "Nível", "Categoria", "Item (VUCA)", "Item (iFood)", "PDV (VUCA)", "PDV (iFood)", "Status", "Observação"
]

COR_OK = "#C6EFCE"       # Verde claro
COR_DIVERGENTE = "#FFEB9C" # Amarelo claro
COR_FALTANDO = "#FFC7CE"  # Vermelho claro
