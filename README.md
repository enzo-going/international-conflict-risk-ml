# International Conflict Risk ML

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/Dashboard-GitHub%20Pages-222222?style=flat&logo=github&logoColor=white)

Pipeline de Machine Learning para previsão de risco de conflito armado em escala global, usando dados históricos de 194 países no formato país-ano.

🔗 **[Ver dashboard publicado](https://enzo-going.github.io/international-conflict-risk-ml/)**

---

## Resultado principal

| Modelo | F1-Score | Features |
|---|---|---|
| Logistic Regression + World Bank | **0.8722** | 33 |
| Baseline (persistência) | 0.8571 | — |

Ganho de ~0.015 sobre o baseline com validação temporal (sem vazamento de dados futuros).

---

## O que o projeto faz

- Integra dados de conflito (UCDP) com indicadores socioeconômicos (World Bank)
- Aplica engenharia de features temporais (lags, tendências)
- Treina e valida com split temporal para simular previsão real
- Gera avaliações de risco para 194 países
- Exporta resultados para SQLite e exibe via dashboard HTML

---

## Estrutura

```
├── data/               # Datasets brutos e processados
├── notebooks/          # Exploração e análise
├── src/
│   ├── pipeline/       # Coleta, limpeza e feature engineering
│   ├── models/         # Treinamento e validação
│   └── db/             # Camada SQL/SQLite
├── dashboard/          # Interface HTML publicada via GitHub Pages
└── docs/               # Documentação metodológica
```

---

## Como executar

```bash
git clone https://github.com/enzo-going/international-conflict-risk-ml.git
cd international-conflict-risk-ml
pip install -r requirements.txt
python src/pipeline/run_pipeline.py
```

---

## Stack

- **Python 3.10+** com scikit-learn, Pandas, NumPy
- **SQLite** via sqlite3 para persistência de resultados
- **Matplotlib / Seaborn** para visualizações
- **GitHub Pages** para publicação do dashboard
