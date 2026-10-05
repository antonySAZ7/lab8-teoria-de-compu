# Laboratorio 8 - Teoria de la Computacion

Este repositorio contiene las implementaciones, el profiling y las respuestas teoricas del Laboratorio 8.

## Estructura

- `src/lab8_profiling.py`: implementacion de los problemas 1, 2 y 3, medicion de tiempos y generacion de resultados.
- `results/profiling_resultados.csv`: resultados en formato CSV.
- `results/resultados.md`: tablas de resultados.
- `results/problema_1.svg`, `results/problema_2.svg`, `results/problema_3.svg`: graficas de input vs. tiempo.
- `pdf_respuestas/README_PDF.md`: texto listo para copiar y pegar en el PDF.

## Requisitos

- Python 3.10 o superior.
- No se necesitan librerias externas.

## Ejecucion

Desde la raiz del repositorio:

```bash
python src/lab8_profiling.py
```

El script genera nuevamente:

```text
results/profiling_resultados.csv
results/resultados.md
results/problema_1.svg
results/problema_2.svg
results/problema_3.svg
```

## Nota sobre el profiling

En los problemas 1 y 3, ejecutar los bucles completos para `n = 1,000,000` no es practico porque la cantidad de iteraciones llega a billones. Por eso, el script:

1. Ejecuta exactamente los programas para entradas pequenas.
2. Cuenta las iteraciones logicas exactas para todos los valores de `n`.
3. Estima los tiempos grandes usando profiling calibrado con entradas que si son ejecutables.

Esto mantiene la relacion con la complejidad teorica y permite presentar la tabla y la grafica solicitadas.

## Video

Enlace al video de ejecucion: PENDIENTE

## Subir a GitHub

Crear un repositorio vacio en GitHub y luego ejecutar:

```bash
git add .
git commit -m "Laboratorio 8"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Reemplazar `URL_DEL_REPOSITORIO` por la URL del repositorio creado en GitHub.
