import pandas as pd


def read_csv(filename, sepator=','):
    pd.read_csv(filename, sep=sepator)


def describe(dataframe):
    return dataframe.describe()

# first(dataframe, count?)
# last(dataframe, count?)
# sort_ascending(dataframe, column_name)
# sort_ascending(series)
# sort_descending(dataframe, column_name)
# sort_descending(series)

# bar_plot(series)
# line_plot(series)
# scatter_plot(dataframe)

# replace_column(dataframe, column_name, series)

# copy(dataframe)
# copy(series)


# to_duration(dataframe, column_name)
# to_duration(series)

# to_datetime(dataframe, column_name)
# to_datetime(series)

# to_float
# to_int

# drop_nan(dataframe, columns?)
# fill_nan(dataframe, columns?)

# is_nan
# is_not_nan

# value_counts(dataframe, column_name)
# group_by(dataframe, column_name) ????


koalas.filter(dataframe, lambda it: it.field  > 0)