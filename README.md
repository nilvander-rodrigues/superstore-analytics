# Superstore Analytics

Projeto de análise de dados desenvolvido em **Python e Power BI** a partir de dados transacionais da Superstore. O objetivo é transformar o histórico de vendas em uma estrutura analítica reproduzível para compreender o desempenho comercial e operacional, investigar clientes e produtos, avaliar o processamento dos pedidos e construir uma referência de previsão da receita mensal.

O projeto cobre o período de **2015 a 2018** e combina qualidade e preparação de dados, análise exploratória, métricas de negócio, forecasting de séries temporais, visualização executiva em Power BI e geração programática de um relatório analítico em HTML.

---

## Visão Geral

O pipeline foi estruturado para responder a perguntas como:

- Como a receita evoluiu entre 2015 e 2018?
- Quais fatores contribuíram para o crescimento da receita?
- Como a receita está distribuída entre os clientes?
- Qual é a relação entre frequência de compra, ticket médio e valor econômico dos clientes?
- Quais produtos possuem maior impacto econômico?
- Quanto da receita está concentrada nos clientes e produtos de maior valor?
- Como se comporta o tempo entre o registro do pedido e o envio?
- Como esse tempo varia entre as modalidades de envio?
- Um modelo de séries temporais consegue superar um baseline sazonal?
- Qual seria a projeção da receita para os 12 meses seguintes ao histórico?

---

## Principais Resultados

### Performance de Vendas

Entre 2015 e 2018, a Superstore registrou:

- **Receita total:** $2,261,255.41
- **Pedidos distintos:** 4,922
- **Clientes:** 793
- **Ticket médio geral:** $459.42

A receita apresentou retração de **4.20% em 2016**, seguida por crescimento de **30.64% em 2017** e **20.30% em 2018**.

A decomposição da variação da receita mostrou que o crescimento observado nos dois últimos anos foi sustentado principalmente pelo **aumento do volume de pedidos**. Em 2018, por exemplo, os pedidos cresceram **28.26%**, enquanto o ticket médio recuou **6.21%**.

### Clientes

A receita apresenta concentração relevante na base de clientes:

- **Top 10% dos clientes:** 31.16% da receita
- **Top 20% dos clientes:** 48.47% da receita

O perfil **Alta Frequência · Alto Ticket** representa **30.14% dos clientes** e concentra **54.29% da receita**.

Considerando os dois perfis classificados como alto ticket, aproximadamente **50.06% dos clientes concentram 76.75% da receita**.

### Produtos

A análise identificou que `Product ID` isoladamente não funciona como chave analítica única: **32 identificadores estão associados a mais de um `Product Name`**.

Por isso, a análise utiliza a combinação:

`Product ID + Product Name`

Essa definição resulta em **1,893 combinações analíticas de produto**.

A concentração da receita é elevada:

- **Top 10% dos produtos:** 59.11% da receita
- **Top 20% dos produtos:** 77.44% da receita

O produto com maior receita no período foi **Canon imageCLASS 2200 Advanced Copier**, com aproximadamente **$61.6 mil** em receita e presença em apenas cinco pedidos.

### Logística

A análise logística foi realizada na granularidade de **pedido consolidado**.

Resultados principais:

- **Mediana geral até o envio:** 4 dias
- **Same Day:** mediana de 0 dia
- **First Class:** mediana de 2 dias
- **Second Class:** mediana de 3 dias
- **Standard Class:** mediana de 5 dias
- **Standard Class:** 59.83% dos pedidos
- **Pedidos na faixa de 6–7 dias:** 18.02%

Esses valores representam **tempo de processamento até o envio**. Eles não são classificados como atrasos porque o dataset não contém prazo prometido, SLA ou data efetiva de entrega.

---

## Forecasting

A receita foi agregada mensalmente, produzindo uma série temporal com **48 observações**, entre janeiro de 2015 e dezembro de 2018.

A avaliação foi realizada cronologicamente:

- **Treino:** 36 meses — 2015 a 2017
- **Teste:** 12 meses — 2018

Um **Seasonal Naive** foi utilizado como baseline e comparado a um modelo **Holt-Winters** com tendência e sazonalidade aditivas e periodicidade anual.

| Modelo | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Seasonal Naive | $15,444.18 | $18,932.10 | 24.86% |
| Holt-Winters | $11,384.97 | $12,429.52 | 22.73% |

Em relação ao baseline, o Holt-Winters apresentou:

- **Redução do MAE:** 26.28%
- **Redução do RMSE:** 34.35%
- **Redução do MAPE:** 8.58%

Após a avaliação fora da amostra, o modelo foi reajustado com as 48 observações disponíveis e utilizado para projetar 2019.

**Receita projetada para 2019: $898,941.86**

A projeção representa uma referência analítica condicionada ao histórico disponível e não deve ser interpretada como resultado realizado ou meta garantida.

---

## Arquitetura do Projeto

O fluxo principal é:

```text
Excel (Raw Data)
        ↓
Data Quality
        ↓
Data Preparation
        ↓
Parquet (Processed Data)
        ↓
Exploratory Data Analysis
        ↓
Business Analysis
        ↓
Time Series Forecasting
        ↓
Power BI + HTML Analytical Report + Documentation
```

A arquitetura separa responsabilidades entre armazenamento, preparação, análise, modelagem e apresentação.

A base processada em Parquet funciona como **fonte analítica comum** para os notebooks posteriores e para a geração do relatório HTML.

---

## Estrutura do Repositório

```text
superstore-analytics/
│
├── data/
│   ├── raw/
│   │   └── sales_data.xlsx
│   └── processed/
│       └── sales_data_clean.parquet
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_data_preparation.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_sales_analysis.ipynb
│   ├── 05_customer_analysis.ipynb
│   ├── 06_product_analysis.ipynb
│   ├── 07_logistics_analysis.ipynb
│   └── 08_time_series_forecasting.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   └── metrics.py
│
├── templates/
│   └── analytical_report.html
│
├── outputs/
│   └── report/
│       └── superstore_analytics_report.html
│
├── reports/
│   ├── executive_summary.md
│   └── technical_documentation.md
│
├── generate_report.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Notebooks

| Notebook | Responsabilidade |
|---|---|
| `01_data_quality.ipynb` | Avaliação inicial da qualidade, schema, valores ausentes, duplicidades e consistência dos dados |
| `02_data_preparation.ipynb` | Limpeza, padronização, criação de variáveis e persistência da base processada |
| `03_eda.ipynb` | Análise exploratória, distribuições, comportamento temporal, valores extremos e relações iniciais |
| `04_sales_analysis.ipynb` | KPIs comerciais, evolução anual, YoY e decomposição da variação da receita |
| `05_customer_analysis.ipynb` | Receita, frequência, ticket médio, concentração e perfis econômicos dos clientes |
| `06_product_analysis.ipynb` | Chave analítica de produto, concentração da receita e produtos de maior impacto |
| `07_logistics_analysis.ipynb` | Tempo de processamento até o envio e comportamento por modalidade |
| `08_time_series_forecasting.ipynb` | Baseline sazonal, Holt-Winters, avaliação fora da amostra e projeção para 2019 |

---

## Módulos Python

### `src/data_cleaning.py`

Centraliza transformações determinísticas utilizadas na preparação dos dados, incluindo:

- conversão e padronização das datas;
- tratamento de `Postal Code`;
- identificação/remoção de duplicidades de negócio quando aplicável;
- orquestração das regras de limpeza.

### `src/metrics.py`

Centraliza regras analíticas reutilizáveis:

- `calculate_iqr_bounds()`
- `decompose_revenue_change()`
- `calculate_top_concentration()`
- `calculate_forecast_metrics()`

A separação entre notebooks e módulos evita duplicação de regras e mantém as definições analíticas reutilizáveis em um único local.

---

## Granularidade e Contratos Analíticos

A base processada mantém a granularidade original de **item de pedido (line item)**.

Dependendo da pergunta de negócio, outras granularidades são construídas:

| Análise | Granularidade |
|---|---|
| Base processada / EDA | Item de pedido |
| Ticket médio e logística | Pedido (`Order ID`) |
| Clientes | Cliente (`Customer ID`) |
| Produtos | `Product ID + Product Name` |
| Forecasting | Mês |

Mudanças de granularidade são acompanhadas por controles de reconciliação para evitar duplicação ou perda indevida de receita.

---

## Qualidade e Validação

O projeto utiliza *quality gates* distribuídos ao longo do pipeline.

Entre os principais controles estão:

- inspeção de valores ausentes e duplicidades;
- validação de tipos e estrutura dos dados;
- reconciliação da receita após transformações;
- validação das granularidades derivadas;
- verificação da consistência logística dentro de cada `Order ID`;
- validação da série temporal mensal;
- separação cronológica entre treino e teste;
- comparação do modelo de forecasting contra um baseline;
- validações internas nas funções reutilizáveis;
- execução dos notebooks utilizando **Restart Kernel → Run All**;
- validação sintática dos módulos Python com `py_compile`;
- regeneração e validação do relatório HTML.

A base processada final contém **9,799 registros e 19 colunas**.

Foram identificados **11 valores ausentes em `Postal Code`**, preservados porque não comprometem as principais métricas utilizadas no projeto. Não foram identificadas duplicidades de negócio que justificassem a remoção de registros.

---

## Relatório Analítico HTML

Além dos notebooks e do Power BI, o projeto gera um relatório analítico estático e autocontido:

```text
outputs/report/superstore_analytics_report.html
```

O relatório é construído por `generate_report.py` utilizando **Jinja2** e o template:

```text
templates/analytical_report.html
```

Os gráficos são gerados com Matplotlib e incorporados ao HTML em Base64, permitindo abrir o relatório sem depender de arquivos de imagem externos.

O documento consolida:

1. Visão Executiva
2. Performance de Vendas
3. Clientes
4. Produtos
5. Logística
6. Forecasting
7. Conclusões e Limitações

O relatório possui navegação interna, layout responsivo e mantém uma apresentação independente dos notebooks.

---

## Power BI

O **Power BI** é utilizado como camada de visualização executiva e exploração interativa.

A separação de responsabilidades adotada no projeto é:

**Python**
- preparação dos dados;
- validações;
- métricas e análises;
- forecasting;
- geração do relatório HTML.

**Power BI**
- comunicação visual;
- exploração interativa;
- acompanhamento executivo dos indicadores.

Essa abordagem evita utilizar a ferramenta de visualização como substituta das regras analíticas previamente definidas e validadas no pipeline Python.

---

## Decisões Técnicas: Python × DAX

### 1. Quais foram as principais diferenças percebidas entre o processamento em DAX e a execução de scripts Python no Power BI?

Neste projeto, optei por concentrar o processamento e as análises em **Python**, utilizando o Power BI principalmente como camada de visualização. Por isso, a comparação não foi feita executando exatamente os mesmos cálculos em DAX e Python.

A principal diferença está no papel de cada tecnologia. O **DAX** é voltado principalmente para criação de medidas e cálculos dentro do modelo semântico do Power BI, respondendo ao contexto de filtros aplicado aos visuais. Já o **Python** oferece maior liberdade para preparação dos dados, análises estatísticas, validações e modelagem.

No projeto, Python permitiu centralizar regras reutilizáveis, realizar controles de qualidade e reconciliação e desenvolver o modelo de forecasting antes de os resultados chegarem à camada de apresentação.

### 2. Em qual cenário de negócios você optaria por utilizar Python em vez de DAX para preparar ou avaliar esse tipo de dado?

Eu utilizaria **Python** quando a necessidade ultrapassasse a construção de indicadores para o dashboard, principalmente em situações que envolvessem preparação e validação mais complexa dos dados, análises estatísticas, avaliação de valores extremos, forecasting, machine learning, automação ou criação de pipelines reproduzíveis.

Neste projeto, Python foi adequado para avaliar a qualidade dos dados, preparar a base, analisar clientes e produtos, validar diferentes granularidades e desenvolver o forecasting com Holt-Winters.

Já utilizaria **DAX** principalmente para medidas que precisam responder dinamicamente aos filtros e interações do relatório no Power BI.

### 3. Como a presença de valores nulos (NULL/NaN) afetou os cálculos em cada uma das linguagens?

No **Python/pandas**, valores ausentes podem ser representados por `NaN`, `NaT` ou `pd.NA`, dependendo do tipo de dado. Eles precisam ser considerados durante a preparação e validação porque podem influenciar agregações, conversões e cálculos.

Neste projeto foram identificados **11 valores ausentes em `Postal Code`**. Eles foram preservados porque não comprometiam as principais métricas comerciais analisadas. A decisão foi tomada considerando o significado e o impacto analítico do campo, em vez de simplesmente eliminar registros com valores ausentes.

No **DAX**, valores ausentes são normalmente tratados como `BLANK()`. Dependendo da medida e da função utilizada, `BLANK()` pode apresentar comportamento diferente de zero. Portanto, também é importante distinguir ausência de informação de um valor efetivamente igual a zero.

A principal conclusão é que, independentemente da tecnologia utilizada, valores nulos devem ser avaliados considerando seu significado e impacto sobre a análise antes de qualquer decisão de remoção ou preenchimento.

## Tecnologias

- **Python 3.12.10**
- **pandas**
- **NumPy**
- **Matplotlib**
- **PyArrow**
- **openpyxl**
- **statsmodels**
- **Jinja2**
- **Jupyter / IPython**
- **Power BI**
- **Parquet**
- **VS Code**
- **Git / GitHub**

As versões exatas das dependências Python estão registradas em `requirements.txt`.

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone <https://github.com/nilvander-rodrigues/superstore-analytics.git>
cd superstore-analytics
```

### 2. Criar o ambiente virtual

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o pipeline analítico

Os notebooks devem ser executados sequencialmente:

```text
01_data_quality.ipynb
        ↓
02_data_preparation.ipynb
        ↓
03_eda.ipynb
        ↓
04_sales_analysis.ipynb
        ↓
05_customer_analysis.ipynb
        ↓
06_product_analysis.ipynb
        ↓
07_logistics_analysis.ipynb
        ↓
08_time_series_forecasting.ipynb
```

A partir do notebook `03`, as análises utilizam a base processada:

```text
data/processed/sales_data_clean.parquet
```

### 5. Gerar o relatório HTML

Na raiz do projeto:

```bash
python generate_report.py
```

O arquivo será gerado em:

```text
outputs/report/superstore_analytics_report.html
```

Abra esse arquivo em um navegador para visualizar o relatório consolidado.

---

## Reprodutibilidade

O projeto foi estruturado para permitir reconstruir o fluxo a partir dos dados de origem.

Os principais elementos de reprodutibilidade são:

- dataset original preservado em `data/raw/`;
- base processada persistida em Parquet;
- notebooks numerados em ordem de execução;
- funções reutilizáveis centralizadas em `src/`;
- ambiente virtual isolado;
- dependências versionadas em `requirements.txt`;
- caminhos relativos à raiz do projeto;
- validações e reconciliações ao longo do pipeline;
- relatório HTML gerado programaticamente.

---

## Limitações

Os resultados devem ser interpretados dentro do escopo dos dados disponíveis.

- O dataset permite analisar **receita**, mas não contém informações suficientes sobre custos, margem ou lucro.
- Não existem dados de SLA, prazo prometido ou data efetiva de entrega; portanto, os tempos logísticos não devem ser interpretados diretamente como atrasos.
- A análise de clientes não incorpora custo de aquisição, campanhas, canais de relacionamento ou custos de atendimento.
- A análise de produtos não contém estoque, custo, margem ou disponibilidade.
- A série temporal contém apenas **48 observações mensais e quatro ciclos anuais**.
- A avaliação do forecasting utiliza uma única janela de teste de 12 meses.
- O modelo utiliza apenas o histórico da receita e não incorpora variáveis externas.
- A projeção para 2019 é uma estimativa condicionada aos padrões históricos e não uma garantia de desempenho futuro.

---

## Documentação

Para uma visão executiva dos resultados:

```text
reports/executive_summary.md
```

Para detalhes sobre arquitetura, granularidade, contratos analíticos, validações e decisões técnicas:

```text
reports/technical_documentation.md
```

Para uma apresentação consolidada dos resultados:

```text
outputs/report/superstore_analytics_report.html
```

---

## Conclusão

O **Superstore Analytics** demonstra um fluxo analítico completo, desde a avaliação e preparação dos dados até análises de negócio, forecasting e apresentação dos resultados.

Mais do que produzir visualizações, o projeto enfatiza **granularidade correta, qualidade dos dados, reconciliação de métricas, modularização, validação temporal e reprodutibilidade**.

Os resultados mostram crescimento recente da receita sustentado principalmente pelo aumento do volume de pedidos, concentração econômica relevante entre clientes e produtos, diferenças claras no tempo de processamento entre modalidades de envio e ganho preditivo do Holt-Winters em relação ao baseline sazonal utilizado na avaliação.

A combinação de **Python, Power BI e relatório HTML** permite apresentar os resultados em diferentes níveis: análise técnica reproduzível, exploração executiva interativa e relatório analítico portátil.
