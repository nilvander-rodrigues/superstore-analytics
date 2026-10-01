## 1. Visão Geral da Arquitetura

O projeto **Superstore Analytics** foi estruturado como um pipeline analítico modular, separando as etapas de armazenamento dos dados, preparação, análise, modelagem, geração de resultados e documentação.

O fluxo inicia com o dataset original em formato Excel, preservado na camada de dados brutos. A partir dessa fonte, são executadas verificações de qualidade e transformações necessárias para construção de uma base analítica consistente. O resultado do processamento é armazenado em formato **Parquet** e utilizado como fonte comum pelas análises subsequentes.

Os notebooks foram organizados de acordo com as diferentes etapas do processo analítico. As primeiras etapas concentram-se na qualidade e preparação dos dados, seguidas pela análise exploratória e pelas análises específicas de vendas, clientes, produtos e logística. A etapa final em Python utiliza a série histórica de receita para construção e avaliação de um modelo de forecasting.

Regras e cálculos reutilizáveis são separados dos notebooks e mantidos em módulos Python dentro de src/, reduzindo duplicação de lógica e facilitando manutenção, validação e reutilização.

Os resultados produzidos pelo pipeline servem como base para diferentes camadas de consumo. O **Power BI** é utilizado como camada de visualização executiva e exploração interativa dos principais indicadores, enquanto a documentação consolida os aspectos analíticos e técnicos do projeto.

Como artefato final do pipeline Python, o projeto também gera um **relatório analítico em HTML**, reunindo os principais KPIs, visualizações, tabelas, insights e resultados de forecasting em um formato autocontido e independente dos notebooks.

De forma simplificada, a arquitetura segue o fluxo:

Excel (Raw Data) → Data Quality → Data Preparation → Parquet (Processed Data) → EDA → Business Analysis → Forecasting → Outputs (Power BI / Executive Summary / HTML Analytical Report)

## 2. Ambiente de Desenvolvimento

### 2.1 — Python e Ambiente Virtual

O projeto foi desenvolvido utilizando **Python 3.12.10** como linguagem principal para preparação dos dados, análise exploratória, construção de métricas, análises de negócio e modelagem de séries temporais.

O desenvolvimento foi realizado no **Visual Studio Code (VS Code)**, utilizando notebooks Jupyter (.ipynb) como principal ambiente de execução das etapas analíticas.

Para isolar as dependências do projeto, foi criado um ambiente virtual Python denominado .venv. Essa abordagem evita conflitos com bibliotecas instaladas globalmente no sistema e permite manter um conjunto controlado de dependências associado especificamente ao projeto.

O kernel utilizado pelos notebooks está associado ao ambiente virtual do projeto, garantindo que as análises sejam executadas utilizando o mesmo interpretador Python e as mesmas dependências instaladas no .venv.

As versões das dependências instaladas são registradas no arquivo requirements.txt, permitindo que o ambiente possa ser reconstruído posteriormente em outra máquina.

**Ambiente utilizado:**

- **Python:** 3.12.10
- **Ambiente virtual:** .venv
- **IDE:** Visual Studio Code
- **Ambiente analítico:** Jupyter Notebook / IPython Kernel
- **Gerenciamento de dependências:** pip
- **Registro das dependências:** requirements.txt

### 2.2 — Dependências Principais

O projeto utiliza um conjunto reduzido de bibliotecas Python, selecionadas de acordo com as necessidades de manipulação de dados, persistência, visualização e modelagem estatística.

| Biblioteca | Função no Projeto |
|---|---|
| **pandas** | Manipulação, transformação, agregação e análise das estruturas de dados utilizadas ao longo do pipeline. |
| **NumPy** | Operações numéricas e suporte aos cálculos estatísticos e métricas implementadas no projeto. |
| **Matplotlib** | Construção das visualizações utilizadas durante as análises exploratórias e analíticas. |
| **PyArrow** | Suporte à leitura e gravação dos dados processados em formato Parquet. |
| **openpyxl** | Suporte à leitura do arquivo Excel utilizado como fonte de dados original. |
| **statsmodels** | Modelagem de séries temporais, incluindo a implementação do modelo Holt-Winters utilizado no forecasting. |
| **Jinja2** | Renderização do template utilizado para geração programática do relatório analítico em HTML. |
| **Jupyter / IPython Kernel** | Execução interativa e documentada dos notebooks analíticos dentro do ambiente do projeto. |

As versões exatas das dependências instaladas no ambiente são registradas no arquivo requirements.txt. Dessa forma, a documentação técnica apresenta apenas as bibliotecas relevantes para a arquitetura do projeto, enquanto o arquivo de requisitos mantém o registro necessário para reconstrução do ambiente.

## 3. Estrutura do Projeto

O projeto foi organizado de forma a separar dados, código reutilizável, notebooks analíticos, artefatos gerados e documentação. Essa estrutura reduz o acoplamento entre as etapas e facilita a manutenção e a reprodução das análises.

A organização principal é:

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
├── .gitignore
└── requirements.txt
```

**Responsabilidade das principais áreas**

- `data/raw/` — preserva os dados de origem sem alterações, mantendo uma referência do dataset recebido.
- `data/processed/` — armazena a base validada e preparada em Parquet, utilizada como fonte comum pelas análises posteriores.
- `notebooks/` — contém o fluxo analítico sequencial, da avaliação de qualidade ao forecasting.
- `src/` — concentra funções reutilizáveis de preparação, regras analíticas e métricas.
- `templates/` — contém o template Jinja2 responsável pela estrutura e apresentação do relatório HTML.
- `outputs/report/` — armazena o relatório HTML gerado programaticamente.
- `reports/` — contém a documentação executiva e técnica do projeto.
- `generate_report.py` — reconstrói indicadores, visualizações, validações e forecasting necessários ao relatório e renderiza o template HTML.
- `requirements.txt` — registra as dependências necessárias para reconstrução do ambiente Python.
- `.gitignore` — impede o versionamento de artefatos locais e temporários, como ambiente virtual, caches e configurações locais.

## 4. Pipeline Analítico

O pipeline foi organizado de forma sequencial, permitindo que cada etapa utilize resultados previamente validados e mantendo separadas as responsabilidades de qualidade, preparação, exploração, análise de negócio e modelagem.

### 4.1 — Dados de Origem

A fonte original do projeto é o arquivo sales_data.xlsx, armazenado em data/raw/.

O dataset contém dados transacionais de vendas da Superstore, incluindo informações relacionadas a pedidos, clientes, produtos, localização, modalidade de envio, datas e receita.

A base original é preservada sem alterações na camada `raw`, funcionando como referência dos dados recebidos e permitindo que as transformações realizadas posteriormente sejam reproduzidas a partir da fonte inicial.

A granularidade original corresponde a **itens de pedido (line items)**. Dessa forma, um mesmo `Order ID` pode aparecer em múltiplas linhas quando um pedido contém mais de um produto.

Após as etapas de qualidade e preparação, a base analítica possui **9.799 registros e 19 colunas**, cobrindo o período de **3 de janeiro de 2015 a 30 de dezembro de 2018**.

A receita total reconciliada da base processada é de **$2.261.255,41**, distribuída por **4.922 pedidos distintos** e **793 clientes**.

### 4.2 — Qualidade dos Dados

Antes de qualquer transformação ou análise de negócio, o dataset original foi submetido a uma etapa específica de avaliação de qualidade no notebook `01_data_quality.ipynb`.

Essa etapa teve como objetivo compreender a estrutura recebida, identificar potenciais problemas e estabelecer uma referência de qualidade antes da construção da base analítica.

As principais verificações realizadas incluíram:

- inspeção da estrutura, dimensões e schema do dataset;
- avaliação dos tipos de dados das colunas;
- identificação de valores ausentes;
- verificação de registros duplicados;
- análise da consistência das principais chaves e campos utilizados nas etapas posteriores;
- validação das variáveis de data, vendas, clientes, pedidos e produtos;
- identificação de situações que exigiriam tratamento ou atenção durante a preparação dos dados.

A análise identificou **11 valores ausentes em `Postal Code`**. Como essa ausência não compromete as principais métricas comerciais e analíticas do projeto, os registros foram preservados em vez de serem eliminados exclusivamente por esse motivo.

Também não foram identificadas **duplicidades de negócio** que justificassem a remoção de registros da base.

Essa etapa foi tratada como um **quality gate** do pipeline: as análises posteriores somente utilizam os dados após a avaliação das condições necessárias para seu processamento.

A separação entre qualidade e preparação também foi mantida propositalmente. O notebook de qualidade identifica e documenta os problemas encontrados, enquanto as transformações necessárias para construção da base analítica são realizadas na etapa seguinte.

### 4.3 — Preparação dos Dados

Após a avaliação de qualidade, o notebook `02_data_preparation.ipynb` concentra as transformações necessárias para construir a base utilizada pelas etapas analíticas posteriores.

A preparação foi desenvolvida preservando a granularidade original de **item de pedido**, evitando agregações prematuras que poderiam eliminar informações necessárias para análises posteriores.

Entre os principais tratamentos realizados estão:

- conversão e padronização das colunas de data;
- adequação dos tipos de dados utilizados nas análises;
- tratamento das condições identificadas durante a avaliação de qualidade;
- criação da variável derivada Shipping Days, representando o número de dias entre Order Date e Ship Date;
- validação da estrutura final da base;
- reconciliação das principais métricas após as transformações.

Ao final da preparação, a base contém **9.799 registros e 19 colunas**, mantendo a receita total de **$2.261.255,41** e a granularidade de item de pedido.

A base preparada é persistida em:

data/processed/sales_data_clean.parquet

O formato **Parquet** foi utilizado como camada intermediária entre preparação e análise, permitindo armazenar os dados com schema e tipos estruturados e evitando a necessidade de repetir o processamento do arquivo Excel em cada notebook.

A partir dessa etapa, os notebooks analíticos passam a consumir diretamente a base processada, estabelecendo uma fonte comum e consistente para EDA, análises de negócio e forecasting.

### 4.4 — Análise Exploratória

O notebook 03_eda.ipynb realiza a análise exploratória da base processada antes da construção das análises específicas de negócio.

A EDA tem como objetivo compreender a distribuição e o comportamento das principais variáveis, identificar padrões relevantes, avaliar valores extremos e verificar relações que possam orientar as etapas analíticas posteriores.

A exploração foi conduzida sobre diferentes perspectivas, incluindo:

- distribuição da receita e dos pedidos;
- comportamento temporal das vendas;
- participação de categorias, segmentos e regiões;
- estrutura e valor dos pedidos;
- distribuição dos valores de venda;
- identificação e análise de valores extremos;
- relações entre características dos pedidos;
- comportamento inicial das modalidades de envio.

A análise de valores extremos foi realizada tanto na granularidade de **item de pedido** quanto na granularidade de **pedido consolidado**. Esses registros foram analisados como parte do comportamento econômico da base e não removidos automaticamente, uma vez que apresentavam contribuição relevante para a receita e não havia evidência suficiente para classificá-los como erros.

A EDA também funcionou como uma etapa de validação analítica, permitindo confirmar que as principais métricas e dimensões apresentavam comportamento consistente antes do desenvolvimento das análises especializadas.

Os resultados exploratórios serviram como base para definir e refinar as questões posteriormente aprofundadas nos notebooks de vendas, clientes, produtos e logística, evitando que as análises de negócio fossem construídas sem uma compreensão prévia da estrutura dos dados.

### 4.5 — Análises de Negócio

Após a análise exploratória, o projeto foi dividido em quatro perspectivas de negócio. Cada notebook utiliza a granularidade adequada à questão investigada, evitando aplicar métricas sobre um nível de detalhe incompatível com o fenômeno analisado.

#### Sales Analysis

O notebook 04_sales_analysis.ipynb analisa a evolução do desempenho comercial ao longo do período.

A análise utiliza principalmente agregações por período e por dimensões de negócio para responder como a receita evoluiu e quais componentes contribuíram para suas variações.

Entre os principais elementos analisados estão:

- receita, número de pedidos, clientes ativos e ticket médio;
- evolução anual dos principais indicadores;
- crescimento ano contra ano (YoY);
- decomposição da variação da receita entre efeito de volume, efeito de ticket médio e interação;
- contribuição de categorias, segmentos e regiões para as variações observadas.

A decomposição permite separar o crescimento associado ao aumento do número de pedidos daquele relacionado à mudança no valor médio das transações.


#### Customer Analysis

O notebook 05_customer_analysis.ipynb altera a granularidade da análise para o nível de **cliente**, consolidando o histórico transacional de cada Customer ID.

A análise investiga:

- receita gerada por cliente;
- número de pedidos;
- ticket médio;
- concentração da receita entre os clientes de maior valor;
- relação entre frequência de compra e receita;
- combinação entre frequência de compra e ticket médio para identificação de diferentes perfis econômicos.

Essa perspectiva permite avaliar como o valor está distribuído pela base de clientes sem interpretar frequência, isoladamente, como medida suficiente de importância econômica.


#### Product Analysis

O notebook 06_product_analysis.ipynb concentra-se na contribuição econômica dos produtos.

Durante essa etapa foi identificado que **32 `Product IDs` estavam associados a mais de um Product Name**. Por esse motivo, Product ID isoladamente não foi tratado como chave analítica única, sendo utilizada a combinação entre identificador e nome do produto.

A análise considera **1.893 combinações analíticas de produto** e investiga:

- receita e presença em pedidos por produto;
- produtos de maior receita;
- concentração da receita entre os produtos de maior valor;
- identificação dos pedidos pertencentes à faixa superior de valor;
- produtos associados com maior frequência às transações de maior impacto econômico.

Essa abordagem preserva a inconsistência identificada na chave original sem consolidar artificialmente produtos com descrições distintas.


#### Logistics Analysis

O notebook 07_logistics_analysis.ipynb utiliza a granularidade de **pedido consolidado**, uma vez que o tempo entre pedido e envio é uma característica do pedido e não de cada item individual.

Antes da consolidação, foram verificadas possíveis inconsistências de Order Date, Ship Date, Ship Mode e Shipping Days dentro de um mesmo Order ID. Não foram identificados conflitos nessas variáveis.

A análise investiga:

- distribuição do tempo entre o registro do pedido e o envio;
- pedidos localizados na faixa superior de tempo de processamento;
- comportamento do tempo de processamento por modalidade de envio;
- participação de cada Ship Mode no volume total de pedidos.

Os resultados são interpretados como **tempo de processamento até o envio**. O projeto não classifica esses períodos como atrasos, pois o dataset não contém prazo prometido, SLA ou data efetiva de entrega.

### 4.6 — Forecasting

O notebook 08_time_series_forecasting.ipynb adiciona uma camada preditiva ao projeto, utilizando o histórico mensal de receita para avaliar a capacidade de previsão de um modelo de séries temporais.

A receita transacional foi agregada na granularidade **mensal**, resultando em uma série temporal contínua com **48 observações**, correspondentes ao período entre janeiro de 2015 e dezembro de 2018. A continuidade da série foi validada antes da modelagem, garantindo a ausência de meses faltantes.

Para preservar a ordem temporal e evitar vazamento de informação entre treinamento e avaliação, os dados não foram divididos aleatoriamente. A série foi separada cronologicamente em:

- **36 meses de treinamento:** janeiro de 2015 a dezembro de 2017;
- **12 meses de teste:** janeiro a dezembro de 2018.

Como referência inicial foi utilizado um **Seasonal Naive**, no qual a previsão de cada mês corresponde ao valor observado no mesmo mês do ano anterior. Esse modelo funciona como baseline e permite avaliar se a utilização de uma técnica de forecasting mais estruturada produz ganho preditivo relevante.

O modelo avaliado foi o **Holt-Winters**, utilizando componentes aditivos de tendência e sazonalidade e periodicidade anual de 12 meses.

As previsões do baseline e do Holt-Winters foram avaliadas sobre o mesmo período de teste utilizando três métricas:

- **MAE (Mean Absolute Error):** mede a magnitude média dos erros em unidades monetárias;
- **RMSE (Root Mean Squared Error):** atribui maior peso aos erros de maior magnitude;
- **MAPE (Mean Absolute Percentage Error):** expressa o erro absoluto médio em relação aos valores observados.

O Holt-Winters apresentou erro inferior ao baseline nas três métricas utilizadas, fornecendo evidência de ganho preditivo no período de teste analisado.

Após a avaliação fora da amostra, o modelo selecionado foi reajustado utilizando as **48 observações disponíveis**. Esse modelo final foi então utilizado para gerar a projeção dos **12 meses seguintes ao histórico**, correspondentes a 2019.

A previsão futura é mantida separada da etapa de avaliação. As métricas de erro são calculadas exclusivamente sobre 2018, período para o qual existem valores reais observados. A projeção de 2019 não recebe métricas de erro, pois os valores futuros não fazem parte do dataset disponível.

A abordagem foi mantida propositalmente parcimoniosa. Considerando o histórico limitado a quatro ciclos anuais, o projeto prioriza uma comparação transparente entre baseline e modelo, em vez da avaliação de um grande número de algoritmos sobre uma série temporal relativamente curta. 

## 5. Módulos Python

O diretório src/ é destinado à lógica Python reutilizável do projeto.

A separação entre notebooks e módulos segue o princípio de que os notebooks devem concentrar a sequência analítica, a exploração dos resultados e sua interpretação, enquanto funções reutilizáveis e regras de cálculo devem permanecer fora das células sempre que sua reutilização ou validação justificar essa separação.

Essa abordagem reduz duplicação de código e permite que uma mesma regra seja utilizada de forma consistente em diferentes etapas do projeto.

### 5.1 — data_cleaning.py

O módulo `src/data_cleaning.py` centraliza as transformações determinísticas utilizadas na preparação da base analítica.

Entre suas responsabilidades estão:

- conversão das datas originalmente representadas com nomes de meses em português;
- padronização das colunas de data;
- adequação de `Postal Code` para uma representação textual compatível com seu papel de identificador geográfico;
- remoção de duplicidades de negócio quando identificadas;
- orquestração das etapas de limpeza por meio de `clean_sales_data()`.

A separação dessas regras da camada de notebook reduz duplicação, torna explícito o contrato de preparação e permite que a mesma lógica seja reaplicada de forma consistente a partir dos dados de origem.

### 5.2 — metrics.py

O módulo src/metrics.py concentra funções analíticas reutilizáveis empregadas nos notebooks.

Atualmente, o módulo implementa quatro funções principais:

- calculate_iqr_bounds() — calcula os limites inferior e superior do método do intervalo interquartil (IQR), utilizado na análise de valores extremos.

- decompose_revenue_change() — decompõe a variação da receita entre períodos em efeito de volume, efeito de ticket médio e efeito de interação.

- calculate_top_concentration() — calcula a participação acumulada de uma determinada fração superior das observações, sendo utilizada nas análises de concentração de clientes e produtos.

- calculate_forecast_metrics() — calcula MAE, RMSE e MAPE para avaliação das previsões produzidas na etapa de forecasting.

A centralização dessas regras evita que a mesma lógica seja implementada separadamente em diferentes notebooks e estabelece uma única definição para métricas reutilizadas pelo projeto.

O módulo também inclui validações associadas às funções quando necessárias. No cálculo das métricas de forecasting, por exemplo, são verificadas a compatibilidade entre o número de valores reais e previstos e a presença de valores reais iguais a zero antes do cálculo do MAPE.

Nem toda transformação realizada nos notebooks é transferida para src/. Operações específicas de uma única análise permanecem próximas ao contexto em que são utilizadas. A modularização é aplicada principalmente quando existe uma regra reutilizável, uma definição analítica relevante ou uma lógica que se beneficia de manutenção e validação centralizadas.

## 6. Contratos e Granularidade dos Dados

As análises do projeto utilizam diferentes unidades de observação de acordo com a pergunta investigada. Por esse motivo, a granularidade dos dados é tratada explicitamente ao longo do pipeline.

A base processada sales_data_clean.parquet preserva a granularidade original de **item de pedido (line item)**. Dessa forma, um mesmo Order ID pode estar presente em múltiplas linhas quando o pedido contém diferentes produtos.

A partir dessa base, estruturas analíticas específicas são construídas quando a pergunta exige outro nível de observação.

| Estrutura Analítica | Granularidade | Identificador / Referência | Aplicação Principal |
|---|---|---|---|
| Base processada | Item de pedido | Linha transacional | EDA e análises que dependem do detalhe dos produtos |
| Pedidos | Pedido consolidado | Order ID | Ticket médio, estrutura dos pedidos e logística |
| Clientes | Cliente | Customer ID | Receita, frequência e valor econômico por cliente |
| Produtos | Produto analítico | Product ID + Product Name | Receita e concentração por produto |
| Série temporal | Mês | Período mensal | Forecasting da receita |

### Contratos Analíticos

Além da granularidade, algumas condições são tratadas como contratos necessários para garantir a consistência das análises.

**Pedidos**

Ao consolidar dados na granularidade de pedido, um mesmo Order ID deve apresentar informações consistentes para atributos pertencentes ao pedido, como Order Date, Ship Date, Ship Mode e Shipping Days.

Essa condição foi explicitamente validada antes da construção da visão logística por pedido.

**Clientes**

Customer ID é utilizado como identificador para consolidação do histórico transacional de cada cliente. As métricas de receita, quantidade de pedidos e ticket médio são calculadas após a transformação para essa granularidade.

**Produtos**

A análise identificou que Product ID isoladamente não representa uma chave analítica única no dataset, pois **32 identificadores estavam associados a mais de um Product Name**.

Por esse motivo, a combinação:

Product ID + Product Name

é utilizada como identificador analítico de produto, resultando em **1.893 combinações distintas**.

**Série Temporal**

Para forecasting, as transações são agregadas por mês. O contrato dessa estrutura exige uma sequência temporal contínua, ordenada cronologicamente e sem meses ausentes.

A série utilizada contém **48 observações mensais consecutivas**, entre janeiro de 2015 e dezembro de 2018.

### Reconciliação entre Granularidades

A mudança de granularidade não deve alterar indevidamente as métricas que precisam permanecer invariantes.

Por esse motivo, as estruturas derivadas são reconciliadas com a base processada sempre que aplicável. A receita total de **$2.261.255,41**, por exemplo, permanece consistente ao consolidar os dados para análises de pedidos, clientes e produtos.

Essa prática permite detectar problemas como duplicações introduzidas por agregações, perda indevida de registros ou utilização incorreta de chaves antes que esses problemas afetem os resultados analíticos.

## 7. Validação e Controles de Qualidade

O pipeline utiliza controles de validação em diferentes etapas para reduzir o risco de inconsistências entre preparação, análise e modelagem.

Os principais controles aplicados incluem:

- verificação de valores ausentes e duplicidades;
- validação dos tipos e estrutura dos dados;
- reconciliação da receita após transformações e mudanças de granularidade;
- verificação da unicidade das estruturas consolidadas;
- validação da consistência de Order Date, Ship Date, Ship Mode e Shipping Days dentro de cada Order ID;
- validação da continuidade mensal da série utilizada no forecasting;
- separação cronológica entre treino e teste para evitar data leakage;
- comparação do modelo de forecasting com um baseline sazonal;
- validações internas nas funções reutilizáveis de metrics.py.

Como controle final de execução, os notebooks são validados a partir de um kernel reiniciado, utilizando **Restart Kernel → Run All**. Esse procedimento permite identificar dependências ocultas entre células e verificar se cada notebook pode ser reproduzido integralmente na ordem definida.

Esses controles funcionam como *quality gates* distribuídos pelo pipeline, garantindo que os resultados avancem para as etapas seguintes somente após as verificações correspondentes.

## 8. Reprodutibilidade

O projeto foi estruturado para permitir que as análises sejam reproduzidas a partir dos dados de origem e do código disponível no repositório.

Os principais elementos utilizados para garantir a reprodutibilidade são:

- preservação do dataset original em data/raw/;
- geração controlada da base processada em data/processed/;
- organização sequencial dos notebooks, de 01 a 08;
- centralização de regras reutilizáveis em `src/`;
- isolamento das dependências por meio do ambiente virtual `.venv`;
- registro das versões das bibliotecas em `requirements.txt`;
- utilização de caminhos relativos à raiz do projeto;
- validação dos notebooks por meio de **Restart Kernel → Run All**;
- geração determinística do relatório HTML por `generate_report.py`, utilizando a base processada e o template versionado.

Dessa forma, o fluxo analítico pode ser reconstruído desde a fonte original até as análises e resultados finais sem depender do estado de execuções anteriores dos notebooks.

As instruções necessárias para configuração do ambiente e execução do projeto serão consolidadas no README.md.

## 9. Camada de Visualização e Relatório HTML

A arquitetura do projeto separa processamento analítico e apresentação.

O **Python** é responsável pela preparação dos dados, validações, construção das métricas, análises estatísticas e forecasting. O **Power BI** funciona como camada de visualização executiva e exploração interativa dos principais indicadores.

Como artefato complementar, o projeto gera um **HTML Analytical Report** estático e autocontido. A geração é realizada por `generate_report.py`, que lê `sales_data_clean.parquet`, recalcula os indicadores necessários, executa controles de reconciliação, reproduz a avaliação e projeção de forecasting e renderiza `templates/analytical_report.html` por meio do **Jinja2**.

Os gráficos do relatório são produzidos com Matplotlib e incorporados ao próprio HTML em Base64. Dessa forma, o arquivo final pode ser aberto localmente sem depender de arquivos de imagem externos.

O relatório consolidado é armazenado em:

```text
outputs/report/superstore_analytics_report.html
```

O documento apresenta sete blocos analíticos:

1. Visão Executiva;
2. Performance de Vendas;
3. Clientes;
4. Produtos;
5. Logística;
6. Forecasting;
7. Conclusões e Limitações.

A geração do relatório também atua como uma camada adicional de validação. Antes da renderização, o script verifica reconciliações de receita, granularidade de pedidos, consistência das informações logísticas e continuidade da série temporal utilizada no forecasting.

As duas camadas de apresentação possuem finalidades distintas:

- **Power BI:** exploração interativa e comunicação executiva dos indicadores.
- **HTML Analytical Report:** apresentação estática, portátil e reproduzível dos principais resultados produzidos pelo pipeline Python.

## 10. Considerações Técnicas

A arquitetura do **Superstore Analytics** foi construída priorizando separação de responsabilidades, rastreabilidade das transformações e consistência entre as diferentes etapas do processo analítico.

As decisões técnicas buscaram manter a complexidade proporcional ao problema. Transformações específicas permanecem próximas às análises que as utilizam, enquanto regras reutilizáveis são centralizadas em módulos Python. Da mesma forma, diferentes granularidades são utilizadas somente quando necessárias para responder corretamente às respectivas perguntas de negócio.

A qualidade dos resultados é apoiada por validações distribuídas ao longo do pipeline, incluindo reconciliação de métricas, verificação de chaves e granularidades, controles de consistência e avaliação temporal fora da amostra no forecasting.

O projeto mantém uma separação clara entre **processamento e modelagem em Python**, **visualização executiva em Power BI**, **relatório analítico HTML** e **documentação dos resultados**, estabelecendo uma base que pode ser expandida posteriormente sem alterar os princípios fundamentais da arquitetura.