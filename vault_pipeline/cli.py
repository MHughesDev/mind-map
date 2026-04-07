"""Command-line entry point for the vault pipeline."""

from __future__ import annotations

import typer

app = typer.Typer(
    name="vault-pipeline",
    help="Process and analyze the mind-map Obsidian vault.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Mind-map vault pipeline."""


if __name__ == "__main__":
    app()
