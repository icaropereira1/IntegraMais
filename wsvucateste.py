from bs4 import BeautifulSoup
import requests

def logar_vuca(login, senha, instancia, id_unidade):
    url_login = f"https://{instancia}.vucasolution.com.br/retaguarda/"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "pt-BR,pt;q=0.9"})
    session.get(f"{url_login}login.php")
    r = session.post(f"{url_login}usuarios/login.php", data={
        "auth_login": login, "auth_senha": senha,
        "url": f"/retaguarda/pg_aplicativos_cardapio_ifood.php?csv=1&form=1&id_unidade={id_unidade}"
    }, allow_redirects=True)
    
    if r.status_code != 200:
        raise Exception("Falha no login. Verifique as credenciais e tente novamente.")
    
    return session, url_login

def extrair_cardapio_vuca(session, url_login, id_unidade):
    soup = BeautifulSoup(session.get(f"{url_login}pg_aplicativos_cardapio_ifood.php?csv=1&form=1&id_unidade={id_unidade}").content, "html.parser")
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
        #item_vuca = row.get("data-id")

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
            "nome_categoria": categoria_map.get(id_categoria_do_item_vuca, "Categoria Desconhecida"),
            "nome_item": nome_item_formatado,
            "codigo_edita": codigo_edita_formatado,
            "codigo_pdv": codigopdv_item_formatado
            })
        
        
        def extrair_detalhes_adicionais(session, url_base, id_item):
            url_ajax = f"{url_base}pg_aplicativos_cardapio_ifood.php?ajax=listarAdicionais&id_item_cardapio={codigo_edita_formatado}"
            response = session.get(url_ajax)
            soup_ajax = BeautifulSoup(response.content, "html.parser")

            adicionais = [] 

            grupos = soup_ajax.find_all("fieldset", class_="box-registros")
            print (grupos)

            for grupo in grupos:
                nome_grupodeopcionais_sem_formatacao = grupo.find("legend")
                nome_grupodeopcionais_formatado = nome_grupodeopcionais_sem_formatacao.text.strip() if nome_grupodeopcionais_sem_formatacao else "Grupo de Opcionais Desconecido"

        
        extrair_detalhes_adicionais(session, url_login, codigo_edita_formatado)


            
    
    return itens, categorias


logar_vuca("", "", "bacanas", "3195")
extrair_cardapio_vuca(logar_vuca("", "", "bacanas", "3195")[0], logar_vuca("", "", "bacanas", "3195")[1], "3195")

'''
[<fieldset class="box-registros box-registros_m">
<legend onclick="$(this).parent().find('div').slideToggle();" style="cursor:pointer;"> <a href="pg_produtos_grupodeopcionais.php?form=1&amp;edita=36&amp;" target="_blank"> OPCIONAIS ALMOÇO EXECUTIVO</a> <span class="iconify" data-icon="ant-design:caret-down-outlined"></span></legend>
<div style="margin:0;display: none;">
<table class="">
<thead>
<tr>
<th style="width:70px;">Produto</th>
<th style="width:70px;">PDV do Adicional</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=837&amp;" target="_blank">OVO FRITO</a></td>
<td>837</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=836&amp;" target="_blank">BANANA FRITA</a></td>
<td>836</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=838&amp;" target="_blank">LEGUMES NA MANTEIGA</a></td>
<td>838</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=839&amp;" target="_blank">FEIJAO DE CALDO</a></td>
<td>839</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=840&amp;" target="_blank">FEIJAO TROPEIRO</a></td>
<td>840</td>
</tr>
</tbody>
</table>
</div>
</fieldset>, <fieldset class="box-registros box-registros_m">
<legend onclick="$(this).parent().find('div').slideToggle();" style="cursor:pointer;"> <a href="pg_produtos_grupodeopcionais.php?form=1&amp;edita=11&amp;" target="_blank"> PARA VIAGEM?</a> <span class="iconify" data-icon="ant-design:caret-down-outlined"></span></legend>
<div style="margin:0;display: none;">
<table class="">
<thead>
<tr>
<th style="width:70px;">Produto</th>
<th style="width:70px;">PDV do Adicional</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=1517&amp;" target="_blank">TALHER PARA VIAGEM</a></td>
<td>1517</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=219&amp;" target="_blank">EMBALAR PARA VIAGEM</a></td>
<td>219</td>
</tr>
</tbody>
</table>
</div>
</fieldset>, <fieldset class="box-registros box-registros_m">
<legend onclick="$(this).parent().find('div').slideToggle();" style="cursor:pointer;"> <a href="pg_produtos_grupodeopcionais.php?form=1&amp;edita=12&amp;" target="_blank"> COMBO EXECUTIVO ENTRADA</a> <span class="iconify" data-icon="ant-design:caret-down-outlined"></span></legend>
<div style="margin:0;display: none;">
<table class="">
<thead>
<tr>
<th style="width:70px;">Produto</th>
<th style="width:70px;">PDV do Adicional</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=831&amp;" target="_blank">2 CROQUETE DE LOMBO</a></td>
<td>831</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=1518&amp;" target="_blank">2 PALITINHOS DE MUSSARELA</a></td>
<td>1518</td>
</tr>
<tr>
<td><a href="pg_produtos.php?form=1&amp;edita=1173&amp;" target="_blank">MINI CEVICHE DE BANANA DA TERRA</a></td>
<td>1173</td>
</tr>
</tbody>
</table>
</div>
</fieldset>]
'''