# RA1 — COVID-19 na Índia

Repositório: [RA1 Data Analytics](https://github.com/bbymicka/RA1-Data-Analytics).

Documento da entrega: [RA1 preenchido](docs/RA1_COVID_India_Preenchido.docx).

O projeto prepara três bases históricas com Python e Pandas. A entrega principal é [notebooks/ra1.ipynb](notebooks/ra1.ipynb), com as seis etapas da RA1, código comentado e saídas salvas.

## O que o projeto faz

Organiza casos, testagem e vacinação para responder, nas próximas etapas:

- Como casos, recuperações e óbitos acumulados evoluíram por estado?
- Como o volume registrado de testes variou entre estados e datas?
- Como primeiras e segundas doses evoluíram durante 2021?

O notebook lê os CSVs, mostra problemas de qualidade, padroniza nomes e tipos, remove uma duplicata idêntica e salva as bases separadas. Ausências, revisões dos acumulados e divergências são preservadas. Não há junções, interpolação ou conclusões epidemiológicas nesta entrega.

## Arquivos necessários

- `notebooks/ra1.ipynb`: toda a preparação, sem importar scripts do projeto.
- `covid_19_india.csv`, `StatewiseTestingDetails.csv` e `covid_vaccine_statewise.csv`: originais preservados na raiz.
- `data/processed/`: resultados `casos.csv`, `testes.csv` e `vacinacao.csv`.
- [Dicionário de dados](docs/data_dictionary.md): campos, tipos e unidades.
- [Validação](reports/validation.json): registro das execuções e da comparação com a versão anterior.
- `requirements.txt`: dependências para executar localmente.

Os arquivos foram fornecidos como provenientes do conjunto COVID-19 in India, de Sudalai Rajkumar, distribuído no Kaggle. A versão e a data do download não foram informadas. A origem primária específica de cada arquivo não foi confirmada.

## Executar no Google Colab

1. No Colab, abra **Arquivo → Fazer upload de notebook** e selecione `notebooks/ra1.ipynb`.
2. Execute todas as células em ordem. Quando solicitado, envie os três CSVs originais, mantendo os nomes.
3. Confira as tabelas de qualidade e o resumo final.
4. No painel **Arquivos**, baixe os resultados em `data/processed`.
5. Salve o notebook executado por **Arquivo → Fazer download → Fazer download do .ipynb**.

O Colab normalmente inclui Pandas. Caso o import falhe, instale com `%pip install pandas` em uma célula antes da execução. O notebook não precisa do Google Drive nem dos relatórios antigos. O fluxo de upload foi preparado, mas não foi testado em uma sessão real do Colab.

## Executar no VS Code

Use Python 3.12 e as extensões Python e Jupyter. No terminal, na raiz do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Abra `notebooks/ra1.ipynb`, selecione o kernel da `.venv` e use **Restart Kernel and Run All Cells**. Salve o notebook após a execução para guardar as saídas. A localização dos dados funciona com o diretório de execução na raiz ou em `notebooks`.

A preparação usa Pandas e biblioteca padrão. `ipykernel` permite executar as células no VS Code; não é uma biblioteca de análise. O ambiente usado para validar esta entrega foi Python 3.12.14 com Pandas 3.0.1, disponível no aplicativo; esse caminho local não aparece no notebook.

## Resultados e cuidados

| Base | Entrada | Saída | Colunas finais | Duplicatas removidas |
|---|---:|---:|---:|---:|
| Casos | 18.110 | 18.110 | 12 | 0 |
| Testes | 16.336 | 16.335 | 8 | 1 |
| Vacinação | 7.845 | 7.845 | 27 | 0 |

Os CSVs usam UTF-8, vírgulas, datas `AAAA-MM-DD` e células vazias para ausências. Todas as variáveis são mantidas, junto de `source_row`, `state_original` e `geographic_level`. Uma nova execução substitui somente as saídas.

Não some acumulados entre datas ou India aos estados. Doses, indivíduos e amostras são medidas diferentes. Confira as lacunas antes de escolher variáveis e períodos. Se novos arquivos trouxerem chaves conflitantes, datas ou contagens inválidas, o notebook interrompe a preparação para revisão antes de exportar.

## Simplificação e validação

O notebook substitui o pipeline externo, o esquema JSON, os scripts de geração/execução e os testes específicos da implementação antiga. Os relatórios detalhados foram substituídos pelas tabelas do notebook e por `reports/validation.json`. O dicionário foi mantido e atualizado.

A validação executou o notebook em três kernels novos: a partir da raiz sem saídas anteriores, a partir de `notebooks` sem saídas anteriores e novamente sobre resultados já gerados. Foram comparadas todas as células dos CSVs e seus hashes com a versão anterior; os três arquivos permaneceram idênticos byte a byte. Os hashes dos originais também foram preservados. O arquivo `.ipynb` entregue contém as células executadas e suas saídas.

Essas execuções verificam o notebook em kernels Python locais. A interface do VS Code e uma sessão real do Colab não foram usadas na validação.

