"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Social Media Manager."""


if __name__ == "__main__":
    main(prog_name="social-media-manager")  # pragma: no cover
