# =======
# Imports
# =======

# Basic stack
import pandas as pd
import numpy as np
import sklearn.linear_model as ln

# Upload and download files
from google.colab import files

# Geocoding and Maps
import geopy
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium import plugins

# Ver https://www.dataquest.io/blog/settingwithcopywarning/
pd.set_option('mode.chained_assignment', None)
pd.options.display.max_columns = 999

# ============
# type helpers
# ============

def _type_name(value):
  return type(value).__name__

# =============
# type checkers
# =============

def _check_single_dataframe(dataframe, function_name):
  if type(dataframe) is not pd.DataFrame:
    raise RuntimeError(f"El argumento de {function_name} debe ser un dataframe, pero vos le pasaste un {_type_name(dataframe)}")

def _check_single_series(series, function_name):
  if type(series) is not pd.Series:
    raise RuntimeError(f"El argumento de {function_name} debe ser un series, pero vos le pasaste un {_type_name(series)}")

def _check_single_dataframe_or_series(value, function_name):
  if type(value) is not pd.DataFrame and type(value) is not pd.Series:
    raise RuntimeError(f"El argumento de {function_name} debe ser un dataframe o un series, pero vos le pasaste un {_type_name(value)}")

def _check_args_count(args, expected_count, message):
  if len(args) != expected_count:
    raise RuntimeError(f"{message}, pero vos le estás pasando {len(args)}")

# ============
# File Reading
# ============

def read_csv(*args):
  _check_args_count(args, 2, "read_csv tiene que tomar dos argumentos (la ruta y el separador)")
  filename, separator = args

  if type(filename) is not str:
    raise RuntimeError(f"El primer argumento de read_csv es una ruta a un archivo y debe ser un string, pero vos le pasaste un {_type_name(filename)}")

  if type(separator) is not str:
    raise RuntimeError(f"El segundo argumento de read_csv es un separador y debe ser un string, pero vos le pasaste un {_type_name(separator)}")

  df = pd.read_csv(filename, sep=separator)
  return df

# ====================
# Stats and describing
# ====================

def describe(*args):
  _check_args_count(args, 1, "describe tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'describe')
  return value.describe()

def max(*args):
  _check_args_count(args, 1, "max tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'max')
  return value.max()

def min(*args):
  _check_args_count(args, 1, "min tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'min')
  return value.min()

def mean(*args):
  _check_args_count(args, 1, "mean tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'mean')
  return value.mean()

def median(*args):
  _check_args_count(args, 1, "median tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'median')
  return value.median()

def mode(*args):
  _check_args_count(args, 1, "mode tiene que tomar un argumento (el dataframe o series)")
  value, = args
  _check_single_dataframe_or_series(value, 'mode')
  return value.mode()


# std
# sample, head, tail


def unique(*args):
  _check_args_count(args, 1, "unique tiene que tomar un argumento (el series)")
  series, = args
  _check_single_series(series, 'unique')
  return pd.unique(series)

# ============
# Quantization
# ============

def quantize(column, rang):
  return np.ceil(column / rang) * rang

def normalize(column):
  return (column - column.min()) / (column.max() - column.min())

# pending:
# sample, head, tail

# ====
# Maps
# ====

def plot_map(dataframe, lat, long, radius, initial_point, initial_zoom = 12):
  if type(radius) == int:
    rad = lambda row: radius
  else:
    rad = lambda row: row[radius]

  plot = folium.Map(
    location = initial_point,
    tiles='cartodbpositron',
    zoom_start=initial_zoom)
  dataframe.apply(lambda row: folium.CircleMarker(location=[row[lat], row[long]], fill = True, radius = rad(row)).add_to(plot), axis=1)
  return plot

def plot_heat(dataframe, lat, long, heat, initial_point, radius = 10, initial_zoom = 12):
  if heat == None:
    points = dataframe[[lat, long]]
  else:
    points = dataframe[[lat, long, heat]]

  plot = folium.Map(initial_point,zoom_start = initial_zoom)
  plot.add_child(plugins.HeatMap(points.values, radius = radius))
  return plot

# =========
# Geocoding
# =========

class CachedGeocoder:
  def __init__(self, geocoder):
    self.geocoder = RateLimiter(geocoder, min_delay_seconds=1)
    self.geocodes = {}

  def geocode(self, address):
    if address not in self.geocodes:
      print("Geocoding ", address, "...")
      location = self.geocoder(address)
      self.geocodes[address] = location
    return self.geocodes[address]

def SuffixedGeocoder(geocoder, suffix):
  return lambda address: geocoder(address + ", " + suffix)

_geocoder = None
def geocoder():
  global _geocoder
  if not _geocoder:
    _geocoder = CachedGeocoder(geopy.Nominatim(user_agent="koalas").geocode)
  return _geocoder

def geocode(address):
  return geocoder().geocode(address)

def geocode_column(dataframe, column, prefix = None):
  dataframe = dataframe.copy()
  local_geocoder = SuffixedGeocoder(geocoder().geocode, prefix) if prefix else geocoder().geocode
  coordinates = dataframe[column].apply(local_geocoder)
  dataframe['lat'] = coordinates.apply(lambda c: c.latitude if c else None)
  dataframe['long'] = coordinates.apply(lambda c: c.longitude if c else None)
  return dataframe

# =======
# Predict
# =======

def compute_linear_model(df, columns):
  projection = df[columns]
  X = project if type(columns) == list else np.array(project).reshape(-1, 1)
  Y = np.array(df['manual_grade'])

  regr = linear_model.LinearRegression()
  regr.fit(X, Y)
  return (regr, regr.score(X, Y))

def predict(model, values):
  return model.predict([values])[0]
