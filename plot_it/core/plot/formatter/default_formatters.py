import matplotlib.dates as md

from plot_it.core.plot.formatter import formatter_store


# Computes Formatters
@formatter_store.register
def compute_bytes(x, *args, **kwargs):
    if x < 0:
        return ""
    for x_unit in ['bytes', 'kB', 'MB', 'GB', 'TB']:
        if x < 1024.0:
            return "%3.1f %s" % (x, x_unit)
        x /= 1024.0


# Time Formatters
@formatter_store.register
def time_hour(x, *args, **kwargs):
    formatter = md.DateFormatter('%H:%M')
    return formatter(x)
