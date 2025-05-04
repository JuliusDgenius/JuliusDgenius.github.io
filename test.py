import json
from pathlib import Path

with Path('portfolio-julius.json').open(encoding='utf-8') as f:
    data = json.load(f)

for line in data:
    print(line)