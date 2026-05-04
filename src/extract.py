# python
import shutil
from pathlib import Path
import zipfile
import kagglehub

def extract(dataset="elemento/nyc-yellow-taxi-trip-data", target_dir="data/raw"):
    """
    Função para extrair CSVs do dataset Kaggle para data/raw.
    """
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)

    # Baixa o dataset (espera-se que retorne caminho para arquivo ou diretório)
    returned = kagglehub.dataset_download(dataset)
    if not returned:
        return []

    src = Path(returned)
    extracted = []

    # Caso seja um arquivo ZIP: extrai apenas arquivos .csv para target
    if src.is_file() and zipfile.is_zipfile(src):
        with zipfile.ZipFile(src, "r") as z:
            for member in z.namelist():
                if member.lower().endswith(".csv"):
                    # grava cada CSV diretamente em target com o nome base do arquivo
                    dest_path = target / Path(member).name
                    with z.open(member) as infile, open(dest_path, "wb") as outfile:
                        shutil.copyfileobj(infile, outfile)
                    extracted.append(str(dest_path.resolve()))
        return extracted

    # Caso seja um único arquivo CSV: move para target
    if src.is_file() and src.suffix.lower() == ".csv":
        dest = target / src.name
        shutil.move(str(src), str(dest))
        extracted.append(str(dest.resolve()))
        return extracted

    # Caso seja um diretório: procura por CSVs e move para target
    if src.exists() and src.is_dir():
        for p in src.rglob("*.csv"):
            dest = target / p.name
            shutil.move(str(p), str(dest))
            extracted.append(str(dest.resolve()))
        return extracted

    # Caso não reconhecido: retorna vazio
    return extracted