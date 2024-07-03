import os
import logging

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from plot_it.models import Chart, ChartType, Plot
from plot_it.core.plot.engine import Engine, InvalidChartType
from plot_it.core.plot.formatter import formatter_store
from plot_it.utils.date_utils import (
    convert_to_timestamp_series,
    convert_to_datetime
)

logger = logging.getLogger()


class MathplotlibEngine(Engine):
    def __init__(self, plot: Plot, data_sources: dict):
        self.plot = plot
        self.data_sources = data_sources

    def __call__(self, chart: Chart):
        if chart.type == ChartType.timeseries:
            self.timeseries(chart)
        else:
            raise InvalidChartType(
                "Chart type '{type}' undefined for mathplotlib engine!".format(
                    type=chart.type
                )
            )

    def save_chart_to_file(self, fig, ax, chart: Chart):
        name = chart.name
        file_output = os.path.join(self.plot.output.dir, name + ".png")

        logger.debug("Saving '%s' chart into file: %s", name, file_output)

        if os.path.exists(file_output) and self.plot.output.overwrite is False:
            raise FileExistsError("Unable to save chart as '{file}' already exists. Try setting 'plot.output.overwrite=true' to overwrite existing contents in the save directory.".format(file=file_output))

        if not os.path.exists(self.plot.output.dir):
            logger.info("Creating output directory for saving plots: %s", self.plot.output.dir)
            os.mkdir(self.plot.output.dir)

        fig.tight_layout()
        fig.savefig(file_output)

    def timeseries(self, chart: Chart):
        # Create matplotlib figures and axis to draw data points    
        fig, ax = plt.subplots()

        # Set Title for the graph and axis
        logger.debug('Configuring Chart metadata')
        if chart.name:
            fig.suptitle(chart.name, fontsize=12)

        if chart.xaxis.name:
            ax.set_xlabel(chart.xaxis.name, fontsize=10)
        else:
            ax.set_xlabel("Timestamp", fontsize=10)

        if chart.yaxis.name:
            ax.set_ylabel(chart.yaxis.name, fontsize=10)

        # Set X-axis Formatters
        logger.debug('Configuring Chart X-Axis Formatter')
        if chart.xaxis.formatter is not None:
            x_axis_formatter = formatter_store.get(chart.xaxis.formatter)
        else:
            x_axis_formatter = formatter_store.get("time_hour")
        ax.xaxis.set_major_formatter(
            FuncFormatter(x_axis_formatter)
        )

        # Set Y-axis Formatters
        logger.debug('Configuring Chart Y-Axis Formatter')
        if chart.yaxis.formatter is not None:
            y_axis_formatter = formatter_store.get(chart.yaxis.formatter)
            ax.yaxis.set_major_formatter(
                FuncFormatter(y_axis_formatter)
            )

        # Plot data points
        min_y_val = float('inf')
        cols_rendered_count = 0
        for data_name in chart.data:
            # Load Dataframe
            csv_file = self.data_sources[data_name]
            df = pd.read_csv(csv_file)

            logger.debug("Data(%s) Shape - %s", data_name, df.shape)

            # Extract X-Axis Col Data
            x = df[chart.xaxis.data]

            # Convert x-axis column into timestamp series
            try:
                x = convert_to_timestamp_series(x)
            except Exception as error:
                logger.warning(
                    "Unable to convert x-axis to timestamp: %s",
                    error
                )

            # Extract Y-Axis Col Data

            # Remaining type
            if chart.yaxis.data is None or chart.yaxis.data == "%":
                # Get remaining col names
                cols = [col for col in df.columns if col != chart.xaxis.data]
                y = df[cols]
                cols_rendered_count += len(cols)
            else:
                y = df[chart.yaxis.data].to_frame()
                cols_rendered_count += 1

            min_y_val = min(min_y_val, y.min().iloc[0])

            # Plot chart
            for col in y.columns:
                ax.plot(x, y[col], label=col)

        # Plot Events
        if chart.show_events is True or self.plot.show_events is True:
            for event in self.plot.events:
                date = convert_to_datetime(event.timestamp, event.format)
                label = event.name
                plt.axvline(
                    x=date,
                    color='r',
                    linestyle='--',
                    linewidth=1.5,
                    alpha=0.5
                )
                plt.annotate(
                    label,
                    xy=(date, min_y_val),
                    xytext=(8, 8),
                    textcoords='offset points', color='r', fontsize=8,
                )

        # Show Legend
        if cols_rendered_count > 1:
            ax.legend()

        # Save results as chart
        self.save_chart_to_file(
            fig=fig,
            ax=ax,
            chart=chart
        )
