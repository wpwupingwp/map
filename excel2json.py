#!/usr/bin/python3

import pandas as pd
from sys import argv
from pathlib import Path

excel_file = Path(argv[1])
data = pd.read_excel(excel_file)
data.to_json(excel_file.with_suffix('.json'), orient='records')
