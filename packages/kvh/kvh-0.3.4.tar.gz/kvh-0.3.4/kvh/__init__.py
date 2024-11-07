__all__ = ["kvh.py"]
from pathlib import Path
__version__=(Path(__file__).parent/"version.txt").read_text().strip()
