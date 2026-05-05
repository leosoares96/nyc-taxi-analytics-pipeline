from src.extract import extract
from src.analytics import run_analytics

def main():
    print("🔽 Extraindo dados...")
    #extract()

    print("⚙️ Processando com DuckDB...")
    paths = run_analytics()

    print("✔ Pipeline finalizado:")
    for name, path in paths.items():
        print(f" - {name}: {path}")

if __name__ == "__main__":
    main()