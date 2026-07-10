"""Default behaviour when a flag is omitted (content lives in the workflow).

Frameworks, hobbies, spoken languages and the System section have no sensible
universal default, so they only appear when passed on the CLI. The values
below are structural fallbacks that keep a bare ``python -m neocard`` useful.
"""

DEFAULT_USER = "wielorzeczownik"

# Which API-sourced identity rows to show, in order
DEFAULT_FIELDS = ["uptime", "host", "kernel", "website"]

# Which stats to show, in order
DEFAULT_STATS = [
    "repos",
    "stars",
    "followers",
    "following",
    "commits",
    "prs",
    "issues",
]

# Section order
DEFAULT_SECTIONS = ["identity", "system", "languages", "hobbies", "stats"]

# Language ordering: size (by bytes) or name (alphabetical)
DEFAULT_LANGUAGE_SORT = "size"

# How many languages to list / chart
DEFAULT_PROGRAMMING_LIMIT = 4
DEFAULT_MARKUP_LIMIT = 4
DEFAULT_BAR_TOP = 6
