from __future__ import annotations

from .models import Theme

# Layout
CANVAS_WIDTH = 1080
LINE_HEIGHT = 20
FONT_SIZE = 16
COLUMN_X = 380  # left edge of the info column
LEADER = 30  # character column where values line up
BAR_CELLS = 66  # language-usage bar width, spans the info column

# Avatar pixel-art
PIXEL_COLS = 48  # avatar width in cells
PIXEL_SIZE = 7  # px per cell
PIXEL_X = 16  # left offset of the portrait

# GitHub Linguist language colors
LANG_COLORS: dict[str, str] = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Python": "#3572A5",
    "Rust": "#dea584",
    "PHP": "#4F5D95",
    "Shell": "#89e051",
    "C++": "#f34b7d",
    "C": "#555555",
    "Go": "#00ADD8",
    "Java": "#b07219",
    "Ruby": "#701516",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "SCSS": "#c6538c",
    "Sass": "#a53b70",
    "Vue": "#41b883",
    "Dockerfile": "#384d54",
    "Makefile": "#427819",
    "Lua": "#000080",
    "Kotlin": "#A97BFF",
    "Swift": "#F05138",
    "Nix": "#7e7eff",
    "Markdown": "#083fa1",
    "TeX": "#3D6117",
    "YAML": "#cb171e",
    "JSON": "#292929",
}
LANG_FALLBACK = "#8b949e"

# Languages rendered on the Markup line instead of Programming
MARKUP_LANGS = frozenset(
    {"HTML", "CSS", "SCSS", "Sass", "Less", "Markdown", "TeX", "Vue"}
)

# Nerd Font icon per field/section
ICONS: dict[str, str] = {
    "Uptime": "",  # clock
    "Host": "",  # building
    "Kernel": "",  # microchip
    "Website": "",  # globe
    "Programming": "",  # code
    "Markup": "",  # book
    "Frameworks": "",  # package
    "Real": "",  # language
    "Software": "",  # rocket
    "Hardware": "",  # wrench
    "Shell": "",  # terminal
    "Terminal": "",  # editor
    "CPU": "",  # coffee
    "Memory": "\U000f035b",  # memory
    "Repos": "",  # repo
    "Stars": "",  # star
    "Followers": "",  # users
    "Following": "",  # user
    "Commits": "",  # git-commit
    "PRs": "",  # git-pull-request
    "Issues": "",  # issue
}

# neofetch ANSI color blocks
BLOCKS_NORMAL = (
    "#484f58",
    "#ff7b72",
    "#3fb950",
    "#d29922",
    "#58a6ff",
    "#bc8cff",
    "#39c5cf",
    "#b1bac4",
)
BLOCKS_BRIGHT = (
    "#6e7681",
    "#ffa198",
    "#56d364",
    "#e3b341",
    "#79c0ff",
    "#d2a8ff",
    "#56d4dd",
    "#f0f6fc",
)

# Themes
DARK = Theme(
    name="dark",
    bg="#161b22",
    fg="#c9d1d9",
    cc="#6e7681",
    key="#ffa657",
    value="#a5d6ff",
    v_floor=0.35,
    v_ceil=1.0,
    px_floor=0.10,
    px_ceil=1.0,
    sat=1.35,
)
LIGHT = Theme(
    name="light",
    bg="#f6f8fa",
    fg="#1f2328",
    cc="#8c959f",
    key="#bc4c00",
    value="#0550ae",
    v_floor=0.0,
    v_ceil=0.62,
    px_floor=0.0,
    px_ceil=0.85,
    sat=1.35,
)
THEMES: tuple[Theme, ...] = (DARK, LIGHT)
