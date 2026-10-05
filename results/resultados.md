# Resultados de profiling

Los tiempos marcados como estimados se calculan con profiling calibrado: se mide una entrada ejecutable y se extrapola por cantidad de iteraciones logicas.

## Problema 1

| n | Iteraciones logicas | Tiempo (s) | Modo |
|---:|---:|---:|---|
| 1 | 2 | 0.000001 | medido |
| 10 | 120 | 0.000015 | medido |
| 100 | 17850 | 0.002089 | medido |
| 1000 | 2505000 | 0.289970 | medido |
| 10000 | 350070000 | 40.523 | estimado por profiling calibrado |
| 100000 | 42500850000 | 4919.75 | estimado por profiling calibrado |
| 1000000 | 5000010000000 | 578783.19 | estimado por profiling calibrado |


Grafica: `results/problema_1.svg`

## Problema 2

| n | Iteraciones logicas | Tiempo (s) | Modo |
|---:|---:|---:|---|
| 1 | 0 | 0.000000400 | medido |
| 10 | 10 | 0.000001 | medido |
| 100 | 100 | 0.000011 | medido |
| 1000 | 1000 | 0.000124 | medido |
| 10000 | 10000 | 0.001325 | medido |
| 100000 | 100000 | 0.013997 | medido |
| 1000000 | 1000000 | 0.171906 | medido |


Grafica: `results/problema_2.svg`

## Problema 3

| n | Iteraciones logicas | Tiempo (s) | Modo |
|---:|---:|---:|---|
| 1 | 0 | 0.000000600 | medido |
| 10 | 9 | 0.000002 | medido |
| 100 | 825 | 0.000105 | medido |
| 1000 | 83250 | 0.011665 | medido |
| 10000 | 8332500 | 0.951819 | medido |
| 100000 | 833325000 | 95.190 | estimado por profiling calibrado |
| 1000000 | 83333250000 | 9519.13 | estimado por profiling calibrado |


Grafica: `results/problema_3.svg`
