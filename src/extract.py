import shutil
from pathlib import Path
import zipfile
import kagglehub
import uuid

def extract(dataset="elemento/nyc-yellow-taxi-trip-data", target_dir="data/raw"):
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)

    returned = kagglehub.dataset_download(dataset)
    if not returned:
        return []

    src = Path(returned)
    extracted = []

    def safe_copy(src_file, target_dir):
        dest = target_dir / f"{src_file.stem}_{uuid.uuid4().hex[:8]}.csv"
        shutil.copy2(src_file, dest)
        return dest

    if src.is_file() and zipfile.is_zipfile(src):
        with zipfile.ZipFile(src, "r") as z:
            for member in z.namelist():
                if member.lower().endswith(".csv"):
                    dest = target / f"{Path(member).stem}_{uuid.uuid4().hex[:8]}.csv"
                    with z.open(member) as infile, open(dest, "wb") as outfile:
                        shutil.copyfileobj(infile, outfile)
                    extracted.append(str(dest.resolve()))
        return extracted

    if src.is_file() and src.suffix.lower() == ".csv":
        dest = safe_copy(src, target)
        extracted.append(str(dest.resolve()))
        return extracted

    if src.exists() and src.is_dir():
        for p in src.rglob("*.csv"):
            dest = safe_copy(p, target)
            extracted.append(str(dest.resolve()))
        return extracted

    return extracted