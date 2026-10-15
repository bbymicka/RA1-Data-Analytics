# Dicionário de dados

Os rótulos descrevem o conteúdo informado no snapshot. Definições operacionais não confirmadas não são inventadas. Valores são preservados mesmo quando há alertas.

## Convenções

- Contagens: `Int64` anulável em memória; inteiros não negativos ou vazio no CSV. Frações, negativos, textos inválidos e valores fora do intervalo Int64 interrompem a preparação para revisão antes da exportação. Ausências reconhecidas continuam vazias.
- Datas: string ISO `AAAA-MM-DD`, validada pelo calendário. Horas: `HH:MM:SS`, sem fuso presumido.
- Texto: string. Todas as colunas originais são mantidas com os nomes abaixo.
- Ausências não são zero. Não somar acumulados entre datas nem doses com indivíduos. Recortes de vacinação têm períodos de preenchimento distintos.
- As faixas 45–60 e 60+ são mantidas literalmente; limites inclusivos e comparabilidade não foram confirmados. Não reclassificar nem somar essas faixas automaticamente.

## Metadados adicionados a cada base

| Campo | Tipo | Significado |
|---|---|---|
| source_row | inteiro | Posição do registro original, contando cabeçalho como 1; usar junto ao nome da base. |
| state_original | string | Texto territorial original, inclusive espaços e anotações. |
| geographic_level | string | national para India; unassigned para Unassigned/redistribuição; state_or_union_territory para demais categorias com chave válida. |

## casos

Arquivo original: `covid_19_india.csv`. Formato de data de entrada: `%Y-%m-%d`.

| Campo original | Campo preparado | Tipo em memória | Unidade | Significado |
|---|---|---|---|---|
| `Sno` | `sno` | Int64 anulável | identificador | Identificador sequencial da fonte; não é medida epidemiológica |
| `Date` | `date` | string | dia | Data do registro/atualização do boletim |
| `Time` | `time` | string | hora | Hora informada no boletim; fuso não especificado |
| `State/UnionTerritory` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `ConfirmedIndianNational` | `confirmed_indian_national` | Int64 anulável | pessoas registradas | Confirmados de nacionalidade indiana informados na fonte |
| `ConfirmedForeignNational` | `confirmed_foreign_national` | Int64 anulável | pessoas registradas | Confirmados de nacionalidade estrangeira informados na fonte |
| `Cured` | `cured` | Int64 anulável | pessoas registradas | Recuperados acumulados informados |
| `Deaths` | `deaths` | Int64 anulável | óbitos registrados | Óbitos acumulados informados |
| `Confirmed` | `confirmed` | Int64 anulável | casos registrados | Casos confirmados acumulados informados |

## testes

Arquivo original: `StatewiseTestingDetails.csv`. Formato de data de entrada: `%Y-%m-%d`.

| Campo original | Campo preparado | Tipo em memória | Unidade | Significado |
|---|---|---|---|---|
| `Date` | `date` | string | dia | Data do registro/atualização do boletim |
| `State` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `TotalSamples` | `total_samples` | Int64 anulável | amostras | Total de amostras testadas informado; não equivale a pessoas únicas |
| `Negative` | `negative` | Int64 anulável | resultados registrados | Resultados negativos informados; definição/cobertura detalhada não confirmada |
| `Positive` | `positive` | Int64 anulável | resultados registrados | Resultados positivos informados; não equiparar aos confirmados da outra base |

## vacinacao

Arquivo original: `covid_vaccine_statewise.csv`. Formato de data de entrada: `%d/%m/%Y`.

| Campo original | Campo preparado | Tipo em memória | Unidade | Significado |
|---|---|---|---|---|
| `Updated On` | `date` | string | dia | Data do registro/atualização do boletim |
| `State` | `state` | string | categoria | Estado, território ou categoria geográfica padronizada |
| `Total Doses Administered` | `total_doses_administered` | Int64 anulável | doses | Total de doses administradas informado |
| `Sessions` | `sessions` | Int64 anulável | sessões | Sessões de vacinação informadas; periodicidade do campo não confirmada |
| ` Sites ` | `sites` | Int64 anulável | locais | Locais de vacinação informados; não presumir total acumulado |
| `First Dose Administered` | `first_dose_administered` | Int64 anulável | doses | Primeiras doses administradas informadas |
| `Second Dose Administered` | `second_dose_administered` | Int64 anulável | doses | Segundas doses administradas informadas |
| `Male (Doses Administered)` | `male_doses_administered` | Int64 anulável | doses | Doses administradas no sexo masculino segundo o rótulo original |
| `Female (Doses Administered)` | `female_doses_administered` | Int64 anulável | doses | Doses administradas no sexo feminino segundo o rótulo original |
| `Transgender (Doses Administered)` | `transgender_doses_administered` | Int64 anulável | doses | Doses administradas na categoria transgender da fonte segundo o rótulo original |
| ` Covaxin (Doses Administered)` | `covaxin_doses_administered` | Int64 anulável | doses | Doses administradas no imunizante Covaxin segundo o rótulo original |
| `CoviShield (Doses Administered)` | `covi_shield_doses_administered` | Int64 anulável | doses | Doses administradas no imunizante CoviShield segundo o rótulo original |
| `Sputnik V (Doses Administered)` | `sputnik_v_doses_administered` | Int64 anulável | doses | Doses administradas no imunizante Sputnik V segundo o rótulo original |
| `AEFI` | `aefi` | Int64 anulável | eventos registrados | Eventos adversos após imunização informados; não estabelece causalidade ou gravidade |
| `18-44 Years (Doses Administered)` | `18_44_years_doses_administered` | Int64 anulável | doses | Doses administradas na faixa de 18–44 anos segundo o rótulo original |
| `45-60 Years (Doses Administered)` | `45_60_years_doses_administered` | Int64 anulável | doses | Doses administradas na faixa de 45–60 anos segundo o rótulo original |
| `60+ Years (Doses Administered)` | `60_plus_years_doses_administered` | Int64 anulável | doses | Doses administradas na faixa de 60+ anos segundo o rótulo original |
| `18-44 Years(Individuals Vaccinated)` | `18_44_years_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados na faixa de 18–44 anos segundo o rótulo original |
| `45-60 Years(Individuals Vaccinated)` | `45_60_years_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados na faixa de 45–60 anos segundo o rótulo original |
| `60+ Years(Individuals Vaccinated)` | `60_plus_years_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados na faixa de 60+ anos segundo o rótulo original |
| `Male(Individuals Vaccinated)` | `male_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados no sexo masculino segundo o rótulo original |
| `Female(Individuals Vaccinated)` | `female_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados no sexo feminino segundo o rótulo original |
| `Transgender(Individuals Vaccinated)` | `transgender_individuals_vaccinated` | Int64 anulável | indivíduos | Indivíduos vacinados na categoria transgender da fonte segundo o rótulo original |
| `Total Individuals Vaccinated` | `total_individuals_vaccinated` | Int64 anulável | indivíduos | Total de indivíduos vacinados informado; não substituir pelo total de doses |

## Releitura das saídas

Ao usar pandas, definir `dtype` das contagens como `Int64`, dos textos como `string` e depois converter `date` com `pd.to_datetime(..., format="%Y-%m-%d")`. O CSV, por si só, não armazena tipos. Não inferir zero para células vazias.

