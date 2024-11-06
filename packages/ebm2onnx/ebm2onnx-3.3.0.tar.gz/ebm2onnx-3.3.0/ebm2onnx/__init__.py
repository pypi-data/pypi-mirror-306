"""Top-level package for ebm2onnx."""

__author__ = """Romain Picard"""
__email__ = 'romain.picard@softathome.com'
__version__ = '3.3.0'

from .convert import to_onnx, get_dtype_from_pandas
from . import sklearn
