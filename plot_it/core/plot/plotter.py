import os
import glob
import logging

from plot_it.models import Plot, PlotResult
from plot_it.core.plot.engine import MathplotlibEngine

logger = logging.getLogger()


class Plotter:
    def __init__(self, plot_data: Plot):
        self.plot_data = plot_data
        self.input_data_files = {}
        self.result = PlotResult()

        # Load Data filenames
        self.load_input_data_filenames()

        # default engine for rendering
        # pylint: disable=abstract-class-instantiated
        self.engine = MathplotlibEngine(
            plot=plot_data,
            data_sources=self.input_data_files
        )

    def load_input_data_filenames(self):
        '''
        Load the filenames of input data into memory. The file's basename is
        used to select the file data to be considered for plotting in Chart.
        '''
        logger.debug("Loading input data filenames")
        for path in self.plot_data.input.paths:
            files = glob.glob(path)
            for file in files:
                # Take last part of the file path's filename
                filename = os.path.basename(file)

                # remove extension
                filename = "".join(filename.split(".")[:-1])

                # Store filename mapping into dictionary
                self.input_data_files[filename] = file

        logger.info("Found %d number of input data files.", len(files))

    def plot(self):
        logger.info('Generating chart plots')

        for chart in self.plot_data.charts:
            try:
                # render and save chart
                self.engine(chart)
                self.result.success += 1
            except Exception as error:
                logger.error(
                    "Unable to generate chart '%s': %s",
                    chart.name,
                    error
                )
                self.result.failed += 1

        logger.info(
            'Plot Result: Total (%d) | Success (%d) | Failed (%d)',
            self.result.success + self.result.failed,
            self.result.success,
            self.result.failed
        )
