from __future__ import annotations

import csv
import math
import statistics
import time
from pathlib import Path


INPUTS = [1, 10, 100, 1_000, 10_000, 100_000, 1_000_000]
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
PDF_DIR = ROOT / "pdf_respuestas"


def p1_iterations(n: int) -> int:
    if n < 1:
        return 0
    outer = n - (n // 2) + 1
    middle = n - (n // 2)
    inner = int(math.floor(math.log2(n))) + 1
    return outer * middle * inner


def p2_iterations(n: int) -> int:
    if n <= 1:
        return 0
    return n


def p3_iterations(n: int) -> int:
    if n < 1:
        return 0
    outer = n // 3
    inner = (n + 3) // 4
    return outer * inner


def p1_exact(n: int) -> int:
    counter = 0
    i = n // 2
    while i <= n:
        j = 1
        while j + (n // 2) <= n:
            k = 1
            while k <= n:
                counter += 1
                k *= 2
            j += 1
        i += 1
    return counter


def p2_exact(n: int) -> int:
    if n <= 1:
        return 0
    counter = 0
    i = 1
    while i <= n:
        j = 1
        while j <= n:
            counter += 1
            break
        i += 1
    return counter


def p3_exact(n: int) -> int:
    counter = 0
    i = 1
    while i <= n // 3:
        j = 1
        while j <= n:
            counter += 1
            j += 4
        i += 1
    return counter


PROBLEMS = {
    "problema_1": {
        "title": "Problema 1",
        "iterations": p1_iterations,
        "exact": p1_exact,
        "calibration_n": 1000,
        "exact_limit": 5_000_000,
        "complexity": "O(n^2 log n)",
    },
    "problema_2": {
        "title": "Problema 2",
        "iterations": p2_iterations,
        "exact": p2_exact,
        "calibration_n": 1_000_000,
        "exact_limit": 2_000_000,
        "complexity": "O(n)",
    },
    "problema_3": {
        "title": "Problema 3",
        "iterations": p3_iterations,
        "exact": p3_exact,
        "calibration_n": 10000,
        "exact_limit": 10_000_000,
        "complexity": "O(n^2)",
    },
}


def time_call(fn, n: int) -> float:
    start = time.perf_counter()
    result = fn(n)
    elapsed = time.perf_counter() - start
    expected = None
    for problem in PROBLEMS.values():
        if problem["exact"] is fn:
            expected = problem["iterations"](n)
            break
    if expected is not None and result != expected:
        raise AssertionError(f"Unexpected counter for n={n}: {result} != {expected}")
    return elapsed


def median_time(fn, n: int, repeats: int = 3) -> float:
    values = [time_call(fn, n) for _ in range(repeats)]
    return statistics.median(values)


def profile_problem(key: str, config: dict) -> list[dict[str, object]]:
    calibration_n = int(config["calibration_n"])
    calibration_ops = int(config["iterations"](calibration_n))
    calibration_time = median_time(config["exact"], calibration_n, repeats=3)
    seconds_per_op = calibration_time / max(calibration_ops, 1)

    rows: list[dict[str, object]] = []
    for n in INPUTS:
        ops = int(config["iterations"](n))
        if n == calibration_n:
            elapsed = calibration_time
            mode = "medido"
        elif ops <= int(config["exact_limit"]):
            repeats = 1 if ops > 1_000_000 else 3
            elapsed = median_time(config["exact"], n, repeats=repeats)
            mode = "medido"
        else:
            elapsed = ops * seconds_per_op
            mode = "estimado por profiling calibrado"
        rows.append(
            {
                "problema": config["title"],
                "n": n,
                "iteraciones_logicas": ops,
                "tiempo_segundos": elapsed,
                "modo": mode,
            }
        )
    return rows


def fmt_seconds(value: float) -> str:
    if value == 0:
        return "0.000000"
    if value < 0.000001:
        return f"{value:.9f}"
    if value < 1:
        return f"{value:.6f}"
    if value < 1000:
        return f"{value:.3f}"
    return f"{value:.2f}"


def write_csv(rows: list[dict[str, object]]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / "profiling_resultados.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["problema", "n", "iteraciones_logicas", "tiempo_segundos", "modo"],
        )
        writer.writeheader()
        writer.writerows(rows)


def scale_log(value: float, min_value: float, max_value: float, start: float, end: float) -> float:
    value = max(value, min_value)
    if min_value == max_value:
        return (start + end) / 2
    ratio = (math.log10(value) - math.log10(min_value)) / (
        math.log10(max_value) - math.log10(min_value)
    )
    return start + ratio * (end - start)


def write_svg(problem_key: str, rows: list[dict[str, object]]) -> None:
    width, height = 760, 460
    left, right, top, bottom = 78, 30, 35, 72
    plot_w = width - left - right
    plot_h = height - top - bottom

    ns = [float(row["n"]) for row in rows]
    times = [max(float(row["tiempo_segundos"]), 1e-9) for row in rows]
    min_n, max_n = min(ns), max(ns)
    min_t, max_t = min(times), max(times)

    points = []
    for n, t in zip(ns, times):
        x = scale_log(n, min_n, max_n, left, left + plot_w)
        y = scale_log(t, min_t, max_t, top + plot_h, top)
        points.append((x, y))

    line = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    circles = "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#1d4ed8" />'
        for x, y in points
    )
    labels = "\n".join(
        f'<text x="{x:.2f}" y="{y - 10:.2f}" text-anchor="middle" font-size="11">{fmt_seconds(t)}s</text>'
        for (x, y), t in zip(points, times)
    )

    x_ticks = "\n".join(
        f'<text x="{scale_log(n, min_n, max_n, left, left + plot_w):.2f}" y="{height - 38}" text-anchor="middle" font-size="12">{int(n):g}</text>'
        for n in ns
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{width / 2}" y="24" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700">{PROBLEMS[problem_key]["title"]}: input vs. tiempo</text>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#111827" stroke-width="1.5"/>
  <line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#111827" stroke-width="1.5"/>
  <text x="20" y="{top + plot_h / 2}" transform="rotate(-90 20 {top + plot_h / 2})" text-anchor="middle" font-family="Arial" font-size="13">Tiempo en segundos (escala log)</text>
  <text x="{left + plot_w / 2}" y="{height - 10}" text-anchor="middle" font-family="Arial" font-size="13">n (escala log)</text>
  <polyline points="{line}" fill="none" stroke="#1d4ed8" stroke-width="3"/>
  {circles}
  {labels}
  {x_ticks}
  <text x="{left}" y="{height - 38}" text-anchor="middle" font-family="Arial" font-size="12">1</text>
  <text x="{left}" y="{top + plot_h + 24}" font-family="Arial" font-size="12">Nota: puntos grandes usan estimacion por profiling calibrado cuando el bucle exacto es impracticable.</text>
</svg>
'''
    (RESULTS_DIR / f"{problem_key}.svg").write_text(svg, encoding="utf-8")


def rows_to_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "| n | Iteraciones logicas | Tiempo (s) | Modo |",
        "|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['n']} | {row['iteraciones_logicas']} | {fmt_seconds(float(row['tiempo_segundos']))} | {row['modo']} |"
        )
    return "\n".join(lines)


def write_markdown_results(grouped: dict[str, list[dict[str, object]]]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    chunks = ["# Resultados de profiling\n"]
    chunks.append(
        "Los tiempos marcados como estimados se calculan con profiling calibrado: se mide una entrada ejecutable y se extrapola por cantidad de iteraciones logicas.\n"
    )
    for key, rows in grouped.items():
        chunks.append(f"## {PROBLEMS[key]['title']}\n")
        chunks.append(rows_to_markdown(rows))
        chunks.append(f"\n\nGrafica: `results/{key}.svg`\n")
    (RESULTS_DIR / "resultados.md").write_text("\n".join(chunks), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    PDF_DIR.mkdir(exist_ok=True)

    grouped = {key: profile_problem(key, config) for key, config in PROBLEMS.items()}
    all_rows = [row for rows in grouped.values() for row in rows]
    write_csv(all_rows)
    write_markdown_results(grouped)
    for key, rows in grouped.items():
        write_svg(key, rows)

    print("Resultados generados en:")
    print(f"- {RESULTS_DIR / 'profiling_resultados.csv'}")
    print(f"- {RESULTS_DIR / 'resultados.md'}")
    print(f"- {RESULTS_DIR / 'problema_1.svg'}")
    print(f"- {RESULTS_DIR / 'problema_2.svg'}")
    print(f"- {RESULTS_DIR / 'problema_3.svg'}")


if __name__ == "__main__":
    main()
