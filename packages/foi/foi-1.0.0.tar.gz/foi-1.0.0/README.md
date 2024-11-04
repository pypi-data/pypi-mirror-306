# Description

files of interest (foi) - Identifies files based on their file type

# Installation

`pip install foi`

# Usage

**From command line:**

`python -m foi [-h] --path PATH [--files FILES]`

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--path | -p | String | - | Path which shall be searched |
|--files | -f | String[] | [txt, pdf, png, jpg] | Comma separated list of file type to be searched for: pdf,jpg,txt |

**Programmatically:**

```python

from foi.search.Search import Search

s = Search(["md", "txt"]) # Provide the file types you are interested in
files = s.getFilePaths("path/to/dir")  # The path which shalle be searched for
                                       # the given file types

# Print findings
for file in files:
    print(file)
```


# Example

`python -m foi -p path/to/dir -f txt`

```
################################################################################

NPDEP - Network Protocol Data Exfiltration Project
foi - files of interest
Identifies files based on their file type

Current working directory: path/to/dir

Datetime: 10/10/1970 10:10:10

################################################################################

Files to be searched: ['txt']

Path: path/to/dir

Files found:
---
path/to/dir/example.txt
path/to/dir/test.txt

################################################################################

Execution Time: 0.005753 sec
```