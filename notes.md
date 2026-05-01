# Conceito de Medallion Architecture

A Medallion Architecture é uma forma de organizar dados em camadas para melhorar qualidade, governança e desempenho analítico. Ela divide o pipeline em níveis progressivos, onde os dados passam de brutos para refinados. O objetivo é garantir rastreabilidade, confiabilidade e facilidade de consumo para análises e dashboards.

# Bronze / Silver / Gold

**Bronze**: camada de dados brutos, exatamente como chegam da fonte original, sem tratamento.
**Silver**: dados limpos, padronizados e enriquecidos, com correções e regras de negócio básicas.
**Gold**: dados prontos para consumo, organizados para BI, métricas, dashboards e tomada de decisão.

# Star Schema

**Star Schema** é um modelo de banco analítico onde uma tabela fato central (métricas, como vendas) se conecta a tabelas dimensão (cliente, tempo, produto). Seu formato lembra uma estrela. Ele facilita consultas rápidas, simplifica análises e é muito usado em Data Warehouses.

# DuckDB (fundamentos)

**DuckDB** é um banco de dados analítico leve, rápido e embutido, ideal para análise local de grandes volumes sem precisar de servidor. Ele lê CSV, Parquet e outros formatos diretamente, usando SQL. É muito útil para projetos locais, prototipagem e pipelines modernos.

# DBT (fundamentos)

**DBT (Data Build Tool)** é uma ferramenta para transformar dados usando SQL com versionamento, testes e documentação. Ele permite organizar transformações como código, criando pipelines confiáveis e reutilizáveis. É amplamente usado para estruturar camadas como Silver e Gold.

# Airflow (conceito de DAG)

**Apache Airflow** é uma ferramenta de orquestração que agenda, monitora e automatiza pipelines de dados. Seu conceito principal é a DAG (Directed Acyclic Graph), que define tarefas e dependências entre elas. Assim, processos como ingestão, transformação e carga rodam na ordem correta.
