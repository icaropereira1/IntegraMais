# 🍔 Gestor de Códigos PDV

Ferramenta web desenvolvida em **Streamlit** para gerenciar códigos PDV (Ponto de Venda) entre o sistema **Vuca** e a plataforma **iFood**. Permite baixar cardápios, comparar códigos e realizar atualizações em lote diretamente via API.

---

## 📁 Estrutura do Projeto

```
gestor-pdv/
├── app.py                  # Interface Streamlit (UI)
├── config.py               # Constantes e configurações globais
├── requirements.txt        # Dependências do projeto
│
├── services/
│   ├── __init__.py
│   ├── ifood.py            # Integração com a API do iFood
│   └── vuca.py             # Scraping do sistema Vuca
│
└── utils/
    ├── __init__.py
    └── excel.py            # Geração de planilhas Excel
```

---

## ⚙️ Funcionalidades

### 📥 Aba 1 — Baixar Planilha iFood
Conecta à API do iFood usando as credenciais fornecidas e gera uma planilha Excel com todo o cardápio da loja, incluindo produtos e complementos com seus respectivos códigos PDV.

### 📤 Aba 2 — Atualizar PDVs no iFood
Recebe o upload de uma planilha editada e atualiza automaticamente no iFood apenas os itens cujo código PDV foi alterado, evitando requisições desnecessárias.

### 📤 Aba 3 — Baixar Planilha Vuca
Faz login no sistema Vuca e extrai o cardápio configurado para uma plataforma de delivery específica, gerando uma planilha Excel com produtos e complementos.

---

## 🔌 Plataformas de Delivery Suportadas (Vuca)

| Label exibido   | Valor interno     |
|-----------------|-------------------|
| iFood           | `ifood`           |
| Accon           | `accon`           |
| Anota AI        | `anotaai`         |
| Delivery Direto | `delivery_direto` |
| 99Food          | `nnfood`          |
| Cardápio Web    | `cardapioWeb`     |
| Keeta           | `keeta`           |

---

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/gestor-pdv.git
cd gestor-pdv
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação
```bash
streamlit run app.py
```

---

## 🔑 Credenciais necessárias

### API iFood (abas 1 e 2)
| Campo         | Descrição                          |
|---------------|------------------------------------|
| Client ID     | ID do cliente da API iFood         |
| Client Secret | Segredo do cliente da API iFood    |
| Merchant ID   | ID da loja no iFood                |

### Sistema Vuca (aba 3)
| Campo       | Descrição                              |
|-------------|----------------------------------------|
| Instância   | Subdomínio Vuca (ex: `minhaempresa`)   |
| ID Unidade  | ID da unidade no sistema Vuca          |
| Login       | Usuário de acesso ao Vuca              |
| Senha       | Senha de acesso ao Vuca                |

> ⚠️ Nenhuma credencial é armazenada. Tudo é processado em memória durante a sessão.

---

## 📦 Dependências

```
streamlit
requests
pandas
xlsxwriter
openpyxl
bs4
```

---

## 🗂️ Descrição dos módulos

### `config.py`
Centraliza todas as constantes do projeto: URLs da API iFood, configurações visuais do Excel (cores, senha de proteção, colunas bloqueadas) e tempos de espera para respeitar o rate limit da API.

### `services/ifood.py`
Responsável por toda comunicação com a API do iFood:
- `get_token` — autenticação via client credentials
- `extrair_cardapio_ifood` — extração completa do cardápio
- `mapear_codigos_atuais` — mapa de códigos PDV atuais para comparação
- `atualizar_item` — atualização de `externalCode` de produtos e opcionais

### `services/vuca.py`
Responsável pelo scraping do sistema Vuca:
- `logar_vuca` — autenticação via sessão HTTP
- `extrair_detalhes_adicionais` — extração de complementos de cada item
- `extrair_cardapio_vuca` — extração completa do cardápio com ordenação

### `utils/excel.py`
Geração do arquivo Excel em memória com formatação profissional: colunas bloqueadas, efeito zebra, filtros automáticos e proteção por senha.
