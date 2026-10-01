"""
Métricas analíticas e utilitários estatísticos.

Este módulo centraliza cálculos reutilizáveis utilizados ao longo do
projeto Superstore Analytics.

O objetivo é separar a lógica analítica dos notebooks, permitindo que
métricas estatísticas e de negócio sejam aplicadas de forma consistente
em diferentes etapas da análise.

Responsabilidades
-----------------
- Calcular métricas estatísticas reutilizáveis.
- Definir limites e critérios analíticos.
- Centralizar regras de negócio utilizadas em diferentes análises.
- Reduzir duplicação de lógica entre notebooks.

"""

import math
import numpy as np


# ---------------------------------------------------------------------
# Métricas Estatísticas
# ---------------------------------------------------------------------

def calculate_iqr_bounds(series, multiplier=1.5):
    """
    Calcula quartis, intervalo interquartil e limites baseados no IQR.

    O IQR (Interquartile Range) representa a amplitude dos 50% centrais
    da distribuição e é calculado pela diferença entre o terceiro
    quartil (Q3) e o primeiro quartil (Q1).

    Fórmula:
        IQR = Q3 - Q1

    A partir do IQR, são definidos os limites inferior e superior:

        Limite inferior = Q1 - (multiplicador × IQR)
        Limite superior = Q3 + (multiplicador × IQR)

    Esses limites podem ser utilizados para identificar observações
    estatisticamente extremas na distribuição.

    Parameters
    ----------
    series : pandas.Series
        Série numérica que será analisada.

    multiplier : float, default=1.5
        Multiplicador aplicado ao intervalo interquartil para definir
        os limites inferior e superior.

    Returns
    -------
    dict
        Dicionário contendo:
        - q1: primeiro quartil.
        - median: mediana.
        - q3: terceiro quartil.
        - iqr: intervalo interquartil.
        - lower_bound: limite inferior.
        - upper_bound: limite superior.

    Notes
    -----
    Observações fora dos limites calculados são consideradas outliers
    segundo o critério estatístico do IQR. Isso não significa,
    necessariamente, que representem erros ou problemas de qualidade
    dos dados.
    """

    # Quartis que delimitam os 50% centrais da distribuição.
    q1 = series.quantile(0.25)
    median = series.median()
    q3 = series.quantile(0.75)

    # Distância entre o terceiro e o primeiro quartil.
    iqr = q3 - q1

    # Limites utilizados para identificar valores estatisticamente extremos.
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    return {
        "q1": q1,
        "median": median,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
    }


# ---------------------------------------------------------------------
# Métricas de Negócio
# ---------------------------------------------------------------------

def decompose_revenue_change(
    current_orders,
    previous_orders,
    current_aov,
    previous_aov
):
    """
    Decompõe a variação da receita entre dois períodos.

    Como a receita pode ser representada por:

        Receita = Número de Pedidos × Ticket Médio (AOV)

    a diferença entre dois períodos pode ser decomposta em três efeitos:

    1. Efeito Volume
       Mede quanto da variação ocorreu pela mudança no número de pedidos,
       mantendo como referência o ticket médio do período anterior.

       Fórmula:
           (Pedidos atuais - Pedidos anteriores) × AOV anterior

    2. Efeito Ticket Médio
       Mede quanto da variação ocorreu pela mudança no valor médio dos
       pedidos, mantendo como referência o volume do período anterior.

       Fórmula:
           (AOV atual - AOV anterior) × Pedidos anteriores

    3. Efeito Interação
       Captura o impacto produzido pela alteração simultânea do volume
       de pedidos e do ticket médio.

       Fórmula:
           (Pedidos atuais - Pedidos anteriores)
           × (AOV atual - AOV anterior)

    A soma dos três efeitos reconcilia a variação total da receita.

    Parameters
    ----------
    current_orders : int or float
        Número de pedidos do período atual.

    previous_orders : int or float
        Número de pedidos do período anterior.

    current_aov : float
        Ticket médio (Average Order Value) do período atual.

    previous_aov : float
        Ticket médio (Average Order Value) do período anterior.

    Returns
    -------
    dict
        Dicionário contendo:
        - volume_effect: efeito da mudança no volume de pedidos.
        - aov_effect: efeito da mudança no ticket médio.
        - interaction_effect: efeito combinado das duas mudanças.
        - reconciled_change: variação total reconciliada da receita.
    """

    # Impacto causado exclusivamente pela alteração no número de pedidos.
    volume_effect = (
        (current_orders - previous_orders)
        * previous_aov
    )

    # Impacto causado exclusivamente pela alteração no ticket médio.
    aov_effect = (
        (current_aov - previous_aov)
        * previous_orders
    )

    # Impacto adicional causado pela alteração simultânea das duas variáveis.
    interaction_effect = (
        (current_orders - previous_orders)
        * (current_aov - previous_aov)
    )

    # A soma dos três componentes deve reconciliar a mudança total da receita.
    reconciled_change = (
        volume_effect
        + aov_effect
        + interaction_effect
    )

    return {
        "volume_effect": volume_effect,
        "aov_effect": aov_effect,
        "interaction_effect": interaction_effect,
        "reconciled_change": reconciled_change,
    }


def calculate_top_concentration(values, top_fraction):
    """
    Calcula a concentração de valor entre a fração superior das entidades.

    A função permite responder perguntas como:

        "Qual percentual da receita está concentrado nos 10% maiores
        clientes?"

    ou:

        "Qual percentual da receita está concentrado nos 20% maiores
        produtos?"

    A metodologia segue quatro etapas:

    1. Ordenar os valores do maior para o menor.
    2. Determinar quantas entidades pertencem à fração analisada.
    3. Somar o valor gerado por essas entidades.
    4. Dividir esse valor pelo valor total da população.

    O número de entidades é arredondado para cima utilizando math.ceil():

        Quantidade Top = ceil(Número de entidades × Fração)

    A participação no valor total é calculada por:

        Participação Top = Valor do Top / Valor Total

    Parameters
    ----------
    values : pandas.Series
        Série numérica contendo o valor associado a cada entidade.
        Por exemplo, receita por cliente ou receita por produto.

    top_fraction : float
        Fração superior das entidades que será analisada.

        Exemplos:
        - 0.10 representa os 10% maiores.
        - 0.20 representa os 20% maiores.
        - 1.00 representa toda a população.

        O valor deve ser maior que 0 e menor ou igual a 1.

    Returns
    -------
    dict
        Dicionário contendo:
        - top_count: quantidade de entidades incluídas na fração superior.
        - top_value: valor total concentrado nessas entidades.
        - top_share: participação dessas entidades no valor total.

    Raises
    ------
    ValueError
        Se top_fraction não estiver no intervalo (0, 1].
    """

    # Garante que a fração informada represente uma proporção válida.
    if not 0 < top_fraction <= 1:
        raise ValueError(
            "top_fraction deve ser maior que 0 e menor ou igual a 1."
        )

    # Ordena as entidades do maior para o menor valor para identificar
    # corretamente aquelas que pertencem ao grupo superior.
    sorted_values = values.sort_values(ascending=False)

    # Calcula quantas entidades pertencem à fração analisada.
    # ceil() garante que uma fração de entidade seja arredondada para cima.
    top_count = math.ceil(
        len(sorted_values) * top_fraction
    )

    # Soma o valor gerado pelas entidades pertencentes ao grupo superior.
    top_value = (
        sorted_values
        .head(top_count)
        .sum()
    )

    # Calcula o valor total da população para servir como denominador.
    total_value = sorted_values.sum()

    # Evita divisão por zero caso a série analisada tenha soma igual a zero.
    top_share = (
        top_value / total_value
        if total_value != 0
        else 0
    )

    return {
        "top_count": top_count,
        "top_value": top_value,
        "top_share": top_share,
    }

# ---------------------------------------------------------------------
# Métricas de Forecasting
# ---------------------------------------------------------------------

def calculate_forecast_metrics(actual, predicted):
    """
    Calcula métricas de erro para avaliação de previsões.

    Parameters
    ----------
    actual : array-like
        Valores reais observados.

    predicted : array-like
        Valores previstos pelo modelo.

    Returns
    -------
    dict
        Dicionário contendo:
        - mae: Mean Absolute Error.
        - rmse: Root Mean Squared Error.
        - mape: Mean Absolute Percentage Error, expresso como proporção.

    Raises
    ------
    ValueError
        Se as séries possuírem tamanhos diferentes ou se algum valor
        real for igual a zero.
    """

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if len(actual) != len(predicted):
        raise ValueError(
            "actual e predicted devem possuir o mesmo número de observações."
        )

    if np.any(actual == 0):
        raise ValueError(
            "MAPE não pode ser calculado quando actual contém valores iguais a zero."
        )

    errors = actual - predicted

    mae = np.mean(np.abs(errors))

    rmse = np.sqrt(
        np.mean(errors ** 2)
    )

    mape = np.mean(
        np.abs(errors / actual)
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
    }