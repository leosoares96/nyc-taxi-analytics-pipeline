# 🚕 NYC Taxi Analytics Pipeline

> Study project — built to practise analytical data engineering end to end.

An analytics pipeline over New York City yellow taxi trips: it ingests the public Kaggle
dataset, builds aggregated analytical datasets with **DuckDB**, and serves them through an
interactive **Streamlit** dashboard for urban mobility analysis.

📦 Dataset: https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data

---

## Goal

Turn raw trip records into answerable business questions:

- When is demand highest?
- Is there daily or weekly seasonality?
- Which payment patterns dominate?
- Which routes are the most frequent?
- How does behaviour change by passenger count or shift?

---

## Architecture

```
nyc-taxi-analytics-pipeline/
│
├── app/
│   └── app.py          # Streamlit dashboard
│
├── data/
│   ├── raw/            # original Kaggle CSVs
│   └── processed/      # aggregated Parquet datasets
│
├── src/
│   ├── extract.py      # Kaggle download via kagglehub
│   └── analytics.py    # DuckDB aggregations -> Parquet
│
├── main.py             # pipeline entry point
└── requirements.txt
```

---

## Pipeline

**1. Ingestion** — `src/extract.py` downloads the dataset with `kagglehub`, unpacks it and
stores the raw CSVs under `data/raw/`.

**2. Aggregation** — `src/analytics.py` opens an in-process **DuckDB** connection, reads the
raw CSVs with `read_csv_auto`, and writes one Parquet file per analytical cut to
`data/processed/`:

| Dataset | Grain |
| --- | --- |
| `by_passenger` | passenger count |
| `by_day` | daily metrics |
| `by_week` | weekly metrics |
| `by_month` | monthly metrics |
| `by_hour` | hour of day |
| `by_shift_payment` | shift × payment type |
| `by_route_top100` | 100 most frequent routes |

**3. Serving** — `app/app.py` reads the Parquet datasets with pandas and renders KPIs, time
series, distributions and automatic observations about variability and skew.

---

## Running it

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline (downloads the dataset and builds the Parquet datasets):

```bash
python main.py
```

Start the dashboard:

```bash
streamlit run app/app.py
```

---

## Tech stack

| Area | Tools |
| --- | --- |
| Ingestion | kagglehub |
| Processing | DuckDB, SQL |
| Storage format | Parquet |
| Serving | Streamlit, pandas |

---

## Roadmap

- Orchestrate the pipeline with Airflow
- Model the aggregations as dbt models with tests
- Add data quality validation between the raw and processed layers

---

## License

[MIT](LICENSE)

---

Built by [@leosoares96](https://github.com/leosoares96) · [leosoares96.github.io](https://leosoares96.github.io/)
