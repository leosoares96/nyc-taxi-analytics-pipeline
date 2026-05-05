import duckdb
from pathlib import Path

def run_analytics(input_path="data/raw/*.csv", output_dir="data/processed"):
    con = duckdb.connect()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # =========================
    # BASE VIEW
    # =========================
    con.execute(f"""
        CREATE OR REPLACE VIEW trips AS
        SELECT *,
            CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_ts,
            CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_ts,
            (epoch(dropoff_ts) - epoch(pickup_ts)) / 60 AS trip_duration_min,
            (total_amount / NULLIF(trip_distance,0)) AS fare_per_km
        FROM read_csv_auto('{input_path}', ignore_errors=true)
    """)

    # =========================
    # FILTRO LIMPO
    # =========================
    con.execute("""
        CREATE OR REPLACE VIEW trips_valid AS
        SELECT *
        FROM trips
        WHERE trip_distance > 0
          AND trip_distance < 1000
          AND total_amount > 0
          AND pickup_ts IS NOT NULL
          AND dropoff_ts IS NOT NULL
          AND trip_duration_min BETWEEN 1 AND 1440
    """)

    # =========================
    # VIEWS ANALÍTICAS
    # =========================
    queries = {

        # =====================
        # PASSAGEIROS
        # =====================
        "by_passenger": """
            SELECT 
                passenger_count AS passageiros,
                COUNT(*) AS total_corridas,
                AVG(trip_distance) AS distancia_media,
                AVG(total_amount) AS ticket_medio,
                SUM(total_amount) AS receita_total
            FROM trips_valid
            GROUP BY passenger_count
        """,

        # =====================
        # MES (BASE PRINCIPAL)
        # =====================
        "by_month": """
            SELECT 
                date_trunc('month', pickup_ts) AS mes,
                COUNT(*) AS total_corridas,
                SUM(total_amount) AS receita_total,
                AVG(total_amount) AS ticket_medio,
                AVG(trip_distance) AS distancia_media
            FROM trips_valid
            GROUP BY mes
            ORDER BY mes
        """,
        # =====================
        # DIA (BASE PRINCIPAL)
        # =====================
        "by_day": """
            SELECT 
                DATE(pickup_ts) AS dia,
                COUNT(*) AS total_corridas,
                SUM(total_amount) AS receita_total,
                AVG(total_amount) AS ticket_medio
            FROM trips_valid
            GROUP BY dia
            ORDER BY dia
        """,

        # =====================
        # SEMANA
        # =====================
        "by_week": """
            SELECT 
                date_trunc('week', pickup_ts) AS semana,
                COUNT(*) AS total_corridas,
                SUM(total_amount) AS receita_total
            FROM trips_valid
            GROUP BY semana
            ORDER BY semana
        """,

        # =====================
        # HORÁRIO (MELHORADO)
        # =====================
        "by_hour": """
            SELECT 
                EXTRACT(hour FROM pickup_ts) AS hora,
                COUNT(*) AS total_corridas,
                SUM(total_amount) AS receita_total,
                AVG(total_amount) AS ticket_medio
            FROM trips_valid
            GROUP BY hora
            ORDER BY hora
        """,

        # =====================
        # TURNOS + PAGAMENTO
        # =====================
        "by_shift_payment": """
            SELECT 
                CASE 
                    WHEN EXTRACT(hour FROM pickup_ts) BETWEEN 6 AND 11 THEN 'Manhã'
                    WHEN EXTRACT(hour FROM pickup_ts) BETWEEN 12 AND 17 THEN 'Tarde'
                    WHEN EXTRACT(hour FROM pickup_ts) BETWEEN 18 AND 23 THEN 'Noite'
                    ELSE 'Madrugada'
                END AS turno,
                payment_type AS forma_pagamento,
                COUNT(*) AS total_corridas,
                SUM(total_amount) AS receita_total
            FROM trips_valid
            GROUP BY turno, payment_type
        """,

        # =====================
        # ROTAS
        # =====================
        "by_route_top100": """
            SELECT 
                pickup_latitude,
                pickup_longitude,
                dropoff_latitude,
                dropoff_longitude,
                COUNT(*) AS total_corridas,
                AVG(total_amount) AS ticket_medio
            FROM trips_valid
            GROUP BY 1,2,3,4
            ORDER BY total_corridas DESC
            LIMIT 100
        """,

        # =====================
        # EFICIÊNCIA (NOVO)
        # =====================
        "route_efficiency": """
            SELECT 
                pickup_latitude,
                pickup_longitude,
                dropoff_latitude,
                dropoff_longitude,
                COUNT(*) AS total_corridas,
                AVG(trip_distance) AS distancia_media,
                AVG(total_amount) AS ticket_medio,
                AVG(fare_per_km) AS receita_por_km
            FROM trips_valid
            GROUP BY 1,2,3,4
        """,

        # =====================
        # SEGMENTAÇÃO DE VIAGENS
        # =====================
        "trip_segments": """
            SELECT 
                CASE 
                    WHEN trip_distance < 2 THEN 'Curta'
                    WHEN trip_distance BETWEEN 2 AND 10 THEN 'Média'
                    ELSE 'Longa'
                END AS segmento_viagem,
                COUNT(*) AS total_corridas,
                AVG(total_amount) AS ticket_medio,
                AVG(trip_duration_min) AS duracao_media
            FROM trips_valid
            GROUP BY segmento_viagem
        """,

        # =====================
        # OUTLIERS (NOVO)
        # =====================
        "outliers": """
            SELECT *
            FROM trips_valid
            WHERE total_amount > (
                SELECT AVG(total_amount) + 3 * STDDEV(total_amount)
                FROM trips_valid
            )
        """
    }

    # =========================
    # EXPORT PARQUET
    # =========================
    paths = {}

    for name, query in queries.items():
        file_path = out / f"{name}.parquet"
        con.execute(f"COPY ({query}) TO '{file_path}' (FORMAT PARQUET)")
        paths[name] = str(file_path.resolve())

    con.close()
    return paths