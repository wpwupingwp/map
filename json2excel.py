#!/usr/bin/python3

import pandas as pd
import json
from sys import argv
from pathlib import Path

json_file = Path(argv[1])
with open(json_file, 'r', encoding='utf-8') as raw:
    data = json.load(raw)
a = pd.read_json(argv[1])
a.to_excel(json_file.with_suffix('.xlsx'), index=False)


