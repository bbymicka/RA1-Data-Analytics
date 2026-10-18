import copy
import hashlib
import json
import platform
from pathlib import Path

import nbformat
from nbclient import NotebookClient
import pyspark

root = Path.cwd()
(root/'tmp').mkdir(exist_ok=True)
p = root / 'notebooks/ra1.ipynb'
original = nbformat.read(p, as_version=4)
n = copy.deepcopy(original)
assert n.cells[-1].id == 'ra2-validation-status'
n.cells.pop()
files = list(root.glob('*.csv')) + list((root/'data/processed').glob('*.csv'))
hashes = {str(f.relative_to(root)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
count = len(n.cells)
n.cells.append(nbformat.v4.new_code_cell('''# Repetindo no mesmo kernel para verificar isolamento entre execuções.
segunda_execucao_ra2 = demonstrar_streaming()
for primeira, segunda in zip(resultados_ra2, segunda_execucao_ra2):
    pd.testing.assert_frame_equal(primeira, segunda)
assert len(spark.streams.active) == 0
assert int(resultados_ra2[-1]["Novas amostras"].sum()) == 64
print("Repetição idêntica e nenhuma consulta ativa.")
spark.stop()
'''))
client = NotebookClient(n, timeout=240, kernel_name='python3', resources={'metadata': {'path': str(root)}})
try:
    client.execute()
finally:
    nbformat.write(n, root/'tmp/docker_attempt.ipynb')
assert all(hashlib.sha256((root/f).read_bytes()).hexdigest() == h for f,h in hashes.items())
assert all(a.source == b.source for a,b in zip(original.cells[:19], n.cells[:19]))
assert not any(o.output_type == 'error' for c in n.cells for o in c.get('outputs', []))
nbformat.write(n, root/'tmp/docker_repeat_evidence.ipynb')
n.cells = n.cells[:count]
n.cells[-1].source = n.cells[-1].source.replace('**Valores esperados (ainda não confirmados pelo Spark neste ambiente):**', '**Resultados confirmados na execução:**')
n.cells.append(nbformat.v4.new_markdown_cell('''### Validação da execução

O notebook completo foi executado em Linux pelo Docker, com Python 3.12, Java 17 e PySpark 3.5.7. O código do RA1 e os conteúdos dos três CSVs originais e dos três CSVs preparados permaneceram iguais.

O Spark recebeu **3, 6 e 9 registros acumulados**, e os totais por estado e janela coincidiram com os valores esperados após cada lote. Os registros em 10:01:00 e 10:02:00 entraram nas novas janelas. O total final foi **64 novas amostras simuladas**.

A simulação foi repetida no mesmo kernel: as três tabelas foram idênticas, usando novas pastas e checkpoints. Nenhuma consulta ficou ativa após o término. As tabelas acima são saídas reais do Spark. A execução nativa no Windows e a execução no Colab não foram validadas; o teste bem-sucedido foi no Docker/Linux.
'''))
n.cells[-1].id = 'ra2-validation-status'
p.write_bytes((nbformat.writes(n)+'\n').encode('utf-8'))
report = {
    'environment': {'system':platform.system(),'python':platform.python_version(),'pyspark':pyspark.__version__,'java':'17','runner':'Docker'},
    'ra1_sources_unchanged':True,'ra1_execution_passed':True,
    'csv_sha256_unchanged':hashes,'full_notebook_executed':True,
    'spark_streaming_passed':True,'second_streaming_execution_passed':True,
    'same_kernel_repetition_identical':True,'active_queries_after':0,
    'cumulative_records':[3,6,9],'total_samples':64,
    'native_windows_validated':False,'colab_validated':False,
}
(root/'reports/validation_ra2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS: full notebook, unchanged RA1/CSVs, streaming batches, boundary windows and repeat.')
