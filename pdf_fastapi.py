# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "python-multipart",
#   "pdfplumber",
#   "pandas",
# ]
# ///

import pandas as pd
import pdfplumber
import io
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# --- FastAPI App Initialization ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_pdf(pdf_stream, product_to_find: str) -> float:
    """Parses a PDF, finds a table, and sums a column for a specific product."""
    total_sum = 0.0
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            # Extract tables from the page
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # Convert to DataFrame, using the first row as header
                df = pd.DataFrame(table[1:], columns=table[0])

                # Check if required columns exist
                if 'Product' not in df.columns or 'Total' not in df.columns:
                    continue

                # Clean data: remove non-numeric chars from 'Total' and convert
                df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

                # Filter by product and sum the 'Total'
                product_sum = df[df['Product'] ==
                                 product_to_find]['Total'].sum()
                total_sum += product_sum

    return total_sum

# --- Request Handler ---


@app.post("/analyze")
async def analyze_invoice(
    file: UploadFile = File(...),
    product_name: Optional[str] = Query(
        default="Widget",
        description="Name of the product to search for in the invoice. Defaults to 'Widget' if not provided."
    )
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a PDF.")

    # Use the provided product_name or fall back to default
    search_product = product_name if product_name else "Widget"

    contents = await file.read()
    pdf_stream = io.BytesIO(contents)

    calculated_sum = analyze_pdf(pdf_stream, search_product)

    return {
        "sum": calculated_sum,
        "product": search_product,
        "using_default": product_name is None or product_name == "Widget"
    }
