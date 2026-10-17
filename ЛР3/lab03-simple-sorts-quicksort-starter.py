#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import sys
import time
import traceback
import matplotlib.pyplot as plt
import math

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: TODO (обосновать в отчёте).
    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    # TODO: реализовать; считать сравнения и обмены
    arr = list(a)
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return arr, comparisons, swaps


def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO (лучший/худший случаи)."""
    # TODO: реализовать; считать сравнения и перемещения (сдвиги)
    arr = list(a)
    n = len(arr)
    comparisons = 0
    moves = 0
    for i in range(1, n):
        x = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > x:
            comparisons += 1
            arr[j + 1] = arr[j]
            moves += 1
            j -= 1
        if j >= 0:
            comparisons += 1
        arr[j + 1] = x
    return arr, comparisons, moves


def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO (почему не зависит от входа?)."""
    # TODO: реализовать; считать сравнения и обмены
    arr = list(a)
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        m = i #минимум
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[m]:
                m = j
        if m != i:
            arr[i], arr[m] = arr[m], arr[i]
            swaps += 1
    return arr, comparisons, swaps


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.
    Ожидаемая сложность: в среднем TODO, в худшем случае TODO (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    if rng is None:
        rng = random.Random()
    # TODO: реализовать (рекурсивно или циклом со стеком);
    # TODO: опорный элемент — a[rng.randrange(lo, hi)], не первый и не последний.
    arr = list(a)
    def sort_part(lo, hi):
        if lo >= hi:
            return
        #случайный опорный
        k = rng.randrange(lo, hi + 1)
        arr[k], arr[hi] = arr[hi], arr[k]
        #разбиение Ломуто
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        #рекурсия
        sort_part(lo, i - 1)
        sort_part(i + 1, hi)

    sort_part(0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """
    # TODO: подготовить пары, прогнать все четыре сортировки, напечатать итог
    data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    print("\nДемонстрация стабильности:")
    print("Вход:", data)

    ref = sorted(data, key=lambda p: p[0])
    print("Эталон (sorted):", ref)
    print()

    #пузырёк
    arr = list(data)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    print("bubble_sort:", arr, "стабильна" if arr == ref else "не стабильна")

    #вставки
    arr = list(data)
    for i in range(1, len(arr)):
        x = arr[i]
        j = i - 1
        while j >= 0 and arr[j][0] > x[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x
    print("insertion_sort:", arr, "стабильна" if arr == ref else "не стабильна")

    #выбором
    arr = list(data)
    n = len(arr)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if arr[j][0] < arr[m][0]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]
    print("selection_sort:", arr, "стабильна" if arr == ref else "не стабильна")

    #QuickSort
    arr = list(data)
    rng = random.Random(42)
    def qs(lo, hi):
        if lo >= hi:
            return
        k = rng.randrange(lo, hi + 1)
        arr[k], arr[hi] = arr[hi], arr[k]
        pivot = arr[hi][0]
        i = lo
        for j in range(lo, hi):
            if arr[j][0] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        qs(lo, i - 1)
        qs(i + 1, hi)
    qs(0, len(arr) - 1)
    print("quick_sort:", arr, "стабильна" if arr == ref else "не стабильна")


# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


class SelfCheckError(Exception):
    """Нарушен контракт или инвариант реализации."""


def expect(condition: bool, message: str) -> None:
    """Явная проверка вместо assert: assert-ы исчезают при запуске python -O."""
    if not condition:
        raise SelfCheckError(message)


def check_algorithm(fn) -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for a in boundary:
        res = fn(list(a))
        expect(isinstance(res, list), f"на {a} возвращён {type(res).__name__}, а не список")
        expect(is_sorted(res), f"нарушен порядок на {a}: получено {res}")
        expect(sorted(res) == sorted(a), f"не перестановка входа {a}: получено {res}")

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        res = fn(list(a))
        expect(res == sorted(a), f"расходится с sorted() на {a}: получено {res}")


def check_counters() -> None:
    """Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе."""
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    expect(comparisons == 10,
           f"selection_sort: неверный счётчик сравнений — {comparisons}, ожидалось 10")
# TODO: добавить собственные проверки (стабильность, счётчики пузырька и вставок)
#       и описать их в отчёте.
def check_stability() -> None:
    #Проверка стабильности: пузырёк и вставки сохраняют порядок меток
    data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    # пузырёк
    arr = list(data)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    expect(arr == [(1, "b"), (1, "d"), (2, "a"), (2, "c")],
           "bubble_sort должен быть стабильным")

    # вставки
    arr = list(data)
    for i in range(1, len(arr)):
        x = arr[i]
        j = i - 1
        while j >= 0 and arr[j][0] > x[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x
    expect(arr == [(1, "b"), (1, "d"), (2, "a"), (2, "c")],
           "insertion_sort должен быть стабильным")

def check_bubble_counters() -> None:
    #Пузырёк на упорядоченном массиве: n-1 сравнений, 0 обменов
    _, comparisons, swaps = bubble_sort([1, 2, 3, 4, 5])
    expect(comparisons == 4 and swaps == 0,
           f"bubble_sort на упорядоченном: ожидали 4/0, получили {comparisons}/{swaps}")

def check_insertion_counters() -> None:
    #Вставки на упорядоченном массиве: n-1 сравнений, 0 сдвигов
    _, comparisons, moves = insertion_sort([1, 2, 3, 4, 5])
    expect(comparisons == 4 and moves == 0,
           f"insertion_sort на упорядоченном: ожидали 4/0, получили {comparisons}/{moves}")

def self_check() -> None:
    """Все проверки по разделам; при любой ошибке замеры не выполняются."""
    # fn=fn фиксирует функцию текущего шага цикла (иначе все лямбды увидят последнюю)
    checks = [(name, lambda fn=fn: check_algorithm(fn)) for name, fn in ALGORITHMS.items()]
    checks.append(("счётчики", check_counters))
    checks.append(("стабильность", check_stability))
    checks.append(("счётчики пузырька", check_bubble_counters))
    checks.append(("счётчики вставок", check_insertion_counters))
    failed = 0
    print("self_check:")
    for name, check in checks:
        try:
            check()
        except NotImplementedError as err:
            where = traceback.extract_tb(err.__traceback__)[-1].name
            print(f"  {name}: не реализовано — {where} (TODO)")
            failed += 1
        except SelfCheckError as err:
            print(f"  {name}: ОШИБКА — {err}")
            failed += 1
        except Exception:  # noqa: BLE001 — падение реализации тоже результат проверки
            print(f"  {name}: ИСКЛЮЧЕНИЕ")
            traceback.print_exc(file=sys.stdout)
            failed += 1
        else:
            print(f"  {name}: OK")
    if failed:
        raise SystemExit(f"self_check: не пройдено разделов — {failed}; "
                         f"замеры выполняются только после всех проверок.")
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов + log-log графики."""
    results = {
        "bubble_sort": {"упорядоченный": [], "случайный": [], "обратный": []},
        "insertion_sort": {"упорядоченный": [], "случайный": [], "обратный": []},
        "selection_sort": {"упорядоченный": [], "случайный": [], "обратный": []},
        "quick_sort": {"упорядоченный": [], "случайный": [], "обратный": []},
    }

    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]

    for name, fn, sizes in plans:
        print(f"\n{name}:")
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                t = bench(fn, data)
                results[name][cls].append((n, t))
                print(f"  n={n:>7}  вход={cls:<13} t={t:.6f} c")

    # log-log графики
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    algs = ["bubble_sort", "insertion_sort", "selection_sort", "quick_sort"]

    for ax, name in zip(axes, algs):
        for cls, points in results[name].items():
            if not points:
                continue
            ns = [p[0] for p in points]
            ts = [p[1] for p in points]
            ax.loglog(ns, ts, "o-", label=cls)
        ax.set_title(name)
        ax.set_xlabel("n")
        ax.set_ylabel("время, с")
        ax.legend()
        ax.grid(True, which="both", ls="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("lab03_loglog.png", dpi=150)
    print("\nГрафик сохранён в lab03_loglog.png")
    plt.show()

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
