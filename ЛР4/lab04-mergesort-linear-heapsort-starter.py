#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 4. MergeSort, Counting, Radix и HeapSort: оценка производительности — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-04 и правилами использования генеративного ИИ
(docs/ai-verification.md). QuickSort перенесите из собственной ЛР 3.

Запуск: python lab04-mergesort-linear-heapsort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import sys
import time
import traceback
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Сортировки (реализуются вручную; sorted() используется только как эталон)
# ---------------------------------------------------------------------------


def merge(left: list, right: list, key) -> list:
    """Стабильное слияние двух отсортированных списков в новый список.
    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: TODO (обосновать в отчёте).
    """
    # TODO: два индекса, сравнение key(left[i]) <= key(right[j])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(a: list, key=lambda x: x) -> list:
    """MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: TODO."""
    # TODO: рекурсивное деление пополам + merge()
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], key)
    right = merge_sort(a[mid:], key)
    return merge(left, right, key)


def counting_sort(a: list[int], key_max: int) -> list[int]:
    """Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].
    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память: TODO — выразить через n и k = key_max + 1;
    ограничение диапазона ключей обсудить в отчёте.
    """
    # TODO: реализовать; проход расстановки — с конца массива (иначе теряется устойчивость)
    n = len(a)
    k = key_max + 1
    count = [0] * k
    for x in a:
        count[x] += 1 
    for i in range(1, k):
        count[i] += count[i - 1]
    result = [0] * n
    # Проход с конца массива для сохранения устойчивости
    for i in range(n - 1, -1, -1):
        x = a[i]
        count[x] -= 1
        result[count[x]] = x
    return result


def radix_sort_lsd(a: list[int]) -> list[int]:
    """RadixSort LSD по десятичным разрядам, неотрицательные целые.
    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему. Ожидаемая сложность: TODO — выразить через n и число разрядов d.
    """
    # TODO: цикл по разрядам (exp = 1, 10, 100, ...) с устойчивой сортировкой
    # по цифре (a[i] // exp) % 10; объяснить, почему без устойчивости
    # внутреннего прохода алгоритм неверен
    if not a:
        return a
    max_val = max(a)
    exp = 1
    result = a[:]
    while max_val // exp > 0:
        count = [0] * 10
        for x in result:
            digit = (x // exp) % 10
            count[digit] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
            
        next_result = [0] * len(result)
        # Обратный проход для устойчивости
        for i in range(len(result) - 1, -1, -1):
            x = result[i]
            digit = (x // exp) % 10
            count[digit] -= 1
            next_result[count[digit]] = x
        result = next_result
        exp *= 10
    return result


def sift_down(a: list[int], i: int, n: int) -> None:
    """Просейка вниз элемента i в куче a[0:n] (max-heap), на месте."""
    # TODO: спуск с обменом с большим из потомков, пока нарушено свойство кучи
    root = i
    while True:
        left = 2 * root + 1
        right = 2 * root + 2
        largest = root
        # Если левый потомок существует и больше текущего наибольшего
        if left < n and a[left] > a[largest]:
            largest = left
        # Если правый потомок существует и больше текущего наибольшего
        if right < n and a[right] > a[largest]:
            largest = right
        # Если наибольший элемент не корень, меняем их местами и продолжаем спуск
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            root = largest  #спускаемся на уровень ниже
        else:
            break

def heap_sort(a: list[int]) -> None:
    """HeapSort in-place: сортирует список a на месте, без вспомогательного массива.

    Схема: построение max-кучи просейками вниз (снизу вверх, O(n)),
    затем обмен вершины с последним элементом и просейка. Сложность: TODO.
    """
    # TODO: построение кучи + фаза извлечения максимумов
    n = len(a)
    #Построение кучи за O(n)
    for start in range((n - 2) // 2, -1, -1):
        sift_down(a, start, n)
    #извлечение максимумов
    for end in range(n - 1, 0, -1):
        # Меняем местами корень с последним элементом текущей кучи
        a[0], a[end] = a[end], a[0]
        # Восстанавливаем свойство кучи для оставшейся части
        # Новый корень (бывший последний элемент) просеиваем вниз
        sift_down(a, 0, end)


def quick_sort(a: list[int]) -> list[int]:
    """QuickSort с рандомизацией опорного элемента — перенести из своей ЛР 3."""
    rng = random.Random(42)  # фиксированный seed для воспроизводимости
    arr = list(a)

    def sort_part(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        # Случайный опорный → обмен с последним
        k = rng.randrange(lo, hi + 1)
        arr[k], arr[hi] = arr[hi], arr[k]

        # Разбиение Ломуто
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]

        sort_part(lo, i - 1)
        sort_part(i + 1, hi)

    sort_part(0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 2. Верификация: инварианты + сверка с эталоном sorted()
#    (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------


class SelfCheckError(Exception):
    """Нарушен контракт или инвариант реализации."""


def expect(condition: bool, message: str) -> None:
    """Явная проверка вместо assert: assert-ы исчезают при запуске python -O."""
    if not condition:
        raise SelfCheckError(message)


def heap_sorted(a: list[int]) -> list[int]:
    """heap_sort сортирует на месте: проверяется тот список, который ему передали."""
    buf = list(a)
    heap_sort(buf)
    return buf


# Каждая функция возвращает отсортированный список; ключи — целые из [0, 999].
SORTS = {
    "merge_sort": lambda a: merge_sort(a),
    "counting_sort": lambda a: counting_sort(a, key_max=999),
    "radix_sort_lsd": lambda a: radix_sort_lsd(a),
    "heap_sort": lambda a: heap_sorted(a),
    "quick_sort": lambda a: quick_sort(a),
}


def check_sort(fn) -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [0],                   # нулевой ключ
        [5, 5, 5],             # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for a in boundary:
        res = fn(list(a))
        expect(isinstance(res, list), f"на {a} возвращён {type(res).__name__}, а не список")
        expect(res == sorted(a), f"на {a} получено {res}, ожидалось {sorted(a)}")

    # Случайные тесты: инвариант перестановки + сверка с эталоном
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(0, 999) for _ in range(rng.randint(0, 60))]
        res = fn(list(a))
        expect(sorted(res) == sorted(a), f"не перестановка входа {a}: получено {res}")
        expect(res == sorted(a), f"расходится с sorted() на {a}: получено {res}")


def check_merge_stability() -> None:
    """Стабильность слияния на парах (ключ, порядковый номер): эталон sorted() стабилен,
    поэтому при равных ключах порядок номеров обязан совпасть."""
    rng = random.Random(0)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    got = merge_sort(pairs, key=lambda p: p[0])
    expect(got == sorted(pairs, key=lambda p: p[0]),
           "merge_sort нестабилен: при равных ключах нарушен исходный порядок номеров")


def check_heap_property() -> None:
    """Проверка свойства max-кучи после построения."""
    # Создаём тестовый массив
    test_data = [random.randint(0, 1000) for _ in range(100)]
    n = len(test_data)
    # Строим кучу (как в heap_sort)
    for start in range((n - 2) // 2, -1, -1):
        sift_down(test_data, start, n)
    
    # Проверяем свойство кучи: для каждого узла i
    # a[i] >= a[2i+1] и a[i] >= a[2i+2] (если потомки существуют)
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            expect(test_data[i] >= test_data[left],
                   f"Нарушено свойство кучи в узле {i}: {test_data[i]} < {test_data[left]}")
        if right < n:
            expect(test_data[i] >= test_data[right],
                   f"Нарушено свойство кучи в узле {i}: {test_data[i]} < {test_data[right]}")


def check_radix_stability() -> None:
    """Проверка устойчивости поразрядной сортировки radix sort."""
    # Создаём массив пар (число, метка), где числа имеют одинаковые разряды
    # Например: 21, 22, 11, 12 — при сортировке по десяткам 11 и 12 имеют одинаковый разряд
    data_with_labels = [(21, 'a'), (22, 'b'), (11, 'c'), (12, 'd'), (21, 'e')]
    # Извлекаем только числа для сортировки
    numbers = [x[0] for x in data_with_labels]
    # Создаём массив индексов для отслеживания порядка
    indexed_numbers = [(num, idx) for idx, (num, _) in enumerate(data_with_labels)]
    # Модифицируем radix_sort для работы с парами (число, индекс)
    def radix_sort_with_index(arr):
        if not arr:
            return arr
        max_val = max(x[0] for x in arr)
        exp = 1
        result = arr[:]
        
        while max_val // exp > 0:
            count = [0] * 10
            for x in result:
                digit = (x[0] // exp) % 10
                count[digit] += 1
            
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            next_result = [0] * len(result)
            # Обратный проход для устойчивости
            for i in range(len(result) - 1, -1, -1):
                x = result[i]
                digit = (x[0] // exp) % 10
                count[digit] -= 1
                next_result[count[digit]] = x
            
            result = next_result
            exp *= 10
        
        return result
    
    sorted_indexed = radix_sort_with_index(indexed_numbers)
    
    # Проверяем устойчивость: элементы с одинаковыми числами должны сохранить исходный порядок
    # Группируем по числам
    from collections import defaultdict
    groups = defaultdict(list)
    for num, idx in sorted_indexed:
        groups[num].append(idx)
    
    # Для каждой группы проверяем, что индексы идут по возрастанию
    for num, indices in groups.items():
        expect(indices == sorted(indices),
               f"Нарушена устойчивость radix sort: для числа {num} индексы {indices} не отсортированы")


def self_check() -> None:
    """Все проверки по разделам; при любой ошибке замеры не выполняются."""
    # fn=fn фиксирует функцию текущего шага цикла (иначе все лямбды увидят последнюю)
    checks = [(name, lambda fn=fn: check_sort(fn)) for name, fn in SORTS.items()]
    checks.append(("стабильность merge_sort", check_merge_stability))
    checks.append(("свойство кучи после построения", check_heap_property))
    checks.append(("устойчивость поразрядного прохода radix", check_radix_stability))
    failed = 0
    print("self_check:")
    for name, check in checks:
        try:
            check()
        except NotImplementedError as err:
            where = traceback.extract_tb(err.__traceback)[-1].name
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

    if failed:
        raise SystemExit(f"self_check: не пройдено разделов — {failed}; "
                         f"замеры выполняются только после всех проверок.")
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 3. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5
SMALL_KEY_MAX = 100        # узкий диапазон: counting уместен
WIDE_KEY_MAX = 10**9       # широкий диапазон: counting теряет смысл (обсудить в отчёте)


def make_datasets(rng: random.Random, n: int) -> dict[str, list[int]]:
    """Массивы разных распределений и диапазонов ключей для размера n."""
    almost = list(range(n))
    for _ in range(max(1, n // 100)):  # ~1 % случайных обменов
        i, j = rng.randrange(n), rng.randrange(n)
        almost[i], almost[j] = almost[j], almost[i]
    return {
        "random_wide": [rng.randint(0, WIDE_KEY_MAX) for _ in range(n)],
        "random_small": [rng.randint(0, SMALL_KEY_MAX) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "almost_sorted": almost,
    }


def bench(fn, data: list[int]) -> float:
    """Медиана времени fn на копии data по REPEATS запускам, с прогревом.

    Каждый запуск получает свежую копию: сортировка на месте не должна
    превращать последующие запуски в сортировку уже отсортированного массива.
    """
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        buf = list(data)
        t0 = time.perf_counter()
        fn(buf)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)

# Основная функция бенчмарка с построением графиков

def run_benchmarks(seed: int) -> None:
    rng = random.Random(seed)
    
    # Используем понятные имена для графиков
    algorithms = [
        ("MergeSort", merge_sort),
        ("CountingSort", lambda a: counting_sort(a, key_max=max(a, default=0))),
        ("RadixSort", radix_sort_lsd),
        ("HeapSort", lambda a: (heap_sort(a), a)[1]),  # in-place, но возвращаем для единообразия
        ("QuickSort", quick_sort),
        ("sorted()", sorted),
    ]
    
    # Структура для хранения данных графиков: results[распределение][алгоритм] = [(n, время), ...]
    results = {}
    
    for n in SIZES:
        datasets = make_datasets(rng, n)
        print(f"\nn = {n}:")
        
        for dist_name, data in datasets.items():
            if dist_name not in results:
                results[dist_name] = {algo_name: [] for algo_name, _ in algorithms}
                
            print(f"  распределение '{dist_name}':")
            for algo_name, fn in algorithms:
                # Специальная обработка границы применимости CountingSort
                if algo_name == "CountingSort" and dist_name == "random_wide":
                    print(f"    {algo_name:>18}: пропуск (диапазон ключей > доступной памяти)")
                    continue
                
                try:
                    t = bench(fn, data)
                    results[dist_name][algo_name].append((n, t))
                    print(f"    {algo_name:>18}: t = {t:.6f} c")
                except MemoryError:
                    print(f"    {algo_name:>18}: MemoryError")
                except Exception as e:
                    print(f"    {algo_name:>18}: Ошибка ({type(e).__name__})")

    # ПОСТРОЕНИЕ LOG-LOG ГРАФИКОВ
    distributions = list(results.keys())
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for idx, dist_name in enumerate(distributions):
        ax = axes[idx]
        for algo_name, _ in algorithms:
            points = results[dist_name].get(algo_name, [])
            if not points:
                continue
            
            ns = [p[0] for p in points]
            ts = [p[1] for p in points]
            
            # Рисуем линию с маркерами
            ax.loglog(ns, ts, "o-", label=algo_name, linewidth=2, markersize=6)
            
        ax.set_title(f"Распределение: {dist_name}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Размер массива n (логарифмическая шкала)")
        ax.set_ylabel("Время выполнения, с (логарифмическая шкала)")
        ax.legend(fontsize=9, loc='upper left')
        ax.grid(True, which="both", ls="--", alpha=0.6)

    # 6-й subplot (пустой) используем для общей легенды или подписи
    if len(distributions) < 6:
        axes[-1].axis('off')
        axes[-1].text(0.5, 0.5, 
                      "Сравнение алгоритмов сортировки\n(Lab 04)\n\n"
                      "• O(n log n): Merge, Heap, Quick, sorted\n"
                      "• O(n + k): Counting (только narrow)\n"
                      "• O(d·(n+b)): Radix LSD",
                      ha='center', va='center', fontsize=11,
                      bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="orange"))

    plt.tight_layout()
    plt.savefig("lab04_loglog.png", dpi=150, bbox_inches='tight')
    print("\nГрафик успешно сохранён в файл: lab04_loglog.png")
    plt.show()
    # TODO: построить log-log графики (matplotlib) по каждому распределению;
    # TODO: заполнить таблицу свойств: время (лучший/средний/худший),
    #       память, стабильность, ограничения — для всех шести сортировок;
    # TODO: объяснить расхождения замеров с асимптотикой в отчёте.



def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
