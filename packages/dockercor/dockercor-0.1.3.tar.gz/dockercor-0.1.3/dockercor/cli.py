# dockercor/cli.py
import typer
from typing import List, Optional
from . import docker_manager

app = typer.Typer()


@app.command()
def ensure_image(
    image_name: str,
    force: bool = typer.Option(False, "--force", "-f", help="Force update the image"),
) -> None:
    """Ensure a Docker image is available locally"""
    try:
        updated, message = docker_manager.ensure_docker_image(image_name, force)
        if updated:
            typer.echo(f"Success: {message}")
        else:
            typer.echo(f"Info: {message}")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def run(
    ctx: typer.Context,
    image_name: str,
    command: str = typer.Argument(..., help="Initial command to run in the container"),
) -> None:
    """Run a command in a Docker container"""
    try:
        # Combine the initial command with any extra args
        full_command = [command] + (ctx.args if ctx.args else [])
        docker_manager.run_docker_command(full_command, image_name)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def info(image_name: str) -> None:
    """Get information about a Docker image"""
    try:
        image_info = docker_manager.get_image_info(image_name)
        if image_info:
            typer.echo("Image Information:")
            for key, value in image_info.items():
                typer.echo(f"{key}: {value}")
        else:
            typer.echo(f"Image {image_name} not found locally")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
