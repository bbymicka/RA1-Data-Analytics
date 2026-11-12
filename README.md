# RA1, RA2 e RA3 — COVID-19 na Índia

[Repositório](https://github.com/bbymicka/RA1-Data-Analytics) · [Notebook](notebooks/ra1.ipynb) · [Documento da avaliação](docs/RA1_COVID_India_Preenchido.docx)

## 1. Problema e perguntas

Vamos preparar dados de casos, testes e vacinação nos estados e territórios da Índia. As perguntas para as próximas etapas são:

- Como os registros acumulados de casos, recuperações e óbitos evoluíram em cada estado no período disponível?
- Como o volume registrado de testes variou entre estados e ao longo do tempo?
- Como a administração da primeira e da segunda dose evoluiu nos estados durante 2021?

A RA1 termina com os dados preparados. Ainda não calculamos indicadores nem tiramos conclusões sobre a pandemia.

## 2. Fontes de dados

Os três CSVs ficam na raiz do projeto. Foram fornecidos como parte do conjunto **COVID-19 in India**, de Sudalai Rajkumar, no Kaggle. A data, a versão do download, a licença e a origem primária de cada arquivo não foram confirmadas.

| Arquivo | Linhas | Colunas | Período |
|---|---:|---:|---|
| `covid_19_india.csv` | 18.110 | 9 | 30/01/2020 a 11/08/2021 |
| `StatewiseTestingDetails.csv` | 16.336 | 5 | 01/04/2020 a 10/08/2021 |
| `covid_vaccine_statewise.csv` | 7.845 | 24 | 16/01/2021 a 16/08/2021 |

## 3. Como carregar e executar

O notebook lê os arquivos diretamente com Pandas e mostra o tamanho e as primeiras linhas de cada base. Não depende de relatórios nem de execuções anteriores.

**No Colab:** abra `notebooks/ra1.ipynb`. Antes de executar, envie os três CSVs pelo painel **Arquivos → Fazer upload**, mantendo os nomes. Execute todas as células em ordem. Ao terminar, baixe os CSVs em `data/processed` e salve uma cópia do notebook com as saídas.

**No VS Code:** use Python 3.12 e as extensões Python e Jupyter. No terminal PowerShell, na raiz do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Abra o notebook, escolha o kernel da `.venv`, reinicie o kernel e execute todas as células. Salve o arquivo para guardar as saídas. O diretório de execução pode ser a raiz do projeto ou a pasta `notebooks`.

## 4. Qualidade dos dados

Conferimos valores vazios, linhas repetidas, datas, números e nomes de estados. As tabelas desta etapa estão em português, sem mudar os nomes das colunas dos datasets.

Encontramos uma linha repetida em testes, grafias diferentes de estados e valores vazios nas três bases. Também mostramos quedas dos totais, diferenças entre colunas e valores mínimos e máximos. As quantidades aparecem nas saídas do notebook.

## 5. Limpeza e preparação

Removemos a linha idêntica, corrigimos as grafias conhecidas e padronizamos datas, horas e contagens. Valores vazios continuam vazios. Quedas e diferenças entre colunas foram mantidas, pois não temos dados para corrigi-las.

Todas as variáveis foram preservadas. Acrescentamos a linha de origem (`source_row`), o nome original do território (`state_original`) e o nível geográfico (`geographic_level`). O [dicionário](docs/data_dictionary.md) explica cada campo.

## 6. Resultado e validação

| Arquivo em `data/processed` | Linhas finais | Colunas finais |
|---|---:|---:|
| `casos.csv` | 18.110 | 12 |
| `testes.csv` | 16.335 | 8 |
| `vacinacao.csv` | 7.845 | 27 |

Os CSVs usam UTF-8, vírgulas, datas `AAAA-MM-DD` e campos vazios para ausências. A execução salva as saídas sem sobrescrever os originais.

## 7. RA2 — Streaming de registros simulados

A seção RA2 está no mesmo `notebooks/ra1.ipynb`, após o RA1. São 9 registros artificiais de novas amostras de testes em Maharashtra e Karnataka, divididos em 3 arquivos JSON. Spark Structured Streaming soma as amostras por estado em janelas Tumbling de 1 minuto. Esses registros não entram nos CSVs reais.

Instale `requirements.txt` e configure Java 17 no ambiente do kernel (`JAVA_HOME`). No Colab, instale `%pip install pyspark==3.5.7` antes do RA2 e use Java 17. No Windows, componentes nativos do Hadoop podem ser necessários. A execução foi validada em Linux pelo Docker; Colab e WSL não foram testados.

Execute as células em ordem. A função `demonstrar_streaming()` inicia a consulta, publica um arquivo por vez, aguarda `processAllAvailable()`, mostra e confere cada tabela e encerra a consulta. Para repetir, execute novamente `resultados_ra2 = demonstrar_streaming()`: entrada, nome da consulta e checkpoint são novos.

**Validação concluída pelo Docker:** notebook completo executado, código do RA1 e seis CSVs preservados. O Spark processou 3, 6 e 9 registros acumulados, confirmou os totais de cada janela e chegou a 64 novas amostras simuladas. A repetição no mesmo kernel produziu as mesmas três tabelas, sem consultas ativas ao final. Veja `reports/validation_ra2.json`. A execução nativa no Windows continua dependente da biblioteca do Hadoop que faltava no ambiente.

Para repetir os testes com o Docker Desktop aberto, execute na raiz do projeto, no PowerShell:

```powershell
docker build -t covid-ra2-validation:local -f scripts/Dockerfile.ra2 scripts
docker run --rm --mount "type=bind,source=${PWD},target=/work" covid-ra2-validation:local python scripts/validate_ra2.py
```

O script executa RA1 e RA2, repete a simulação e salva o notebook com as saídas e o relatório após as verificações. A evidência completa da repetição fica em `tmp/docker_repeat_evidence.ipynb`. A imagem Docker é apenas um ambiente de teste; não acrescenta serviços à análise.

O [PDF do notebook](output/pdf/RA1_RA2_COVID_India.pdf) inclui RA1, RA2 e as três tabelas reais do streaming. Para exportar novamente após mudanças, use Jupyter/VS Code para exportar em HTML e a opção de impressão em PDF do navegador; confira as tabelas largas do RA1.

## 8. RA3 — Análise dos dados e previsão

O [relatório do RA3](docs/ra3.md) reúne estatísticas descritivas, cinco visualizações interpretadas, a discussão sobre representatividade e a avaliação da regressão. O [script](scripts/ra3.py) usa os três CSVs preparados que já estão no repositório.

Na raiz do projeto, com Python 3.12 ou 3.13 disponível no terminal, execute:

```powershell
python -m pip install -r requirements-ra3.txt
python scripts/ra3.py
```

As tabelas e as métricas aparecem no terminal. Os gráficos e as previsões por data são gravados em `output/ra3`. A execução do RA3 é independente do notebook e do Spark.
