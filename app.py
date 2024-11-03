from fastapi import FastAPI, Query
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

# Inicie a API
app = FastAPI()

adjusted_embeddings = torch.load('data/adjusted_embeddings.pt')

# Função de busca usando similaridade do cosseno
def buscar_jogos(query, embeddings, df, top_n=10):
    query_embedding = autoencoder.encoder(sbert_model.encode([query], convert_to_tensor=True)).detach()
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    indices_recomendados = similarities.argsort()[-top_n:][::-1]
    recomendacoes = [
        {
            "game_name": df.iloc[idx]['game_name'],
            "description": df.iloc[idx]['description'],
            "url": df.iloc[idx]['url'],
            "relevance": similarities[idx]
        }
        for idx in indices_recomendados if similarities[idx] > 0
    ]
    return recomendacoes

@app.get("/query/")
async def get_recommendations(text: str = Query(..., min_length=1)):
    try:
        recommendations = buscar_jogos(text, adjusted_embeddings, df)
        return {"results": recommendations, "message": "OK"}
    except Exception as e:
        return {"message": str(e)}

# Para rodar a API
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9191)