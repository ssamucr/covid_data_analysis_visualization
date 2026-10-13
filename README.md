---
title: COVID-19 Dashboard
emoji: 🦠
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Visualización de la propagación del COVID-19

Proyecto final del curso **Gestión y Análisis de Datos e Información** (Universidad Tecnológica de Panamá).
Dashboard interactivo hecho con **Dash + Plotly** sobre el dataset de COVID-19 de
[Our World in Data](https://github.com/owid/covid-19-data) (datos hasta junio de 2024).

**Demo:** <https://covid-dashboard-6ejn.onrender.com> (en el plan gratuito de Render la primera carga puede tardar hasta un minuto).

## Qué muestra

- Totales globales (casos, muertes y vacunaciones) y nuevos casos a la fecha elegida.
- Para el país seleccionado: casos, muertes y personas vacunadas, con sus gráficas contra el tiempo.
- Nuevas muertes vs. personas vacunadas, por país y comparando varios países a la vez.
- Mapa mundial de vacunación y relación entre nuevos casos e índice de restricción (*stringency*).

## Ejecutar

Requiere Python 3.9 o superior.

```bash
pip install -r requirements.txt
python main.py
```

Abre <http://127.0.0.1:8050>.

## Despliegue

La app se publica en Hugging Face Spaces con el `Dockerfile` incluido (gunicorn en el puerto 7860).
El bloque YAML al inicio de este README es la configuración del Space.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `main.py` | Aplicación Dash (layout y callbacks). |
| `assets/styles.css` | Estilos del dashboard. |
| `owid-covid-data-preprocesado.csv.gz` | Dataset ya procesado que consume la app (comprimido). |
| `Preprocesamiento.ipynb` | Notebook que limpia el dataset original y genera el archivo anterior. |

## Regenerar el dataset procesado

1. Descarga `owid-covid-data.csv` desde OWID y colócalo junto al notebook.
2. Ejecuta `Preprocesamiento.ipynb`: rellena valores acumulados, conserva las columnas relevantes y
   agrega el grupo de ingresos de cada país. Escribe `owid-covid-data-preprocesado.csv.gz`.

## Equipo

Steven Guerra, Alberto Bellera, Juan Cortés, Neel Patel, Samuel Castro y Yeshua Zapata.

> Este repositorio se publicó en octubre de 2026, dos años después de entregar el proyecto (julio de 2024),
> porque la subida original a GitHub no se había completado.
