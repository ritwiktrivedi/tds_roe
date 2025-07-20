from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']
)
YOUR_EMAIL = "23f2001604@ds.study.iitm.ac.in"  # <-- replace with your own!

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Read the file data
    contents = await file.read()

    # Load to DataFrame; robust header handling
    df = pd.read_csv(
        io.BytesIO(contents),
        skipinitialspace=True,   # removes spaces right after commas (important!)
        dtype=str,               # treat everything as string for safety in cleaning
        quotechar='"'
    )

    # Clean column names: strip spaces, lowercase, remove internal spaces
    df.columns = [c.strip().lower().replace(" ", "") for c in df.columns]

    # Clean category: lowercase, strip spaces
    df['category'] = df['category'].str.strip().str.lower()

    # Select only rows with category == "food"
    food_rows = df[ df['category'] == 'food' ]

    # Clean "amount" column
    def clean_amount(x):
        if pd.isna(x):
            return 0.0
        s = str(x).replace(",", "").replace("$", "").replace("'", "").replace('"', "").strip()
        try:
            return float(s)
        except ValueError:
            return 0.0

    total = food_rows['amount'].map(clean_amount).sum()

    return {
        "answer": round(total,2),
        "email": YOUR_EMAIL,
        "exam": "tds-2025-05-roe"
    }

# -------------
# HOW TO RUN:
# -------------
# Run this FastAPI app with:
#    uvicorn csv_food_sum_api:app --reload --host 0.0.0.0 --port 8000
#
# Then POST a multipart form to http://localhost:8000/analyze with form field "file" containing your CSV.
#
# The endpoint will respond with JSON in the required format.
#
# ----------------
# IMPORTANT NOTES:
# ----------------
# 1. The script dynamically finds the category and amount columns by guessing column names.
#    Change the column name detection logic if your files use different names.
#
# 2. Handles varied number formats by stripping commas and currency symbols.
#
# 3. Category matching is case-insensitive and strips spaces.
#
# 4. If the "Food" category is missing, returns 0.0 total.
#
# 5. To deploy publicly, be sure to bind the server to 0.0.0.0 and use HTTPS.
#
# 6. Always test your endpoint with sample CSV prior to submitting URL.
#
# 7. Replace YOUR_EMAIL with your exact email (must match exam submission).
#
# 8. Enable CORS allows the testing server to be accessed from anywhere.


"""curl -X POST "http://localhost:8000/analyze" \
  -F "file=@path_to_your_sample.csv" \
  -H "accept: application/json"""

#to test locally on postman or bash
