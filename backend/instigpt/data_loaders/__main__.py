from rich import print
from rich.progress import Progress, TextColumn, SpinnerColumn
from rich.prompt import Prompt, Confirm

from dotenv import load_dotenv

load_dotenv()
print(":white_check_mark: [bold]Loaded environment variables![/bold]")

from instigpt import llm
from instigpt import data_loaders

emdbeddings = llm.embeddings.get_embeddings()
with Progress(
    SpinnerColumn(), TextColumn("{task.description}"), transient=True
) as progress:
    task = progress.add_task("Connecting to database...", total=None)
    client = llm.retriever.get_db_client()
print(":white_check_mark: [bold]Connected to vector database![/bold]")

reset = Confirm.ask("Do you want to reset the database?", default=False)
if reset:
    client.reset()
    print(":white_check_mark: [bold]Reset the database![/bold]")

file_path = Prompt.ask(
    "Enter the path to the file to load data from (relative to current dir)"
)
document_name = Prompt.ask(
    "Enter the name of the document", default=file_path.split("/")[-1].split(".")[0]
)

with Progress(
    SpinnerColumn(), TextColumn("{task.description}"), transient=True
) as progress:
    task = progress.add_task("Loading data...", total=None)
    if file_path.endswith(".pdf"):
        num_docs_added = data_loaders.load_pdf_data(
            client=client,
            embeddings=emdbeddings,
            document_name=document_name,
            data_path=file_path,
        )
    elif file_path.endswith(".json"):
        num_docs_added = data_loaders.load_json_data(
            client=client,
            embeddings=emdbeddings,
            document_name=document_name,
            data_path=file_path,
        )
    elif file_path.endswith("WEBLOADER.csv"):
        num_docs_added = data_loaders.load_web_urls_in_csv_data(
            client=client,
            embeddings=emdbeddings,
            document_name=document_name,
            data_path=file_path,
        )
    elif file_path.endswith(".csv"):
        num_docs_added = data_loaders.load_csv_data(
            client=client,
            embeddings=emdbeddings,
            document_name=document_name,
            data_path=file_path,
        )

    else:
        print(":x: [bold red]Invalid file format![/bold red]")
        print("[red]Only [bold].pdf, .json[/bold] and .csv[/bold] files are supported![/red]")
        exit(1)

print(
    f":white_check_mark: [green]Added [bold]{num_docs_added}[/bold] documents to the database![/green]"
)
