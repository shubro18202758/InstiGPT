# InstiGPT

The answer to all of insti's questions.

## NOTION PAGE FOR HELLOFOSS CONTRIBUTORS
[CLICK HERE](https://magical-ornament-602.notion.site/27c83e2bca3f80df826edae7da9e0de7?v=27c83e2bca3f803f9796000c2f66f220&source=copy_link) - WE ARE STILL UPDATING!

## Developing

The application has 4 parts: backend, frontend a vector database and a relational database.

### Backend

1. Install the dependencies using `pipenv install`.
1. Run the app using `pipenv run python main.py`.

### Frontend

1. Install the dependencies using `pnpm i`.
1. Run the app using `pnpm dev`.

### Vector DB

This app uses `chromadb` as its vector store.
To run an instance of `chromadb` in docker, run: `docker run -p 8000:8000 --env IS_PERSIST=true --env ALLOW_RESET=true --name chromadb chromadb/chroma`.

Also make sure you set the required environment variables in the `.env` file namely `VECTOR_DB_HOST` to `localhost` and `VECTOR_DB_PORT` to `8000`

To generate embeddings, run `pipenv run python load_data_in_db.py` in scripts folder. Do the commented changes accordingly to use resobin data or ugrulebook data in `load_data_in_db.py` and `config.py`.

### Relational DB

This app uses `postgres` as its relational database.
To run an instance of `postgres` in docker, run: `docker run -p 5432:5432 --env POSTGRES_PASSWORD=<password> --name postgres postgres`.

## Running in Production

This app can easily be run in production through docker by running `docker compose up -d`
