import re


def ext_player(filename):
    pattern = re.compile(r'p(\d)')
    match = pattern.search(filename)
    if match:
        return int(match.group(1))


filename = "999t6p65.csv"
# Define a regular expression pattern to match the winning player number
print("result: ", ext_player(filename))
# pattern = re.compile(r'p(\d)')

# # Use the pattern to find the winning player number in the filename
# match = pattern.search(filename)

# # Extract the player number if the pattern is found
# if match:
#     winning_player = int(match.group(1))
#     print("Winning Player:", winning_player)
# else:
#     print("No match found.")