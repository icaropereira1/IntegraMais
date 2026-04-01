import pandas as pd
import io
from config import COLUNAS_BLOQUEADAS, SENHA_PROTECAO_EXCEL, COR_ZEBRA, COR_BLOQUEADO, COR_OK, COR_DIVERGENTE, COR_FALTANDO

def gerar_excel_em_memoria(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Cardapio', index=False)

    workbook  = writer.book
    worksheet = writer.sheets['Cardapio']

    formato_bloqueado = workbook.add_format({'locked': True, 'bg_color': COR_BLOQUEADO})
    formato_liberado = workbook.add_format({'locked': False})

    colunas_para_bloquear = ["Nível", "Categoria", "Produto Pai", "Item / Opcional", "Status", "ID iFood", "Código PDV", "Link", "Grupo de opcionais"]

    for col_num, col_name in enumerate(df.columns):
        if not df[col_name].empty:
            max_len = max(df[col_name].astype(str).map(len).max(), len(str(col_name))) + 2
        else:
            max_len = len(str(col_name)) + 2

        if max_len > 60: max_len = 60

        if col_name in colunas_para_bloquear:
            worksheet.set_column(col_num, col_num, max_len, formato_bloqueado)
        else:
            worksheet.set_column(col_num, col_num, max_len, formato_liberado)

    # APLICANDO O EFEITO ZEBRA 
    formato_zebra = workbook.add_format({'bg_color': COR_ZEBRA})

    # Aplica a formatação condicional da linha 1 (abaixo do cabeçalho) até o final do DF
    worksheet.conditional_format(1, 0, len(df), len(df.columns) - 1, {
        'type': 'formula',
        'criteria': '=MOD(ROW(), 2) = 0', # Lê-se: Se a linha for par, aplique a cor
        'format': formato_zebra
    })

    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    worksheet.protect(SENHA_PROTECAO_EXCEL, {
        'autofilter': True,
        'objects': True,
        'select_locked_cells': True,
        'select_unlocked_cells': True, 
        'format_columns': True
    })

    writer.close()
    return output.getvalue()


def gerar_excel_comparativo(df):
    """Gera o Excel de comparação com formatação condicional."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Comparação', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Comparação']

    # Formatos
    fmt_ok = workbook.add_format({'bg_color': COR_OK})
    fmt_divergente = workbook.add_format({'bg_color': COR_DIVERGENTE})
    fmt_faltando = workbook.add_format({'bg_color': COR_FALTANDO})

    # Ajustar largura e formatação básica
    for col_num, col_name in enumerate(df.columns):
        if not df[col_name].empty:
            max_len = max(df[col_name].astype(str).map(len).max(), len(str(col_name))) + 2
        else:
            max_len = len(str(col_name)) + 2
        if max_len > 60: max_len = 60
        worksheet.set_column(col_num, col_num, max_len)

    # Identificar coluna 'Status'
    if 'Status' in df.columns:
        idx_status = list(df.columns).index('Status')

        # Aplicar formatação condicional baseada no status
        worksheet.conditional_format(1, 0, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': f'=${chr(65+idx_status)}2="OK"',
            'format': fmt_ok
        })
        worksheet.conditional_format(1, 0, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': f'=OR(ISNUMBER(SEARCH("Divergente", ${chr(65+idx_status)}2)), ISNUMBER(SEARCH("Incorreto", ${chr(65+idx_status)}2)))',
            'format': fmt_divergente
        })
        worksheet.conditional_format(1, 0, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': f'=OR(ISNUMBER(SEARCH("Faltando", ${chr(65+idx_status)}2)), ISNUMBER(SEARCH("Ausente", ${chr(65+idx_status)}2)))',
            'format': fmt_faltando
        })

    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    writer.close()
    return output.getvalue()