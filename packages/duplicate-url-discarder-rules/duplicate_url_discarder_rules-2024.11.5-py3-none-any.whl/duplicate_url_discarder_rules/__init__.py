from glob import glob
from pathlib import Path
from typing import List, Optional

__all__ = [
    "RULE_PATHS",
    "RULE_PATHS_COMMON",
    "RULE_PATHS_ARTICLE",
    "RULE_PATHS_PRODUCT",
]

_current_path = Path(__file__).parent.resolve()
RULE_PATHS: Optional[List[str]] = glob(str(_current_path / "**/*.json"), recursive=True)

RULE_PATHS_COMMON: List[str] = []
RULE_PATHS_ARTICLE: List[str] = []
RULE_PATHS_PRODUCT: List[str] = []

for path in RULE_PATHS or []:
    filename = Path(path).name
    if filename == "article.json":
        RULE_PATHS_ARTICLE.append(path)
    elif filename == "product.json":
        RULE_PATHS_PRODUCT.append(path)
    else:
        RULE_PATHS_COMMON.append(path)

__version__ = "2024.11.05"
