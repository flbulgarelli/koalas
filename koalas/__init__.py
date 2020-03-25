# =======
# Imports
# =======
import pandas as pd

# ============
# type helpers
# ============

def type_name(value):
    return type(value).__name__

# =============
# type checkers
# =============

def check_single_dataframe(dataframe, function_name): 
    if type(dataframe) is not pd.DataFrame:
        raise RuntimeError(f"El argumento de {function_name} debe ser un dataframe, pero vos le pasaste un {type_name(dataframe)}")

def check_single_series(series, function_name): 
    if type(series) is not pd.Series:
        raise RuntimeError(f"El argumento de {function_name} debe ser un series, pero vos le pasaste un {type_name(series)}")

def check_single_dataframe_or_series(value, function_name): 
    if type(value) is not pd.DataFrame and type(value) is not pd.Series:
        raise RuntimeError(f"El argumento de {function_name} debe ser un dataframe o un series, pero vos le pasaste un {type_name(value)}")

def check_args_count(args, expected_count, message):
    if len(args) != expected_count: 
        raise RuntimeError(f"{message}, pero vos le estás pasando {len(args)}")


# ==============================
# actual koalas public functions
# ===============================


def read_csv(*args):
    check_args_count(args, 2, "read_csv tiene que tomar dos argumentos (la ruta y el separador)")
    filename, separator = args

    if type(filename) is not str:
        raise RuntimeError(f"El primer argumento de read_csv es una ruta a un archivo y debe ser un string, pero vos le pasaste un {type_name(filename)}")

    if type(separator) is not str:
        raise RuntimeError(f"El segundo argumento de read_csv es un separador y debe ser un string, pero vos le pasaste un {type_name(separator)}")

    df = pd.read_csv(filename, sep=separator)
    return df

def describe(*args):
    check_args_count(args, 1, "describe tiene que tomar un argumento (el dataframe o series)")
    value, = args
    check_single_dataframe_or_series(value, 'describe')
    return dataframe.describe()

def maximum(*args):
    check_args_count(args, 1, "maximum tiene que tomar un argumento (el dataframe o series)")
    value, = args
    check_single_dataframe_or_series(value, 'maximum')
    return dataframe.max()

def minimum(*args):
    check_args_count(args, 1, "minimum tiene que tomar un argumento (el dataframe o series)")
    value, = args
    check_single_dataframe_or_series(value, 'minimum')
    return dataframe.min()

def unique(*args):
    check_args_count(args, 1, "unique tiene que tomar un argumento (el series)")
    series, = args
    check_single_series(series, 'unique')

    return pd.unique(series)

koalas.filter(dataframe, lambda it: it.field  > 0)
