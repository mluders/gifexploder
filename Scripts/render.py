import sys
import re

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3 or later")

lines = []

with open('./greeting.aepx', 'r') as f:
    lines = f.readlines()

with open('./greeting.aepx', 'w') as f:
    tokens = {
        'name': 'George',
    }

    for i in range(len(lines)):
        for key, value in tokens.items():
            pattern = r"var \$%s.*=.*'.+'" % (key)
            replacement = "var $" + key + " = '" + value + "'"
            lines[i] = re.sub(
                pattern,
                replacement,
                lines[i]
            )

    f.writelines(lines)
