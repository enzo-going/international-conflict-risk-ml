# Contribuindo

Pull requests são bem-vindos. Para mudanças grandes, abra uma issue antes para
discutir o que você pretende alterar.

Antes de abrir o PR, rode o mesmo que o CI roda:

```bash
pip install -r requirements.txt
ruff check .
python src/validation/validate_pipeline_state.py
python src/validation/validate_project_artifacts.py
python src/validation/validate_reproducibility_contract.py
```

Os validadores conferem o estado do pipeline, os artefatos exigidos (arquivos,
colunas dos CSVs, métricas) e o contrato de reprodutibilidade. O F1 do modelo
principal e do baseline e o número de features e de gráficos ficam fixados em
`validate_reproducibility_contract.py`. Se a mudança altera esses números de
propósito, atualize o contrato no mesmo PR.
