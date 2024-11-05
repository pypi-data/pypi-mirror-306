import typer

llm = typer.Typer(short_help="The LLM management.")


@llm.command(short_help="Start a server for the LLM.")
def serve(
    model: str = typer.Argument("", help="The ID of the LLM model to use."),
    model_name: str = typer.Argument("", help="The name of the LLM model to use."),
    parallal_size: int = typer.Option(1, help="The number of GPUs to use."),
    host: str = typer.Option("0.0.0.0", help="The host of the server."),
    port: int = typer.Option(8000, help="The port of the server."),
):
    from mw_python_sdk.llm.inference import serve

    serve(model, model_name=model_name, host=host, port=port)


datasets = typer.Typer(short_help="The datasets management.")


@datasets.command(short_help="Create a new dataset by uploading a directory.")
def create(
    name: str = typer.Argument(..., help="The name of the dataset to create."),
    source: str = typer.Argument(..., help="The path to the directory to upload."),
    description: str = typer.Option(None, help="The description of the dataset."),
):
    from mw_python_sdk import create_dataset

    create_dataset(name, source, "", description)
    return


@datasets.command(short_help="Upload a file or directory to the dataset.")
def upload(
    source: str = typer.Argument(
        help="The path to the file or the directory to upload."
    ),
    destination: str = typer.Argument(
        help="The destination of the file or the directory in the dataset."
    ),
    dataset: str = typer.Argument(help="The ID of the dataset to upload in."),
    overwrite: bool = typer.Option(
        False, help="Whether to overwrite the file if it already exists."
    ),
    recursive: bool = typer.Option(
        False, "-r", help="Whether to recursively upload all files in the directory."
    ),
):
    from mw_python_sdk import upload_file, upload_folder
    import os

    if recursive:
        if not os.path.isdir(source):
            raise ValueError("Source must be a directory when using --recursive.")
        upload_folder(source, destination, dataset, overwrite)
        return
    else:
        upload_file(source, destination, dataset, overwrite)
        return


@datasets.command(short_help="Download a file or directory from the dataset.")
def download(
    dataset: str = typer.Argument(..., help="The ID of the dataset to download from."),
    source: str = typer.Argument(
        None, help="The name of the file or the directory to download."
    ),
    destination: str = typer.Option(
        None, "-d", help="The destination directory of the downloaded file."
    ),
    recursive: bool = typer.Option(
        False,
        "-r",
        help="Whether to recursively download all files in the directory.",
    ),
):
    from mw_python_sdk import download_file, download_dir

    if recursive or source is None:
        downloaded_dir = download_dir(dataset, sub_dir=source, local_dir=destination)
        print(f"Successfully downloaded to {downloaded_dir}")
        return
    else:
        downloaded_file = download_file(dataset, source, local_dir=destination)
        print(f"Successfully downloaded to {downloaded_file}")
        return



app = typer.Typer()
app.add_typer(llm, name="llm")
app.add_typer(datasets, name="ds")

@app.command(short_help="Set up a fast reverse proxy.")
def frp(
    port: int = typer.Argument(..., help="The port of the proxy.")
):
    from mw_python_sdk.frp import fast_reverse_proxy

    fast_reverse_proxy(port)

if __name__ == "__main__":
    app()
