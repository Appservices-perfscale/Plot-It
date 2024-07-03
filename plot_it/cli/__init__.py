'''CLI Entrypoint'''
import click

from plot_it.cli import plot_command

# Setup root logger
from plot_it.utils.logger_config import setup_default_logger

@click.group()
def cli():
    """CLI Package"""
    pass

# Setup root logger
setup_default_logger()

# Register all commands for CLI
cli.add_command(plot_command.plot)
