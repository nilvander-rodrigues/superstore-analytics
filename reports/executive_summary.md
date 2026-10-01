## 1. Objetivo do Projeto

O projeto **Superstore Analytics** tem como objetivo transformar dados históricos de vendas em informações analíticas capazes de apoiar a compreensão do desempenho comercial e operacional do negócio.

A análise utiliza dados transacionais do período de **2015 a 2018** para investigar a evolução da receita, os fatores associados ao seu crescimento, o comportamento econômico dos clientes, a contribuição dos produtos e o tempo entre o registro dos pedidos e o envio.

Além da análise histórica, o projeto incorpora uma etapa de **forecasting da receita mensal**, utilizando validação temporal fora da amostra para comparar um modelo de séries temporais com um baseline sazonal e, posteriormente, gerar uma projeção para os 12 meses seguintes ao histórico disponível.

Todo o processo foi desenvolvido com foco em **qualidade dos dados, consistência das métricas, reprodutibilidade das análises e interpretação orientada ao negócio**, utilizando Python para preparação, análise e modelagem dos dados e Power BI como camada de visualização executiva.

## 2. Perguntas de Negócio

A análise foi estruturada para responder às seguintes perguntas:

1. **Como a receita evoluiu entre 2015 e 2018 e quais fatores contribuíram para essa evolução?**

2. **Como o valor econômico está distribuído entre os clientes e qual é o nível de concentração da receita?**

3. **Qual é a relação entre frequência de compra, ticket médio e valor gerado pelos clientes?**

4. **Quais produtos apresentam maior impacto econômico e quanto da receita está concentrada nos produtos de maior valor?**

5. **Quais produtos estão mais associados aos pedidos de alto valor?**

6. **Como se comporta o tempo entre o registro do pedido e o envio?**

7. **Como o tempo de processamento dos pedidos varia entre as diferentes modalidades de envio?**

8. **Um modelo de séries temporais consegue melhorar a previsão da receita mensal em relação a um baseline sazonal?**

9. **Qual é a projeção de receita para os 12 meses seguintes ao histórico disponível?**

## 3. Principais Achados

### 3.1 — Crescimento da Receita

A Superstore gerou **$2,26 milhões em receita** entre 2015 e 2018, distribuídos por **4.922 pedidos** e **793 clientes**.

A evolução anual não foi linear. A receita recuou **4,20% em 2016**, avançou **30,64% em 2017** e cresceu mais **20,30% em 2018**, quando atingiu aproximadamente **$722 mil**, o maior valor anual do período analisado.

A decomposição do crescimento mostrou que a expansão observada nos dois últimos anos foi sustentada principalmente pelo **aumento do número de pedidos**, e não pelo crescimento do ticket médio. Em 2018, por exemplo, os pedidos aumentaram **28,26%**, enquanto o ticket médio recuou **6,21%**.

Isso indica que o crescimento recente da receita esteve mais associado à expansão do volume de transações do que ao aumento do valor médio de cada pedido.


### 3.2 — Valor e Concentração dos Clientes

A distribuição da receita entre os clientes apresenta concentração relevante. Os **10% de clientes de maior valor responderam por 31,16% da receita**, enquanto os **20% superiores concentraram 48,47%**.

A relação entre frequência de compra e receita é positiva, mas não suficiente para explicar isoladamente o valor econômico de um cliente. A correlação de Spearman entre número de pedidos e receita foi de **0,564**, indicando associação moderada.

Ao combinar frequência de compra e ticket médio, o grupo classificado como **Alta Frequência | Alto Ticket** representou **30,14% dos clientes**, mas respondeu por **54,29% da receita**.

Considerando conjuntamente os dois perfis de alto ticket, aproximadamente **50,06% dos clientes concentraram 76,75% da receita**, reforçando a importância do valor médio das transações na composição da receita por cliente.


### 3.3 — Concentração e Impacto dos Produtos

A análise identificou **1.893 combinações analíticas de produto**, considerando conjuntamente `Product ID` e `Product Name`. Essa abordagem foi necessária porque **32 Product IDs estavam associados a mais de um nome de produto**, impedindo o uso isolado do identificador como chave analítica única.

A receita apresenta concentração elevada entre os produtos. Os **10% de produtos de maior valor responderam por 59,11% da receita**, enquanto os **20% superiores concentraram 77,44%**.

O produto com maior receita no período foi o **Canon imageCLASS 2200 Advanced Copier**, responsável por aproximadamente **$61,6 mil**, apesar de aparecer em apenas cinco pedidos.

Também foi identificado que os pedidos pertencentes aos **10% de maior valor** responderam por **53,14% de toda a receita**, evidenciando o impacto econômico de um grupo relativamente pequeno de transações.


### 3.4 — Processamento dos Pedidos

O tempo mediano entre o registro do pedido e o envio foi de **4 dias**, com valores observados entre **0 e 7 dias**.

As modalidades de envio apresentaram comportamentos claramente distintos. A mediana foi de **0 dias para Same Day**, **2 dias para First Class**, **3 dias para Second Class** e **5 dias para Standard Class**.

A **Standard Class** concentrou **59,83% dos pedidos**, sendo, portanto, a modalidade predominante no conjunto de dados.

Além disso, **18,02% dos pedidos apresentaram tempos de processamento de 6 ou 7 dias**. Esses casos representam a faixa superior observada na distribuição, mas não podem ser classificados como atrasos porque o dataset não contém informação de prazo prometido ou SLA.

## 4. Implicações para o Negócio

Os resultados mostram que o crescimento recente da Superstore foi sustentado principalmente pelo aumento do volume de pedidos. Em 2018, a expansão da quantidade de transações ocorreu simultaneamente à redução do ticket médio, indicando que o acompanhamento do crescimento deve considerar não apenas a receita total, mas também a evolução conjunta de **volume e valor médio por pedido**.

A concentração observada entre os clientes evidencia que uma parcela relativamente limitada da base possui participação relevante na geração de receita. Os clientes de **Alta Frequência | Alto Ticket**, por exemplo, representam 30,14% da base e concentram 54,29% da receita. Esse comportamento torna relevante acompanhar separadamente frequência de compra, ticket médio e participação na receita, permitindo identificar alterações na composição econômica da carteira de clientes ao longo do tempo.

A concentração é ainda mais acentuada no portfólio de produtos: os 20% de produtos de maior valor respondem por 77,44% da receita. Esse nível de concentração torna importante acompanhar continuamente quais produtos sustentam maior parcela do faturamento e como essa participação evolui, especialmente porque produtos de alta receita não necessariamente apresentam elevada frequência de pedidos.

Na dimensão operacional, a predominância da **Standard Class**, responsável por 59,83% dos pedidos, faz com que o comportamento dessa modalidade tenha peso relevante sobre o tempo de processamento observado no conjunto da operação. As diferenças entre modalidades também justificam seu acompanhamento de forma separada, evitando interpretar uma média geral como representativa de todos os pedidos.

Em conjunto, os resultados indicam que uma visão executiva do negócio deve acompanhar simultaneamente **receita, volume de pedidos, ticket médio, concentração de clientes, concentração de produtos e tempo de processamento por modalidade de envio**. Essa combinação permite observar não apenas quanto o negócio cresce, mas também como esse crescimento está sendo formado.

## 5. Forecasting

A etapa de forecasting avaliou se um modelo de séries temporais seria capaz de melhorar a previsão da receita mensal em relação a uma referência sazonal simples.

A série utilizada contém **48 observações mensais**, entre janeiro de 2015 e dezembro de 2018. Para preservar a ordem temporal e simular um cenário real de previsão, os primeiros **36 meses (2015–2017)** foram utilizados para treinamento e os **12 meses de 2018** foram reservados exclusivamente para avaliação fora da amostra.

Como referência, foi utilizado um modelo **Seasonal Naive**, no qual cada mês de 2018 recebe como previsão o valor observado no mesmo mês do ano anterior. O baseline apresentou **MAE de $15.444,18**, **RMSE de $18.932,10** e **MAPE de 24,86%**.

O modelo **Holt-Winters**, utilizando tendência e sazonalidade aditivas com periodicidade anual, apresentou desempenho superior no mesmo período de teste, com **MAE de $11.384,97**, **RMSE de $12.429,52** e **MAPE de 22,73%**.

Em relação ao baseline, o modelo reduziu o **MAE em 26,28%**, o **RMSE em 34,35%** e o **MAPE em 8,58%**, indicando ganho preditivo no período utilizado para validação.

Após a avaliação, o Holt-Winters foi reajustado utilizando todo o histórico disponível entre 2015 e 2018 e empregado para projetar os 12 meses seguintes. A previsão resultante indica uma **receita total de aproximadamente $898,9 mil para 2019**, equivalente a uma média mensal de **$74,9 mil**.

Dentro da projeção, **dezembro apresenta o maior valor mensal previsto, com aproximadamente $116,3 mil**, enquanto **fevereiro apresenta o menor, com aproximadamente $41,6 mil**.

Esses valores representam projeções condicionadas aos padrões históricos identificados pelo modelo e não devem ser interpretados como resultados realizados ou metas garantidas.

## 6. Limitações

As análises desenvolvidas devem ser interpretadas considerando as características e limitações do conjunto de dados disponível.

- **Rentabilidade:** o dataset permite analisar receita, mas não contém informações suficientes sobre custos, margem ou lucro. Portanto, produtos, clientes ou segmentos com maior receita não podem ser automaticamente classificados como os mais rentáveis.

- **Logística:** estão disponíveis as datas de registro do pedido e de envio, permitindo calcular o tempo de processamento até o despacho. Entretanto, não há informações sobre data prometida, data efetiva de entrega, transportadora, custo de frete ou SLA. Por esse motivo, não é possível avaliar atrasos, cumprimento de prazo ou eficiência logística completa.

- **Clientes:** a análise identifica concentração de receita, frequência de compra e ticket médio, mas não contém informações sobre custo de aquisição, campanhas, canais de relacionamento ou custos de atendimento. Assim, os perfis identificados representam comportamento econômico histórico e não uma avaliação completa do valor ou da rentabilidade futura dos clientes.

- **Produtos:** a análise mede receita, presença em pedidos e concentração econômica, mas não incorpora informações sobre estoque, custo, margem, preço de aquisição ou disponibilidade. Dessa forma, não é possível avaliar rentabilidade ou desempenho operacional completo dos produtos.

- **Forecasting:** a série temporal contém apenas **48 observações mensais e quatro ciclos anuais**, limitando a quantidade de informação disponível para estimação de padrões temporais. A avaliação foi realizada em uma única janela de teste de 12 meses, correspondente a 2018.

- **Variáveis externas:** o modelo de forecasting utiliza exclusivamente o histórico da receita. Fatores como promoções, alterações de preços, condições econômicas, disponibilidade de produtos ou mudanças comerciais não estão incorporados à modelagem.

- **Projeções futuras:** a previsão para 2019 representa uma estimativa condicionada aos padrões observados entre 2015 e 2018. Os valores projetados não devem ser interpretados como resultados realizados, metas garantidas ou intervalos de certeza.

Essas limitações não invalidam os resultados obtidos, mas estabelecem o escopo dentro do qual as conclusões do projeto devem ser interpretadas.

## 7. Conclusão

O projeto **Superstore Analytics** consolidou uma visão integrada do desempenho comercial e operacional da empresa entre 2015 e 2018, conectando análises de vendas, clientes, produtos, processamento de pedidos e séries temporais em uma estrutura analítica única.

Os resultados mostram que o crescimento mais recente da receita foi sustentado principalmente pela expansão do volume de pedidos, ao mesmo tempo em que foi identificada uma concentração relevante de receita entre clientes e, de forma ainda mais acentuada, entre produtos. Na dimensão operacional, as diferentes modalidades de envio apresentam padrões distintos de tempo de processamento, reforçando a importância de analisar esses comportamentos separadamente.

A etapa de forecasting complementou a análise histórica ao demonstrar, por meio de validação fora da amostra, que o modelo Holt-Winters apresentou desempenho superior ao baseline sazonal utilizado como referência. A projeção para 2019 amplia a análise para uma perspectiva futura, mas deve ser interpretada dentro das limitações do histórico disponível e das variáveis consideradas pelo modelo.

Em conjunto, o projeto demonstra como dados transacionais podem ser transformados em uma estrutura analítica reproduzível, conectando preparação e validação dos dados, análises de negócio, forecasting e camadas de apresentação em Power BI e relatório HTML. Essa estrutura permite acompanhar o desempenho, identificar padrões economicamente relevantes e estabelecer uma base consistente para análises e decisões futuras.