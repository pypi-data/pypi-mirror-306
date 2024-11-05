import subprocess

project = subprocess.run(
    "hatch project metadata | jq -r .name",
    check = True, capture_output = True, encoding = 'utf-8', shell = True
).stdout.strip()

author = subprocess.run(
    "hatch project metadata | jq -r '.authors[0].name'",
    check = True, capture_output = True, encoding = 'utf-8', shell = True
).stdout.strip()

year = 2024
