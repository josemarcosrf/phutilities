import logging

from phutilities import version

# define the version before the other imports since these need it
__version__ = version.__version__

# TODO: Import here the different utility scripts


logging.getLogger(__name__).addHandler(logging.NullHandler())
