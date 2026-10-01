"""
Pipeline de limpeza de dados do projeto Superstore Sales Analytics.

Este módulo centraliza as transformações determinísticas identificadas
durante a etapa de auditoria de qualidade dos dados.

Responsabilidades:
- converter variáveis temporais para tipos adequados;
- padronizar identificadores geográficos;
- remover duplicidades de negócio;
- orquestrar as etapas de limpeza do dataset de vendas.

As funções recebem DataFrames e retornam novas estruturas tratadas,
preservando os dados de entrada.

Questões relacionadas à modelagem dimensional, como a definição das
chaves de produto e geografia, permanecem fora desta camada para evitar
alterações arbitrárias nos dados de origem.
"""

import pandas as pd


# Mapeamento utilizado para normalizar os nomes dos meses presentes
# nas datas por extenso antes da conversão para datetime.
MONTH_MAP = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12",
}


def convert_portuguese_date(series: pd.Series) -> pd.Series:
    """
    Converte datas por extenso em português para o tipo datetime.

    A fonte original armazena as datas no formato textual
    ``DD de mês de YYYY``. Os nomes dos meses são substituídos por
    suas representações numéricas antes da conversão com pandas.

    Valores que não possam ser convertidos são representados como NaT,
    permitindo que eventuais falhas sejam identificadas posteriormente
    pelos controles de qualidade do pipeline.

    Parameters
    ----------
    series : pd.Series
        Série contendo datas textuais em português.

    Returns
    -------
    pd.Series
        Série convertida para datetime.
    """
    converted = series.copy()

    # Normaliza os nomes dos meses para representação numérica.
    for month_name, month_number in MONTH_MAP.items():
        converted = converted.str.replace(
            month_name,
            month_number,
            regex=False,
        )

    # Remove os conectores textuais para obter o formato DD MM YYYY.
    converted = converted.str.replace(" de ", " ", regex=False)

    return pd.to_datetime(
        converted,
        format="%d %m %Y",
        errors="coerce",
    )


def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza as variáveis temporais do dataset de vendas.

    ``Order Date`` e ``Ship Date`` são convertidas utilizando a regra
    definida em ``convert_portuguese_date``. A transformação é realizada
    sobre uma cópia para preservar o DataFrame recebido como entrada.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset contendo as colunas Order Date e Ship Date.

    Returns
    -------
    pd.DataFrame
        Cópia do dataset com as variáveis temporais convertidas.
    """
    cleaned_df = df.copy()

    cleaned_df["Order Date"] = convert_portuguese_date(
        cleaned_df["Order Date"]
    )

    cleaned_df["Ship Date"] = convert_portuguese_date(
        cleaned_df["Ship Date"]
    )

    return cleaned_df


def clean_postal_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza Postal Code como identificador textual.

    Na fonte original, Postal Code é interpretado como ``float`` devido
    à presença de valores ausentes. Como códigos postais representam
    identificadores e não medidas numéricas, a coluna é convertida
    inicialmente para ``Int64`` anulável e posteriormente para ``string``.

    Essa estratégia remove a representação decimal dos códigos postais
    sem substituir ou imputar os valores ausentes identificados durante
    a auditoria de qualidade.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset contendo a coluna Postal Code.

    Returns
    -------
    pd.DataFrame
        Cópia do dataset com Postal Code padronizado como string.
    """
    cleaned_df = df.copy()

    # Int64 permite remover a parte decimal preservando valores ausentes.
    cleaned_df["Postal Code"] = (
        cleaned_df["Postal Code"]
        .astype("Int64")
        .astype("string")
    )

    return cleaned_df


def remove_business_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove registros classificados como duplicidades de negócio.

    ``Row ID`` é excluído da comparação por representar um identificador
    técnico único da fonte. Registros cujos demais atributos sejam
    integralmente idênticos são tratados como duplicidades de negócio.

    Quando uma duplicidade é encontrada, a primeira ocorrência é
    preservada e as ocorrências subsequentes são removidas.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de vendas a ser validado.

    Returns
    -------
    pd.DataFrame
        Cópia do dataset sem duplicidades de negócio.
    """
    cleaned_df = df.copy()

    # A regra de duplicidade considera todos os atributos de negócio,
    # desconsiderando apenas o identificador técnico Row ID.
    business_columns = [
        column for column in cleaned_df.columns
        if column != "Row ID"
    ]

    cleaned_df = cleaned_df.drop_duplicates(
        subset=business_columns,
        keep="first",
    )

    return cleaned_df


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executa o pipeline principal de limpeza dos dados de vendas.

    As transformações são aplicadas sequencialmente sobre uma cópia
    do DataFrame recebido, preservando o objeto de entrada.

    Pipeline
    --------
    1. Padronização das variáveis temporais.
    2. Padronização de Postal Code.
    3. Remoção de duplicidades de negócio.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset bruto de vendas.

    Returns
    -------
    pd.DataFrame
        Dataset tratado e preparado para os controles de qualidade
        e posterior persistência na camada processada.
    """
    cleaned_df = df.copy()

    # A ordem mantém cada transformação isolada e explicitamente
    # encadeada dentro do pipeline.
    cleaned_df = clean_date_columns(cleaned_df)
    cleaned_df = clean_postal_code(cleaned_df)
    cleaned_df = remove_business_duplicates(cleaned_df)

    return cleaned_df