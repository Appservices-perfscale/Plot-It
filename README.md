# Plot-It

Manage and visualize plots in declarative manner.

"Plot It" is a CLI-based utility to automate data visualization through simple YAML definitions.

> **NOTE ⚠️:** This project is currently in active development and is not production-ready. Features, functionality, and APIs are subject to change. Feedbacks are welcome through raising issues on this repository!

## Highlights

As of current release, this projects supports the following capability:
- Data Source Loader: CSV
- Chart/Graph: Timeseries
- Data Formatters: Time, Compute, Numeric

Following capabilities are in development/roadmap:
- Load data from JSON source
- Support for plotting histogram and bar graphs
- Add custom data formatters
- Chart Customizations (Theme/Fonts/Colors/etc)

## Installation

```
$ pip install git+https://https://github.com/Appservices-perfscale/Plot-It.git

$ plot_it --help
Usage: plot_it [OPTIONS] COMMAND [ARGS]...

  CLI Package

Options:
  --help  Show this message and exit.

Commands:
  plot  Plot Command
```

## Getting Started

```
$ mkdir -p project
$ cd project

# Download sample data
$ curl -OL https://raw.githubusercontent.com/Appservices-perfscale/Plot-It/main/examples/weather/weather_data.csv
$ head -n 10 weather_data.csv

cat <<EOF >>plot.yaml
input:
  paths:
  - ./weather_data.csv

output:
  dir: ./results/
  overwrite: true

charts:
- type: timeseries
  name: Weather Humidity
  data:
  - weather_data
  xaxis:
    name: Timestamp
    formatter: time_hour
    data: timestamp
  yaxis:
    name: Humidity
    data: "humidity"
EOF

# Plot charts for weather data
$ plot_it plot
$ ls -l ./results/
```

You can find more details on the YAML fields from this detailed example: [plot.yaml](examples/weather/plot.yaml).
