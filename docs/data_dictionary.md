# Dicionário de dados

Este arquivo explica as colunas originais e os nomes usados nos dados preparados. Os valores são mantidos mesmo quando geram alertas.

## Como ler os campos

- `Int64`: números inteiros que também aceitam valores vazios. Números negativos, frações, textos inválidos ou números grandes demais para esse tipo fazem a execução parar para revisão.
- Datas: `AAAA-MM-DD`. Horas: `HH:MM:SS`. Não atribuímos um fuso horário à fonte.
- `string`: texto. Todas as colunas originais continuam presentes, com os nomes mostrados nas tabelas.
- Ausências não são zero. Não somar acumulados entre datas nem doses com indivíduos. Recortes de vacinação têm períodos de preenchimento distintos.
- As faixas 45–60 e 60+ seguem os nomes da fonte. Como não sabemos exatamente como os limites foram definidos, não somamos essas faixas automaticamente.

## Colunas adicionadas a cada base

| Campo | Tipo | Significado |
|---|---|---|
| source_row | inteiro | Posição do registro original, contando cabeçalho como 1; usar junto ao nome da base. |
| state_original | string | Nome do território como veio no arquivo, incluindo espaços e anotações. |
| geographic_level | string | national: total da Índia; unassigned: sem estado definido ou em redistribuição; state_or_union_territory: demais estados e territórios. |

## casos

Arquivo original: `covid_19_india.csv`. Formato de data de entrada: `%Y-%m-%d`.

| Campo original | Campo preparado | Tipo após a limpeza | Unidade | Significado |
|---|---|---|---|---|
| `Sno` | `sno` | Int64 | identificador | Identificador sequencial da fonte; não é medida epidemiológica |
| `Date` | `date` | string | dia | Data do registro/atualização do boletim |
| `Time` | `time` | string | hora | Hora informada no boletim; fuso não especificado |
| `State/UnionTerritory` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `ConfirmedIndianNational` | `confirmed_indian_national` | Int64 | pessoas registradas | Confirmados de nacionalidade indiana informados na fonte |
| `ConfirmedForeignNational` | `confirmed_foreign_national` | Int64 | pessoas registradas | Confirmados de nacionalidade estrangeira informados na fonte |
| `Cured` | `cured` | Int64 | pessoas registradas | Recuperados acumulados informados |
| `Deaths` | `deaths` | Int64 | óbitos registrados | Óbitos acumulados informados |
| `Confirmed` | `confirmed` | Int64 | casos registrados | Casos confirmados acumulados informados |

## testes

Arquivo original: `StatewiseTestingDetails.csv`. Formato de data de entrada: `%Y-%m-%d`.

| Campo original | Campo preparado | Tipo após a limpeza | Unidade | Significado |
|---|---|---|---|---|
| `Date` | `date` | string | dia | Data do registro/atualização do boletim |
| `State` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `TotalSamples` | `total_samples` | Int64 | amostras | Total de amostras testadas informado; não equivale a pessoas únicas |
| `Negative` | `negative` | Int64 | resultados registrados | Resultados negativos informados; definição/cobertura detalhada não confirmada |
| `Positive` | `positive` | Int64 | resultados registrados | Resultados positivos informados; não tratar como a mesma medida de confirmados da base de casos |

## vacinacao

Arquivo original: `covid_vaccine_statewise.csv`. Formato de data de entrada: `%d/%m/%Y`.

| Campo original | Campo preparado | Tipo após a limpeza | Unidade | Significado |
|---|---|---|---|---|
| `Updated On` | `date` | string | dia | Data do registro/atualização do boletim |
| `State` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `Total Doses Administered` | `total_doses_administered` | Int64 | doses | Total de doses administradas informado |
| `Sessions` | `sessions` | Int64 | sessões | Sessões de vacinação informadas; periodicidade do campo não confirmada |
| ` Sites ` | `sites` | Int64 | locais | Locais de vacinação informados; não presumir total acumulado |
| `First Dose Administered` | `first_dose_administered` | Int64 | doses | Primeiras doses administradas informadas |
| `Second Dose Administered` | `second_dose_administered` | Int64 | doses | Segundas doses administradas informadas |
| `Male (Doses Administered)` | `male_doses_administered` | Int64 | doses | Doses administradas no sexo masculino segundo o rótulo original |
| `Female (Doses Administered)` | `female_doses_administered` | Int64 | doses | Doses administradas no sexo feminino segundo o rótulo original |
| `Transgender (Doses Administered)` | `transgender_doses_administered` | Int64 | doses | Doses administradas na categoria transgênero da fonte segundo o rótulo original |
| ` Covaxin (Doses Administered)` | `covaxin_doses_administered` | Int64 | doses | Doses administradas no imunizante Covaxin segundo o rótulo original |
| `CoviShield (Doses Administered)` | `covi_shield_doses_administered` | Int64 | doses | Doses administradas no imunizante CoviShield segundo o rótulo original |
| `Sputnik V (Doses Administered)` | `sputnik_v_doses_administered` | Int64 | doses | Doses administradas no imunizante Sputnik V segundo o rótulo original |
| `AEFI` | `aefi` | Int64 | eventos registrados | Eventos adversos após imunização informados; o registro não comprova a causa nem a gravidade |
| `18-44 Years (Doses Administered)` | `18_44_years_doses_administered` | Int64 | doses | Doses administradas na faixa de 18–44 anos segundo o rótulo original |
| `45-60 Years (Doses Administered)` | `45_60_years_doses_administered` | Int64 | doses | Doses administradas na faixa de 45–60 anos segundo o rótulo original |
| `60+ Years (Doses Administered)` | `60_plus_years_doses_administered` | Int64 | doses | Doses administradas na faixa de 60+ anos segundo o rótulo original |
| `18-44 Years(Individuals Vaccinated)` | `18_44_years_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados na faixa de 18–44 anos segundo o rótulo original |
| `45-60 Years(Individuals Vaccinated)` | `45_60_years_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados na faixa de 45–60 anos segundo o rótulo original |
| `60+ Years(Individuals Vaccinated)` | `60_plus_years_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados na faixa de 60+ anos segundo o rótulo original |
| `Male(Individuals Vaccinated)` | `male_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados no sexo masculino segundo o rótulo original |
| `Female(Individuals Vaccinated)` | `female_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados no sexo feminino segundo o rótulo original |
| `Transgender(Individuals Vaccinated)` | `transgender_individuals_vaccinated` | Int64 | indivíduos | Indivíduos vacinados na categoria transgênero da fonte segundo o rótulo original |
| `Total Individuals Vaccinated` | `total_individuals_vaccinated` | Int64 | indivíduos | Total de indivíduos vacinados informado; não substituir pelo total de doses |

## Releitura das saídas

Ao reler com Pandas, use `dtype="Int64"` para contagens e `dtype="string"` para textos. Converta a data com `pd.to_datetime(..., format="%Y-%m-%d")`. O CSV não guarda esses tipos. Valores vazios não devem virar zero.

