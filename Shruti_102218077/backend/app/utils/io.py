import pandas as pd

REQUIRED_COLS = ["uniq_id","title","brand","description","price",
                 "categories","images","manufacturer","package dimensions",
                 "country_of_origin","material","color"]

def load_products(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for c in REQUIRED_COLS:
        if c not in df.columns:
            df[c] = None
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["text_blob"] = (df["title"].fillna('') + " | " +
                       df["brand"].fillna('') + " | " +
                       df["description"].fillna('') + " | " +
                       df["material"].fillna('') + " | " +
                       df["categories"].fillna(''))
    return df
