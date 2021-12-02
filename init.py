#!/usr/bin/env python3

import sys
import os.path
import subprocess
from requests import session
from bs4 import BeautifulSoup

year = 2021
day = int(sys.argv[1])

dir = f"day{day:02}"
os.makedirs(dir)

s = session()
s.cookies["session"] = os.getenv("AOC_SESSION")

r = s.get(f"https://adventofcode.com/{year}/day/{day}")
soup = BeautifulSoup(r.text, features="html.parser")

for code in soup.find_all("code"):
    if code.text.count("\n") >= 5:
        example = code.text.strip()
        break

r = s.get(f"https://adventofcode.com/{year}/day/{day}/input")

open(os.path.join(dir, "input.txt"), "w").write(r.text.strip())

src = f'''#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
{example}
""".splitlines()

src = example

src = [r.strip() for r in src if r.strip()]

'''

runpy = os.path.join(dir, "run.py")

open(runpy, "w").write(src)

subprocess.run(["chmod", "+x", runpy])
