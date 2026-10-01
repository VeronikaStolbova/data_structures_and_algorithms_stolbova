#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 2. Рекурсивные функции; динамический массив, стек и дек — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-02 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab02-recursion-structures-starter.py --variant N
"""
from __future__ import annotations
import matplotlib.pyplot as plt

import argparse
import collections
import math
import random
import statistics
import time

# ---------------------------------------------------------------------------
# 1. Рекурсивные функции (счётчик вызовов — для сравнения наивной рекурсии
#    и мемоизации; результаты счётчика включаются в отчёт)
# ---------------------------------------------------------------------------

CALLS = {"fib_naive": 0, "fib_memo": 0}  # счётчики рекурсивных вызовов


def factorial(n: int) -> int:
    """Факториал n >= 0 рекурсивно. Ожидаемая сложность: TODO (обосновать в отчёте)."""
    if n == 0:
        return 1
    return n * factorial(n - 1)

def fib_naive(n: int) -> int:
    """n-е число Фибоначчи наивной рекурсией; увеличивает CALLS["fib_naive"].
    Ожидаемая сложность: TODO (экспоненциальная — показать счётчиком вызовов).
    """
    CALLS["fib_naive"] += 1
    # TODO: F(0)=0, F(1)=1, далее F(n)=F(n-1)+F(n-2)
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """n-е число Фибоначчи с мемоизацией; увеличивает CALLS["fib_memo"].
    Ожидаемая сложность: TODO (линейная — сравнить счётчики в отчёте).
    """
    CALLS["fib_memo"] += 1
    # TODO: словарь memo передаётся по рекурсии; повторные подзадачи не пересчитываются
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

hanoimov = []
def hanoi(n: int, src: str = "A", dst: str = "C", aux: str = "B", 
          _rods: dict | None = None) -> int:
    if _rods is None:
        _rods = {"A": list(range(n, 0, -1)), "B": [], "C": []}
        global hanoimov
        hanoimov = []
    if n == 0:
        return 0
    #Перенос n-1 дисков на вспомогательный
    moves = hanoi(n - 1, src, aux, dst, _rods)
    #Перенос самого большого доступного диска с проверкой
    if not _rods[src]:
        raise ValueError("Вы пытаетесь взять диск с пустого стержня")
    disk = _rods[src].pop()
    if _rods[dst] and _rods[dst][-1] < disk:
        raise ValueError("Вы пытаетесь положить большой диск на маленький")
    _rods[dst].append(disk)
    hanoimov.append((src, dst)) # Запись перемещения
    
    #Перенос n-1 дисков на целевой
    moves += 1 + hanoi(n - 1, aux, dst, src, _rods)
    return moves
# ---------------------------------------------------------------------------
# 2. Динамический массив с ручным управлением ёмкостью (рост x2)
# ---------------------------------------------------------------------------

class DynamicArray:
    """Динамический массив поверх «сырого» буфера фиксированной ёмкости.
    Инвариант: 0 <= self._size <= self._capacity.
    Буфер имитируем списком фиксированной длины, заполненным None;
    использовать list.append/insert для буфера запрещено.
    """
    INITIAL_CAPACITY = 4

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._buffer: list = [None] * self._capacity  # «сырая» память
        self.copies = 0

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def _grow(self) -> None:
        """Увеличить ёмкость в 2 раза и скопировать элементы в новый буфер."""
        # TODO: выделить новый буфер размера 2 * capacity, перенести _size элементов
        new_capacity = self._capacity * 2
        new_buffer = [None] * new_capacity
        for i in range(self._size):
            new_buffer[i] = self._buffer[i]
            self.copies += 1  
        self._buffer = new_buffer
        self._capacity = new_capacity

    def append(self, value) -> None:
        """Добавить элемент в конец; при size == capacity сначала вызвать _grow.
        Амортизированная сложность: TODO (обосновать методом учёта в отчёте).
        """
        # TODO: рост при необходимости, запись в ячейку _buffer[_size], инкремент _size
        if self._size == self._capacity:
            self._grow()
        self._buffer[self._size] = value
        self._size += 1

    def pop(self):
        """Удалить и вернуть последний элемент. Сложность: O(1)."""
        if self._size == 0:
            raise IndexError("pop из пустого массива")
        self._size -= 1
        value = self._buffer[self._size]
        self._buffer[self._size] = None
        return value

    def get(self, index: int):
        """Вернуть элемент по индексу 0 <= index < size; иначе IndexError."""
        # TODO: проверка границ + чтение из буфера
        if index < 0 or index >= self._size:
            raise IndexError("Индекс выходит за границы")
        return self._buffer[index]

    def set(self, index: int, value) -> None:
        """Записать элемент по индексу 0 <= index < size; иначе IndexError."""
        # TODO: проверка границ + запись в буфер
        if index < 0 or index >= self._size:
            raise IndexError("Индекс выходит за границы")
        self._buffer[index] = value


# ---------------------------------------------------------------------------
# 3. Стек и дек на базе собственных структур
# ---------------------------------------------------------------------------


class Stack:
    """Стек (LIFO) на базе DynamicArray."""

    def __init__(self) -> None:
        self._data = DynamicArray()

    def __len__(self) -> int:
        return len(self._data)

    def push(self, value) -> None:
        """Положить элемент на вершину. Амортизированная сложность: TODO."""
        # TODO: делегировать DynamicArray.append
        self._data.append(value)

    def pop(self):
        """Снять элемент с вершины; для пустого стека — IndexError."""
        # TODO: прочитать последний элемент, уменьшить размер
        return self._data.pop()

    def peek(self):
        """Вернуть вершину без удаления; для пустого стека — IndexError."""
        if len(self._data) == 0:
            raise IndexError("peek из пустого стекк")
        return self._data.get(len(self._data) - 1)


class _Node:
    """Узел двусвязного списка для Deque."""
    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, next=None) -> None:  # noqa: A002
        self.value = value
        self.prev = prev
        self.next = next


class Deque:
    """Дек (двусторонняя очередь) на базе двусвязного списка.
    Все четыре операции концов должны стоить O(1) — без амортизации,
    в отличие от вставки в начало динамического массива (см. отчёт).
    """

    def __init__(self) -> None:
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def push_front(self, value) -> None:
        """Добавить элемент в начало. Сложность: TODO."""
        # TODO: создать узел, перевязать ссылки head (учесть пустой дек)
        new_node = _Node(value)
        if self._size == 0:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1


    def push_back(self, value) -> None:
        """Добавить элемент в конец. Сложность: TODO."""
        # TODO: симметрично push_front для tail
        new_node = _Node(value)
        if self._size == 0:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def pop_front(self):
        """Извлечь элемент из начала; для пустого дека — IndexError."""
        # TODO: учесть переход к пустому деку (tail тоже обнуляется)
        if self._size == 0:
            raise IndexError("pop из пустого дека")
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None  # tail обнуляется
        else:
            self._head.prev = None
        self._size -= 1
        return value

    def pop_back(self):
        """Извлечь элемент из конца; для пустого дека — IndexError."""
        if self._size == 0:
            raise IndexError("pop из пустого дека")
        value = self._tail.value
        self._tail = self._tail.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        self._size -= 1
        return value


# ---------------------------------------------------------------------------
# 4. Репрезентативные тесты и инварианты (шаги 1–3 методики верификации)
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Граничные и типовые случаи + сверка с эталонами стандартной библиотеки."""
    # --- рекурсия: сверка с math.factorial и формулой Ханойских башен ---
    assert factorial(0) == 1
    for n in range(0, 12):
        assert factorial(n) == math.factorial(n)
    CALLS["fib_naive"] = CALLS["fib_memo"] = 0
    assert fib_naive(10) == 55
    assert fib_memo(10) == 55
    assert CALLS["fib_memo"] < CALLS["fib_naive"]  # мемоизация экономит вызовы
    for n in (0, 1, 3, 8):
        assert hanoi(n) == 2 ** n - 1

    # --- DynamicArray: инвариант size <= capacity, сверка с list ---
    arr, ref = DynamicArray(), []
    for i in range(100):  # проходим несколько границ роста ёмкости
        arr.append(i * i)
        ref.append(i * i)
        assert len(arr) == len(ref) <= arr.capacity
    assert [arr.get(i) for i in range(len(arr))] == ref
    arr.set(0, -1)
    assert arr.get(0) == -1
    try:
        arr.get(len(arr))
        assert False, "ожидался IndexError"
    except IndexError:
        pass

    # --- Stack: порядок LIFO, сверка с list ---
    st, ref = Stack(), []
    for x in [1, 2, 3]:
        st.push(x)
        ref.append(x)
    assert st.peek() == ref[-1]
    while ref:
        assert st.pop() == ref.pop()
    assert len(st) == 0

    # --- Deque: порядок FIFO и работа с обоих концов, сверка с collections.deque ---
    dq, ref = Deque(), collections.deque()
    dq.push_back(1), ref.append(1)
    dq.push_front(0), ref.appendleft(0)
    dq.push_back(2), ref.append(2)
    assert dq.pop_front() == ref.popleft() == 0
    assert dq.pop_back() == ref.pop() == 2
    assert dq.pop_front() == ref.popleft() == 1
    assert len(dq) == len(ref) == 0
    try:
        dq.pop_front()
        assert False, "ожидался IndexError"
    except IndexError:
        pass
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 5. Замеры (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5


def bench(fn, *args) -> float:
    """Медиана времени выполнения fn(*args) по REPEATS запускам, с прогревом."""
    fn(*args)  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def appends_dynamic_array(n: int) -> None:
    """n последовательных append в свой DynamicArray."""
    arr = DynamicArray()
    for i in range(n):
        arr.append(i)


def inserts_front_list(n: int) -> None:
    """n вставок в начало встроенного list — ожидаемо O(n) на операцию."""
    a: list[int] = []
    for i in range(n):
        a.insert(0, i)


def inserts_front_deque(n: int) -> None:
    """n вставок в начало collections.deque — ожидаемо O(1) на операцию."""
    d: collections.deque = collections.deque()
    for i in range(n):
        d.appendleft(i)


def inserts_front_custom_deque(n: int) -> None:
    """n вставок в начало нашего Deque — ожидаемо O(1) на операцию."""
    d: Deque = Deque()
    for i in range(n):
        d.push_front(i)

def run_benchmarks(seed: int) -> None:
    """Средняя стоимость append и сравнение вставки в начало list/deque."""
    rng = random.Random(seed)
    _ = rng.random()
    
    #Сбор данных для графика и консоли
    print("\nСредняя стоимость append (DynamicArray), демонстрация амортизированной O(1):")
    sizes_for_graph = [1_000, 5_000, 10_000, 50_000, 100_000]
    avg_costs = []
    
    for n in sizes_for_graph:
        t = bench(appends_dynamic_array, n)
        cost_per_op = t / n
        avg_costs.append(cost_per_op)
        print(f"  n={n:>7}  всего t={t:.6f} c  на операцию t/n={cost_per_op:.3e} c")
        
    #Замеры вставки в начало
    print("\nВставка в начало: list.insert(0, x) против deque.appendleft и Deque.push_front:")
    for n in SIZES:
        if n > 30_000:
            continue  # вставка в начало list квадратична по суммарному времени
        t_list = bench(inserts_front_list, n)
        t_deque = bench(inserts_front_deque, n)
        t_custom = bench(inserts_front_custom_deque, n)
        print(f"  n={n:>7}  list={t_list:.6f} c  std_deque={t_deque:.6f} c  custom_deque={t_custom:.6f} c")

    #Построение графика
    print("\nПостроение графика...")
    plt.figure(figsize=(8, 5))
    plt.plot(sizes_for_graph, avg_costs, marker='o', linestyle='-', color='b', linewidth=2)
    plt.title("Амортизированная стоимость append (t/n от n)")
    plt.xlabel("Размер массива (n)")
    plt.ylabel("Время на одну операцию (t/n), сек")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("append_graph.png", dpi=300)
    print("График успешно сохранен")
    # TODO: снять аналогичные замеры для push_front своего Deque;
    # TODO: построить график t/n от n для append и включить его в отчёт;
    # TODO: провести амортизированный анализ push_back методом учёта (в отчёте).


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
