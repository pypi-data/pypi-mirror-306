import sys
from pathlib import Path

for item in ["mtmtrain", "mtmlib", "mtmdb", "mtmscreentocode", "mtmai"]:
    sys.path.insert(
        0, str(Path(f"{Path(__file__).resolve().parent}/../../../{item}").resolve())
    )
