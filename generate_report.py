"""
Geração do relatório analítico HTML do projeto Superstore Analytics.

O script utiliza a camada de dados processados para calcular os
indicadores do relatório e renderizar o template HTML com Jinja2.
"""

import base64
import math
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from jinja2 import Environment, FileSystemLoader


# ---------------------------------------------------------------------
# Caminhos do projeto
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sales_data_clean.parquet"
)

TEMPLATE_DIR = PROJECT_ROOT / "templates"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "report"

OUTPUT_PATH = OUTPUT_DIR / "superstore_analytics_report.html"


# ---------------------------------------------------------------------
# Carregamento dos dados
# ---------------------------------------------------------------------

df = pd.read_parquet(DATA_PATH)


# =====================================================================
# 1. INDICADORES EXECUTIVOS
# =====================================================================

total_revenue = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

average_order_value = (
    total_revenue
    / total_orders
)


# =====================================================================
# 2. PERFORMANCE DE VENDAS
# =====================================================================

annual_sales = (
    df.assign(Year=df["Order Date"].dt.year)
    .groupby("Year")
    .agg(
        Revenue=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Customers=("Customer ID", "nunique"),
    )
    .reset_index()
)

annual_sales["Average Order Value"] = (
    annual_sales["Revenue"]
    / annual_sales["Orders"]
)

annual_sales["Revenue YoY"] = (
    annual_sales["Revenue"]
    .pct_change()
)


# ---------------------------------------------------------------------
# Validação da tabela anual
# ---------------------------------------------------------------------

annual_revenue_check = annual_sales["Revenue"].sum()

if not abs(annual_revenue_check - total_revenue) < 0.01:
    raise ValueError(
        "A receita anual não reconcilia com a receita total do dataset."
    )


# ---------------------------------------------------------------------
# Tabela anual para apresentação
# ---------------------------------------------------------------------

annual_sales_table = []

for _, row in annual_sales.iterrows():
    annual_sales_table.append(
        {
            "year": int(row["Year"]),
            "revenue": f'${row["Revenue"]:,.2f}',
            "orders": f'{int(row["Orders"]):,}',
            "average_order_value": (
                f'${row["Average Order Value"]:,.2f}'
            ),
            "revenue_yoy": (
                "—"
                if pd.isna(row["Revenue YoY"])
                else f'{row["Revenue YoY"]:.2%}'
            ),
        }
    )


# ---------------------------------------------------------------------
# Gráfico anual de receita
# ---------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 4.8))

ax.plot(
    annual_sales["Year"],
    annual_sales["Revenue"],
    marker="o",
    linewidth=2,
)

ax.set_title(
    "Evolução Anual da Receita",
    loc="left",
    fontsize=14,
    fontweight="bold",
)

ax.set_xlabel("Ano")
ax.set_ylabel("Receita (USD)")
ax.set_xticks(annual_sales["Year"])

ax.grid(
    axis="y",
    alpha=0.2,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for year, revenue in zip(
    annual_sales["Year"],
    annual_sales["Revenue"],
):
    ax.annotate(
        f"${revenue / 1000:,.0f}k",
        (year, revenue),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
    )

fig.tight_layout()

chart_buffer = BytesIO()

fig.savefig(
    chart_buffer,
    format="png",
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

chart_buffer.seek(0)

annual_revenue_chart = base64.b64encode(
    chart_buffer.getvalue()
).decode("utf-8")

chart_buffer.close()


# =====================================================================
# 3. ANÁLISE DE CLIENTES
# =====================================================================

customer_analysis = (
    df.groupby("Customer ID")
    .agg(
        Revenue=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
    )
    .reset_index()
)

customer_analysis["Average Order Value"] = (
    customer_analysis["Revenue"]
    / customer_analysis["Orders"]
)


# ---------------------------------------------------------------------
# Validação da análise de clientes
# ---------------------------------------------------------------------

customer_revenue_check = customer_analysis["Revenue"].sum()

if not abs(customer_revenue_check - total_revenue) < 0.01:
    raise ValueError(
        "A receita por cliente não reconcilia com a receita total."
    )

if len(customer_analysis) != total_customers:
    raise ValueError(
        "A quantidade de clientes não reconcilia com o total do dataset."
    )


# ---------------------------------------------------------------------
# Concentração da receita por cliente
# ---------------------------------------------------------------------

customers_ranked = customer_analysis.sort_values(
    "Revenue",
    ascending=False,
).reset_index(drop=True)

top_10_count = math.ceil(
    len(customers_ranked) * 0.10
)

top_20_count = math.ceil(
    len(customers_ranked) * 0.20
)

top_10_revenue_share = (
    customers_ranked
    .head(top_10_count)["Revenue"]
    .sum()
    / total_revenue
)

top_20_revenue_share = (
    customers_ranked
    .head(top_20_count)["Revenue"]
    .sum()
    / total_revenue
)


# ---------------------------------------------------------------------
# Perfis econômicos de clientes
# ---------------------------------------------------------------------

median_orders = customer_analysis["Orders"].median()

median_aov = customer_analysis[
    "Average Order Value"
].median()


def classify_customer(row):
    high_frequency = row["Orders"] >= median_orders

    high_ticket = (
        row["Average Order Value"] >= median_aov
    )

    if high_frequency and high_ticket:
        return "Alta Frequência · Alto Ticket"

    if not high_frequency and high_ticket:
        return "Menor Frequência · Alto Ticket"

    if high_frequency and not high_ticket:
        return "Alta Frequência · Menor Ticket"

    return "Menor Frequência · Menor Ticket"


customer_analysis["Profile"] = (
    customer_analysis.apply(
        classify_customer,
        axis=1,
    )
)

customer_profiles = (
    customer_analysis
    .groupby("Profile")
    .agg(
        Customers=("Customer ID", "nunique"),
        Revenue=("Revenue", "sum"),
        Average_Orders=("Orders", "mean"),
        Average_AOV=("Average Order Value", "mean"),
    )
    .reset_index()
)

customer_profiles["Customer Share"] = (
    customer_profiles["Customers"]
    / total_customers
)

customer_profiles["Revenue Share"] = (
    customer_profiles["Revenue"]
    / total_revenue
)


# ---------------------------------------------------------------------
# Ordem analítica dos perfis
# ---------------------------------------------------------------------

profile_order = [
    "Alta Frequência · Alto Ticket",
    "Menor Frequência · Alto Ticket",
    "Alta Frequência · Menor Ticket",
    "Menor Frequência · Menor Ticket",
]

customer_profiles["Profile"] = pd.Categorical(
    customer_profiles["Profile"],
    categories=profile_order,
    ordered=True,
)

customer_profiles = (
    customer_profiles
    .sort_values("Profile")
    .reset_index(drop=True)
)


# ---------------------------------------------------------------------
# Validação dos perfis de clientes
# ---------------------------------------------------------------------

if customer_profiles["Customers"].sum() != total_customers:
    raise ValueError(
        "Os perfis não reconciliam com o total de clientes."
    )

profile_revenue_check = customer_profiles["Revenue"].sum()

if not abs(profile_revenue_check - total_revenue) < 0.01:
    raise ValueError(
        "A receita dos perfis não reconcilia com a receita total."
    )


# ---------------------------------------------------------------------
# Tabela de clientes para apresentação
# ---------------------------------------------------------------------

customer_profiles_table = []

for _, row in customer_profiles.iterrows():
    customer_profiles_table.append(
        {
            "profile": str(row["Profile"]),
            "customers": f'{int(row["Customers"]):,}',
            "customer_share": (
                f'{row["Customer Share"]:.2%}'
            ),
            "revenue": f'${row["Revenue"]:,.2f}',
            "revenue_share": (
                f'{row["Revenue Share"]:.2%}'
            ),
        }
    )


# ---------------------------------------------------------------------
# Indicadores consolidados de clientes
# ---------------------------------------------------------------------

high_ticket_profiles = customer_profiles[
    customer_profiles["Profile"].isin(
        [
            "Alta Frequência · Alto Ticket",
            "Menor Frequência · Alto Ticket",
        ]
    )
]

high_ticket_customer_share = (
    high_ticket_profiles["Customers"].sum()
    / total_customers
)

high_ticket_revenue_share = (
    high_ticket_profiles["Revenue"].sum()
    / total_revenue
)


# =====================================================================
# 4. ANÁLISE DE PRODUTOS
# =====================================================================

product_analysis = (
    df.groupby(
        ["Product ID", "Product Name"],
        as_index=False,
    )
    .agg(
        Revenue=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
    )
)

product_analysis["Average Revenue per Order"] = (
    product_analysis["Revenue"]
    / product_analysis["Orders"]
)


# ---------------------------------------------------------------------
# Validação da análise de produtos
# ---------------------------------------------------------------------

product_revenue_check = product_analysis["Revenue"].sum()

if not abs(product_revenue_check - total_revenue) < 0.01:
    raise ValueError(
        "A receita por produto não reconcilia com a receita total."
    )

total_product_combinations = len(product_analysis)


# ---------------------------------------------------------------------
# Concentração da receita por produto
# ---------------------------------------------------------------------

products_ranked = product_analysis.sort_values(
    "Revenue",
    ascending=False,
).reset_index(drop=True)

top_10_product_count = math.ceil(
    total_product_combinations * 0.10
)

top_20_product_count = math.ceil(
    total_product_combinations * 0.20
)

top_10_product_revenue_share = (
    products_ranked
    .head(top_10_product_count)["Revenue"]
    .sum()
    / total_revenue
)

top_20_product_revenue_share = (
    products_ranked
    .head(top_20_product_count)["Revenue"]
    .sum()
    / total_revenue
)


# ---------------------------------------------------------------------
# Top produtos por receita
# ---------------------------------------------------------------------

top_products = products_ranked.head(10).copy()

top_products["Revenue Share"] = (
    top_products["Revenue"]
    / total_revenue
)


# ---------------------------------------------------------------------
# Tabela de produtos para apresentação
# ---------------------------------------------------------------------

top_products_table = []

for _, row in top_products.iterrows():
    top_products_table.append(
        {
            "product_name": row["Product Name"],
            "orders": f'{int(row["Orders"]):,}',
            "revenue": f'${row["Revenue"]:,.2f}',
            "revenue_share": f'{row["Revenue Share"]:.2%}',
        }
    )


# =====================================================================
# 5. ANÁLISE LOGÍSTICA
# =====================================================================

# ---------------------------------------------------------------------
# Consistência das informações dentro de cada pedido
# ---------------------------------------------------------------------

logistics_consistency = (
    df.groupby("Order ID")
    .agg(
        Order_Date_Values=("Order Date", "nunique"),
        Ship_Date_Values=("Ship Date", "nunique"),
        Ship_Mode_Values=("Ship Mode", "nunique"),
        Shipping_Days_Values=("Shipping Days", "nunique"),
    )
)

logistics_conflicts = (
    logistics_consistency > 1
).any(axis=1).sum()

if logistics_conflicts != 0:
    raise ValueError(
        f"Foram encontrados {logistics_conflicts} pedidos "
        "com informações logísticas inconsistentes."
    )


# ---------------------------------------------------------------------
# Consolidação na granularidade de pedido
# ---------------------------------------------------------------------

order_logistics = (
    df.groupby("Order ID")
    .agg(
        Order_Date=("Order Date", "first"),
        Ship_Date=("Ship Date", "first"),
        Ship_Mode=("Ship Mode", "first"),
        Shipping_Days=("Shipping Days", "first"),
    )
    .reset_index()
)

if len(order_logistics) != total_orders:
    raise ValueError(
        "A quantidade de pedidos na análise logística "
        "não reconcilia com o total de pedidos."
    )


# ---------------------------------------------------------------------
# Distribuição geral do tempo de processamento
# ---------------------------------------------------------------------

shipping_days_median = (
    order_logistics["Shipping_Days"].median()
)

upper_processing_orders = (
    order_logistics["Shipping_Days"] > 5
).sum()

upper_processing_share = (
    upper_processing_orders
    / total_orders
)


# ---------------------------------------------------------------------
# Performance por modalidade de envio
# ---------------------------------------------------------------------

shipping_mode_analysis = (
    order_logistics
    .groupby("Ship_Mode")
    .agg(
        Orders=("Order ID", "nunique"),
        Mean_Days=("Shipping_Days", "mean"),
        Median_Days=("Shipping_Days", "median"),
        Min_Days=("Shipping_Days", "min"),
        Max_Days=("Shipping_Days", "max"),
    )
    .reset_index()
)

shipping_mode_analysis["Order Share"] = (
    shipping_mode_analysis["Orders"]
    / total_orders
)


# ---------------------------------------------------------------------
# Ordem analítica das modalidades
# ---------------------------------------------------------------------

shipping_mode_order = [
    "Same Day",
    "First Class",
    "Second Class",
    "Standard Class",
]

shipping_mode_analysis["Ship_Mode"] = pd.Categorical(
    shipping_mode_analysis["Ship_Mode"],
    categories=shipping_mode_order,
    ordered=True,
)

shipping_mode_analysis = (
    shipping_mode_analysis
    .sort_values("Ship_Mode")
    .reset_index(drop=True)
)


# ---------------------------------------------------------------------
# Validação das modalidades
# ---------------------------------------------------------------------

if shipping_mode_analysis["Orders"].sum() != total_orders:
    raise ValueError(
        "As modalidades de envio não reconciliam "
        "com o total de pedidos."
    )


# ---------------------------------------------------------------------
# Tabela logística para apresentação
# ---------------------------------------------------------------------

shipping_mode_table = []

for _, row in shipping_mode_analysis.iterrows():
    shipping_mode_table.append(
        {
            "ship_mode": str(row["Ship_Mode"]),
            "orders": f'{int(row["Orders"]):,}',
            "order_share": f'{row["Order Share"]:.2%}',
            "median_days": f'{row["Median_Days"]:.0f}',
            "mean_days": f'{row["Mean_Days"]:.2f}',
            "range": (
                f'{row["Min_Days"]:.0f}–'
                f'{row["Max_Days"]:.0f}'
            ),
        }
    )


# ---------------------------------------------------------------------
# Participação do Standard Class
# ---------------------------------------------------------------------

standard_class_share = (
    shipping_mode_analysis.loc[
        shipping_mode_analysis["Ship_Mode"].astype(str)
        == "Standard Class",
        "Order Share",
    ]
    .iloc[0]
)


# ---------------------------------------------------------------------
# Gráfico da mediana de dias por modalidade
# ---------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 4.8))

ax.bar(
    shipping_mode_analysis["Ship_Mode"].astype(str),
    shipping_mode_analysis["Median_Days"],
)

ax.set_title(
    "Mediana de Dias até o Envio por Modalidade",
    loc="left",
    fontsize=14,
    fontweight="bold",
)

ax.set_xlabel("Modalidade de Envio")
ax.set_ylabel("Dias")

ax.grid(
    axis="y",
    alpha=0.2,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for index, value in enumerate(
    shipping_mode_analysis["Median_Days"]
):
    ax.annotate(
        f"{value:.0f}",
        (index, value),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        fontsize=9,
    )

fig.tight_layout()


# ---------------------------------------------------------------------
# Conversão do gráfico para Base64
# ---------------------------------------------------------------------

chart_buffer = BytesIO()

fig.savefig(
    chart_buffer,
    format="png",
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

chart_buffer.seek(0)

shipping_mode_chart = base64.b64encode(
    chart_buffer.getvalue()
).decode("utf-8")

chart_buffer.close()

# =====================================================================
# 6. FORECASTING
# =====================================================================

# ---------------------------------------------------------------------
# Série temporal mensal
# ---------------------------------------------------------------------

monthly_revenue = (
    df.set_index("Order Date")
    .resample("MS")["Sales"]
    .sum()
)

if len(monthly_revenue) != 48:
    raise ValueError(
        "A série temporal deveria conter 48 observações mensais."
    )

if monthly_revenue.isna().any():
    raise ValueError(
        "A série temporal contém meses sem valor de receita."
    )

if not abs(monthly_revenue.sum() - total_revenue) < 0.01:
    raise ValueError(
        "A receita mensal não reconcilia com a receita total."
    )


# ---------------------------------------------------------------------
# Separação treino e teste
# ---------------------------------------------------------------------

train = monthly_revenue.iloc[:36]
test = monthly_revenue.iloc[36:]


# ---------------------------------------------------------------------
# Baseline sazonal
# ---------------------------------------------------------------------

seasonal_naive = train.iloc[-12:].copy()

seasonal_naive.index = test.index


# ---------------------------------------------------------------------
# Função de métricas
# ---------------------------------------------------------------------

def calculate_forecast_metrics(actual, predicted):
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    mae = np.mean(
        np.abs(actual - predicted)
    )

    rmse = np.sqrt(
        np.mean((actual - predicted) ** 2)
    )

    mape = np.mean(
        np.abs(
            (actual - predicted)
            / actual
        )
    ) * 100

    return mae, rmse, mape


baseline_mae, baseline_rmse, baseline_mape = (
    calculate_forecast_metrics(
        test,
        seasonal_naive,
    )
)


# ---------------------------------------------------------------------
# Holt-Winters
# ---------------------------------------------------------------------

holt_winters_model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=12,
).fit()

holt_winters_test_forecast = (
    holt_winters_model.forecast(12)
)

hw_mae, hw_rmse, hw_mape = (
    calculate_forecast_metrics(
        test,
        holt_winters_test_forecast,
    )
)


# ---------------------------------------------------------------------
# Ganho em relação ao baseline
# ---------------------------------------------------------------------

mae_reduction = (
    1
    - hw_mae / baseline_mae
)

rmse_reduction = (
    1
    - hw_rmse / baseline_rmse
)

mape_reduction = (
    1
    - hw_mape / baseline_mape
)


# ---------------------------------------------------------------------
# Modelo final utilizando toda a série histórica
# ---------------------------------------------------------------------

final_forecast_model = ExponentialSmoothing(
    monthly_revenue,
    trend="add",
    seasonal="add",
    seasonal_periods=12,
).fit()

forecast_2019 = (
    final_forecast_model.forecast(12)
)

forecast_2019_total = forecast_2019.sum()
forecast_2019_average = forecast_2019.mean()

forecast_peak_month = (
    forecast_2019.idxmax()
)

forecast_peak_value = (
    forecast_2019.max()
)


# ---------------------------------------------------------------------
# Tabela mensal da projeção
# ---------------------------------------------------------------------

forecast_table = []

for date, value in forecast_2019.items():
    forecast_table.append(
        {
            "month": date.strftime("%b %Y"),
            "forecast": f"${value:,.2f}",
        }
    )


# ---------------------------------------------------------------------
# Gráfico histórico + projeção
# ---------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    label="Receita Histórica",
    linewidth=2,
)

ax.plot(
    forecast_2019.index,
    forecast_2019.values,
    label="Forecast 2019",
    linewidth=2,
    linestyle="--",
)

ax.axvline(
    monthly_revenue.index[-1],
    linestyle=":",
    alpha=0.6,
)

ax.set_title(
    "Receita Mensal Histórica e Forecast 2019",
    loc="left",
    fontsize=14,
    fontweight="bold",
)

ax.set_xlabel("Período")
ax.set_ylabel("Receita (USD)")

ax.grid(
    axis="y",
    alpha=0.2,
)

ax.legend(
    frameon=False,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()


# ---------------------------------------------------------------------
# Conversão do gráfico para Base64
# ---------------------------------------------------------------------

chart_buffer = BytesIO()

fig.savefig(
    chart_buffer,
    format="png",
    dpi=150,
    bbox_inches="tight",
)

plt.close(fig)

chart_buffer.seek(0)

forecast_chart = base64.b64encode(
    chart_buffer.getvalue()
).decode("utf-8")

chart_buffer.close()

# =====================================================================
# CONTEXTO DO RELATÓRIO
# =====================================================================

report_context = {
    # Visão executiva
    "total_revenue": f"${total_revenue:,.2f}",
    "total_orders": f"{total_orders:,}",
    "total_customers": f"{total_customers:,}",
    "average_order_value": f"${average_order_value:,.2f}",

    # Vendas
    "annual_revenue_chart": annual_revenue_chart,
    "annual_sales_table": annual_sales_table,

    # Clientes
    "customer_total": f"{total_customers:,}",
    "customer_top_10_share": (
        f"{top_10_revenue_share:.2%}"
    ),
    "customer_top_20_share": (
        f"{top_20_revenue_share:.2%}"
    ),
    "customer_profiles_table": customer_profiles_table,
    "high_ticket_customer_share": (
        f"{high_ticket_customer_share:.2%}"
    ),
    "high_ticket_revenue_share": (
        f"{high_ticket_revenue_share:.2%}"
    ),

    # Produtos
    "product_total": f"{total_product_combinations:,}",
    "product_top_10_share": (
        f"{top_10_product_revenue_share:.2%}"
    ),
    "product_top_20_share": (
        f"{top_20_product_revenue_share:.2%}"
    ),
    "top_products_table": top_products_table,

    # Logística
    "shipping_median_days": (
        f"{shipping_days_median:.0f}"
    ),
    "upper_processing_share": (
        f"{upper_processing_share:.2%}"
    ),
    "standard_class_share": (
        f"{standard_class_share:.2%}"
    ),
    "shipping_mode_table": shipping_mode_table,
    "shipping_mode_chart": shipping_mode_chart,

    # Forecasting
    "baseline_mape": f"{baseline_mape:.2f}%",
    "forecast_mape": f"{hw_mape:.2f}%",
    "forecast_rmse_reduction": f"{rmse_reduction:.2%}",
    "forecast_mae_reduction": f"{mae_reduction:.2%}",
    "forecast_2019_total": f"${forecast_2019_total:,.2f}",
    "forecast_2019_average": f"${forecast_2019_average:,.2f}",
    "forecast_peak_month": forecast_peak_month.strftime("%b %Y"),
    "forecast_peak_value": f"${forecast_peak_value:,.2f}",
    "forecast_chart": forecast_chart,
    "forecast_table": forecast_table,
}


# =====================================================================
# RENDERIZAÇÃO DO TEMPLATE
# =====================================================================

environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR)
)

template = environment.get_template(
    "analytical_report.html"
)

rendered_report = template.render(
    **report_context
)


# =====================================================================
# PERSISTÊNCIA DO RELATÓRIO
# =====================================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_PATH.write_text(
    rendered_report,
    encoding="utf-8",
)


# =====================================================================
# VALIDAÇÃO NO TERMINAL
# =====================================================================

print("\nPerformance anual de vendas:\n")

print(
    annual_sales.to_string(
        index=False,
        formatters={
            "Revenue": lambda value: f"${value:,.2f}",
            "Average Order Value": (
                lambda value: f"${value:,.2f}"
            ),
            "Revenue YoY": lambda value: (
                "-"
                if pd.isna(value)
                else f"{value:.2%}"
            ),
        },
    )
)


print("\nConcentração da receita por cliente:\n")

print(
    f"Top 10%: {top_10_revenue_share:.2%}"
)

print(
    f"Top 20%: {top_20_revenue_share:.2%}"
)


print("\nPerfis econômicos de clientes:\n")

print(
    customer_profiles.to_string(
        index=False,
        formatters={
            "Revenue": lambda value: f"${value:,.2f}",
            "Average_Orders": (
                lambda value: f"{value:.1f}"
            ),
            "Average_AOV": (
                lambda value: f"${value:,.2f}"
            ),
            "Customer Share": (
                lambda value: f"{value:.2%}"
            ),
            "Revenue Share": (
                lambda value: f"{value:.2%}"
            ),
        },
    )
)


print("\nConcentração da receita por produto:\n")

print(
    f"Combinações analíticas de produtos: "
    f"{total_product_combinations:,}"
)

print(
    f"Top 10%: {top_10_product_revenue_share:.2%}"
)

print(
    f"Top 20%: {top_20_product_revenue_share:.2%}"
)


print("\nTop 10 produtos por receita:\n")

print(
    top_products[
        [
            "Product ID",
            "Product Name",
            "Orders",
            "Revenue",
            "Revenue Share",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": lambda value: f"${value:,.2f}",
            "Revenue Share": (
                lambda value: f"{value:.2%}"
            ),
        },
    )
)


print("\nAnálise logística:\n")

print(
    f"Pedidos analisados: {len(order_logistics):,}"
)

print(
    f"Conflitos logísticos: {logistics_conflicts:,}"
)

print(
    f"Mediana geral: {shipping_days_median:.0f} dias"
)

print(
    f"Pedidos acima de 5 dias: "
    f"{upper_processing_orders:,} "
    f"({upper_processing_share:.2%})"
)


print("\nModalidades de envio:\n")

print(
    shipping_mode_analysis.to_string(
        index=False,
        formatters={
            "Mean_Days": (
                lambda value: f"{value:.2f}"
            ),
            "Median_Days": (
                lambda value: f"{value:.0f}"
            ),
            "Min_Days": (
                lambda value: f"{value:.0f}"
            ),
            "Max_Days": (
                lambda value: f"{value:.0f}"
            ),
            "Order Share": (
                lambda value: f"{value:.2%}"
            ),
        },
    )
)

print("\nForecasting:\n")

print(
    f"Baseline sazonal — "
    f"MAE: ${baseline_mae:,.2f} | "
    f"RMSE: ${baseline_rmse:,.2f} | "
    f"MAPE: {baseline_mape:.2f}%"
)

print(
    f"Holt-Winters — "
    f"MAE: ${hw_mae:,.2f} | "
    f"RMSE: ${hw_rmse:,.2f} | "
    f"MAPE: {hw_mape:.2f}%"
)

print(
    f"Redução do MAE: {mae_reduction:.2%}"
)

print(
    f"Redução do RMSE: {rmse_reduction:.2%}"
)

print(
    f"Forecast 2019: ${forecast_2019_total:,.2f}"
)

print(
    f"\nRelatório gerado com sucesso: {OUTPUT_PATH}"
)