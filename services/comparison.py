import pandas as pd
import numpy as np
import unicodedata
import re

def normalize_string(s):
    """Normalize string by removing accents, stripping whitespace, converting to lowercase and removing non-alphanumeric chars."""
    if not isinstance(s, str):
        s = str(s)
    # Remove accents
    s = unicodedata.normalize('NFD', s)
    s = s.encode('ascii', 'ignore').decode("utf-8")
    # Lowercase
    s = s.lower()
    # Remove all non-alphanumeric characters (including spaces)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s.strip()

def compare_menus(vuca_df: pd.DataFrame, marketplace_df: pd.DataFrame, 
                  mkt_name_col: str = "Item / Opcional", 
                  mkt_pdv_col: str = "Código PDV (externalCode)",
                  mkt_name: str = "iFood") -> pd.DataFrame:
    """
    Compares marketplace menu data (iFood) with VUCA menu data.
    Focuses on ensuring everything in Marketplace exists and is correct in VUCA.
    
    Args:
        vuca_df: DataFrame with VUCA data
        marketplace_df: DataFrame with marketplace data
        mkt_name_col: Column name for item name in marketplace
        mkt_pdv_col: Column name for PDV code in marketplace
        mkt_name: Name of the marketplace (e.g., "iFood", "99Food")
        
    Returns:
        DataFrame with comparison results focused on Marketplace -> VUCA.
        Columns: Nível, Categoria, Item (VUCA), Item (Marketplace), PDV (VUCA), PDV (Marketplace), Status, Observação
    """
    results = []
    
    pdv_vuca_col = "PDV (VUCA)"
    pdv_mkt_col = f"PDV ({mkt_name})"
    item_vuca_col = "Item (VUCA)"
    item_mkt_col = f"Item ({mkt_name})"
    
    # Standardize marketplace columns for internal use if needed
    # But we use the provided column names.

    # Primary loop: Iterate through the Marketplace (iFood) items
    for idx, mkt_row in marketplace_df.iterrows():
        mkt_pdv = str(mkt_row.get(mkt_pdv_col, "")).strip()
        mkt_name_orig = str(mkt_row.get(mkt_name_col, ""))
        mkt_nivel = str(mkt_row.get("Nível", ""))
        mkt_cat = str(mkt_row.get("Categoria", ""))
        
        # 1. Try to find match in VUCA by PDV and Nível (Strict)
        vuca_match_pdv = vuca_df[
            (vuca_df["Código PDV"].astype(str).str.strip() == mkt_pdv) &
            (vuca_df["Nível"] == mkt_nivel)
        ]
        
        if not vuca_match_pdv.empty:
            # Match found by PDV. Check name.
            vuca_row = vuca_match_pdv.iloc[0]
            vuca_name_orig = str(vuca_row.get("Item / Opcional", ""))
            
            vuca_name_norm = normalize_string(vuca_name_orig)
            mkt_name_norm = normalize_string(mkt_name_orig)
            
            if vuca_name_norm == mkt_name_norm:
                status = "OK"
            else:
                status = "Nome Divergente"
                
            results.append({
                "Nível": mkt_nivel,
                "Categoria": mkt_cat,
                item_vuca_col: vuca_name_orig,
                item_mkt_col: mkt_name_orig,
                pdv_vuca_col: str(vuca_row.get("Código PDV", "")),
                pdv_mkt_col: mkt_pdv,
                "Status": status,
                "Observação": ""
            })
        else:
            # 2. Try to find match in VUCA by Name and Nível (Strict)
            mkt_name_norm = normalize_string(mkt_name_orig)
            vuca_match_name = vuca_df[
                (vuca_df["Item / Opcional"].apply(normalize_string) == mkt_name_norm) &
                (vuca_df["Nível"] == mkt_nivel)
            ]
            
            if not vuca_match_name.empty:
                vuca_row = vuca_match_name.iloc[0]
                results.append({
                    "Nível": mkt_nivel,
                    "Categoria": mkt_cat,
                    item_vuca_col: str(vuca_row.get("Item / Opcional", "")),
                    item_mkt_col: mkt_name_orig,
                    pdv_vuca_col: str(vuca_row.get("Código PDV", "")),
                    pdv_mkt_col: mkt_pdv,
                    "Status": "PDV Incorreto",
                    "Observação": f"No iFood o PDV é {mkt_pdv}, no VUCA é {vuca_row.get('Código PDV', '')}"
                })
            else:
                # 3. Item missing in VUCA
                results.append({
                    "Nível": mkt_nivel,
                    "Categoria": mkt_cat,
                    item_vuca_col: "",
                    item_mkt_col: mkt_name_orig,
                    pdv_vuca_col: "",
                    pdv_mkt_col: mkt_pdv,
                    "Status": "Faltando no VUCA",
                    "Observação": f"Item {mkt_name_orig} ({mkt_nivel}) não encontrado no VUCA."
                })

    return pd.DataFrame(results, columns=[
        "Nível", "Categoria", item_vuca_col, item_mkt_col, pdv_vuca_col, pdv_mkt_col, "Status", "Observação"
    ])
