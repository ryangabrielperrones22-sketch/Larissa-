# NEXUS Platform

Plataforma unificada futurista que integra os 3 dashboards:

| Módulo | Descrição |
|--------|-----------|
| **Planner Semanal** | Kanban semanal com Excel como banco de dados |
| **Meta Ads** | Analytics de campanhas Meta Ads (Excel/CSV) |
| **Extrato Bancário** | Análise de extrato bancário (Excel/CSV) |

## Como rodar

```bash
cd nexus_platform
pip install -r requirements.txt
python app.py
```

Abra no navegador: **http://127.0.0.1:5000**

## Atalhos

- `Alt + 1` → Planner
- `Alt + 2` → Meta Ads
- `Alt + 3` → Extrato

## Arquitetura

- **Flask** serve a shell (sidebar) + os 3 HTMLs originais intactos
- Cada módulo continua 100% client-side (SheetJS + Chart.js + Tailwind)
- Processamento de Excel acontece no navegador (offline após carregar a página)
- Visual glassmorphism / neon idêntico aos HTMLs originais

## Estrutura

```
nexus_platform/
├── app.py                 # Servidor Flask
├── requirements.txt
├── templates/
│   └── index.html         # Shell com sidebar
└── static/
    ├── planner.html       # Dashboard Planner
    ├── meta_ads.html      # Dashboard Meta Ads
    └── extrato.html       # Dashboard Extrato
```
