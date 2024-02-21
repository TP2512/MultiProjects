import re

# Sample string
input_string = """
CELLS OPERATIONAL STATUS
========================
CELL 0 SERVICE STATE=1
CELL 1 SERVICE STATE=1
"""

# Define the regular expression pattern
pattern = r'SERVICE STATE=(\d+)'

# Search for the pattern in the input string
matches = re.findall(pattern, input_string)

# Extract the status values
status_list = [int(match) for match in matches]

# Print the status values
print("Status:", status_list)

