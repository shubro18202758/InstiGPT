# InstiGPT

The answer to all of insti's questions.

## Developing

The application has 3 parts: backend, frontend and a vector database.

### Backend

1. Install the dependencies using `pipenv install`.
1. Run the app using `pipenv run python main,py`.

### Frontend

1. Install the dependencies using `pnpm i`.
1. Run the app using `pnpm dev`.

### Vector DB

This app uses `chromadb` as its vector store.
To run an instance of `chromadb` in docker, run: `docker run -p 8000:8000 --env IS_PERSIST=true --env ALLOW_RESET=true --name chromadb chromadb/chroma`.

> NOTE: You may choose to recreate all the embeddings from scratch or reuse the ones provided in this repository. To reuse the ones provided in this repo, run `docker exec -it chromadb rm -rf /chroma/chroma; docker cp ./embeddings chromadb:/chroma/chroma`

## Running in Production

This app can easily be run in production through docker by running `docker compose up -d`
