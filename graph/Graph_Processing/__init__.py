import logging

# Create a logger
logger = logging.getLogger(__name__)

# Configure the logger
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

# Create a file handler
file_handler = logging.FileHandler('..\graph_analysis.log')

# Create a formatter and set the format for log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Initialization code
print("Initializing graph analysis software package...")

from Graph_Processing.graph_creation import Graphs
# # from .analysis import analyze_graph
#
# # Symbol exports
__all__ = ['Graphs']             #from package import *
# #
# # # Submodule imports
# #
# # # Version information
# __version__ = '1.0'
