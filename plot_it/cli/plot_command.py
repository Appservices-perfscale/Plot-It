import sys
import logging

import click
from pydantic import ValidationError

from plot_it.core.data_loader import load_yaml_file
from plot_it.core.plot import Plotter
from plot_it.models import Plot
from plot_it.utils.logger_config import get_log_level

logger = logging.getLogger()


@click.command()
@click.option('-f', '--filename', type=str, default='plot.yaml',
              help="Path to input YAML file that contains plot-it configuration.")
@click.option('-v', '--verbose', count=True, default=2, help="Set verbosity for log level")
def plot(
    filename: str,
    verbose: int
):
    '''Plot Command'''
    # Setting up root logger
    log_level = get_log_level(verbose)
    logger.setLevel(log_level)

    # Read plot-it configuration file
    try:
        logger.info("Loading yaml config data from filepath: %s", filename)
        config_data = load_yaml_file(filename)
    except FileNotFoundError:
        logger.error("Given filepath '%s' not found.", filename)
        sys.exit(1)

    # Load plot-it configuration data
    try:
        logger.info("Parsing config data for plots and charts")
        plot_data = Plot(**config_data)
    except ValidationError as error:
        logger.error(
            "Error parsing plot-it configuration file %s: %s",
            filename, error, exc_info=True)
        sys.exit(1)

    # Plot charts and graphs
    plotter = Plotter(plot_data=plot_data)
    plotter.plot()
