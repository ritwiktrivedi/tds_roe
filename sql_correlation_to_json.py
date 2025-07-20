import pandas as pd
import sqlite3
import json
import os

# ========== PARAMETERS ========== #

#SQL_FILE = "q-sql-correlation-github-pages.sql"  # Input SQL file
SQL_FILE = "testdata.sql"  # Change this to your actual SQL file name
DB_FILE = "temp_retail.db"                       # Temporary local DB
TABLE_NAME = "retail_data"                       # Name as per SQL schema

# ================================= #

# -- 1. Load SQL file into SQLite DB --
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
conn = sqlite3.connect(DB_FILE)
with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_script = f.read()
conn.executescript(sql_script)
conn.commit()

# -- 2. Read the full table with pandas --
df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
conn.close()
os.remove(DB_FILE)  # Clean up temp DB

# -- 3. Calculate correlations ---
pairs = [
    ('Footfall', 'Promo_Spend'),
    ('Footfall', 'Avg_Basket'),
    ('Promo_Spend', 'Avg_Basket')
]
correlations = {
    f"{p1}-{p2}": df[p1].corr(df[p2])
    for p1, p2 in pairs
}
strongest_pair = max(correlations, key=lambda k: abs(correlations[k]))
strongest_value = correlations[strongest_pair]

# -- 4. Output to JSON file --
result = {
    "pair": strongest_pair,
    "correlation": round(strongest_value, 6)  # Rounded for display, not required
}
with open("answer.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

# ========== IMPORTANT NOTES & NEXT STEPS ==========
#
# 1. To use:
#    - Download the .sql file from the exam system.
#    - Place it in the same folder as this script (rename if different).
#    - Run:   python sql_correlation_to_json.py
#
# 2. After running, upload the generated "answer.json" to your GitHub Pages repo.
#    - Push it and, once live, copy the RAW URL (not blob!)
#
# 3. Paste that URL into the exam form as your answer.
#
# 4. This script is fully generic! It does not require manual editing unless the
#    table name or column names change (which is unlikely if the schema is the same).
#
# 5. To change input files: just set SQL_FILE = "your_file.sql" at the top.
#
# 6. Don't forget to clean up old temp SQLite files if anything fails mid-run.
#
# 7. Requires: python, pandas
#       pip install pandas
#
# ========== END OF SCRIPT ==========
