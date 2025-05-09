import uvicorn

from graphrag import GraphRag

app = GraphRag()

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
