# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "fastapi>=0.104.1",
#     "uvicorn>=0.24.0",
#     "httpx>=0.25.2",
# ]
# ///

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx
from urllib.parse import urlparse

app = FastAPI()

'''
Write a FastAPI proxy server (1 mark)
Write a FastAPI proxy server that serves the data from the given URL but also adds a CORS header Access-Control-Allow-Origin: * to the response.

For example, if your API URL endpoint is http://127.0.0.1:8000/api, then a request to http://127.0.0.1:8000/api?url=https%3A%2F%2Fexample.com%2F%3Fkey%3Dvalue should return the data from https://example.com/?key=value but with the CORS header.

Note: Keep your server running for the duration of the exam.

What is your FastAPI Proxy URL endpoint?
'''


@app.get("/api")
async def proxy(url: str, request: Request):
    # Validate the URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL scheme")

    try:
        async with httpx.AsyncClient() as client:
            proxied_response = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502, detail=f"Error fetching URL: {str(e)}")

    # Build and return a response with headers and content from proxied site
    return Response(
        content=proxied_response.content,
        status_code=proxied_response.status_code,
        media_type=proxied_response.headers.get(
            "content-type", "application/octet-stream"),
        headers={
            "Access-Control-Allow-Origin": "*"
        }
    )


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn app:app --reload
