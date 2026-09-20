def power(x, n):
    """Вычисляет степень n числа x (n >= 1)."""
    z = 1
    i = 1
    while n >= i:
        z = z * x
        i = i + 1
    return z


def power_traced(x, n):
    """Функция возведения в степень с трассировкой всех переменных"""
    trace = []
    z = 1
    trace.append(("z=1", {"x": x, "n": n, "z": z}))

    i = 1
    trace.append(("i=1", {"x": x, "n": n, "z": z, "i": i}))

    while n >= i:
        trace.append((f"check n>=i ({n}>={i})", {"x": x, "n": n, "z": z, "i": i}))
        z = z * x
        trace.append(("z=z*x", {"x": x, "n": n, "z": z, "i": i}))
        i = i + 1
        trace.append(("i=i+1", {"x": x, "n": n, "z": z, "i": i}))

    trace.append(("exit", {"x": x, "n": n, "z": z, "i": i}))
    return z, trace


def reverse_check(trace):
    """
    Обратное выполнение: идём снизу вверх и проверяем,
    что каждое предыдущее состояние выводится из текущего.
    """
    print("\n=== ОБРАТНОЕ ВЫПОЛНЕНИЕ (снизу вверх) ===")
    ok = True
    for idx in range(len(trace) - 1, 0, -1):
        op_curr, st_curr = trace[idx]
        op_prev, st_prev = trace[idx - 1]
        print(f"\nШаг {idx}: {op_curr}  ->  {st_curr}")
        print(f"  Проверяем предыдущее: {op_prev} -> {st_prev}")

        # Простейшая проверка: значения x и n не меняются
        if st_curr["x"] != st_prev["x"] or st_curr["n"] != st_prev["n"]:
            print("  ОШИБКА: x или n изменились!")
            ok = False

        # Проверка для z = z*x
        if op_curr == "z=z*x" and st_prev["x"] != 0:
            expected_prev_z = st_curr["z"] // st_prev["x"]
            if expected_prev_z != st_prev["z"]:
                print(f"  ОШИБКА: ожидалось z={expected_prev_z}, получено z={st_prev['z']}")
                ok = False
            else:
                print(f"  OK: обратный ход z = {st_curr['z']}/{st_prev['x']} = {expected_prev_z}")

        # Проверка для i = i+1
        if op_curr == "i=i+1":
            if st_prev["i"] + 1 != st_curr["i"]:
                print(f"  ОШИБКА: i должно быть {st_curr['i']-1}, а равно {st_prev['i']}")
                ok = False
            else:
                print(f"  OK: обратный ход i = {st_curr['i']} - 1 = {st_prev['i']}")

    print("\n=== РЕЗУЛЬТАТ ОБРАТНОЙ ПРОВЕРКИ ===")
    print("Все шаги согласованы" if ok else "Обнаружены ошибки!")
    return ok


# ---------- ТЕСТОВЫЕ СЛУЧАИ (по методичке) ----------
def run_tests():
    test_cases = [
        # (x, n, ожидаемый результат, описание)
        (2, 3, 8,    "Обычный случай: 2^3 = 8"),
        (2, 1, 2,    "Минимальная степень: 2^1 = 2"),
        (5, 4, 625,  "5^4 = 625"),
        (1, 100, 1,  "1^100 = 1"),
        (0, 5, 0,    "0^5 = 0"),
        (10, 2, 100, "10^2 = 100"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ФУНКЦИИ power(x, n)")
    print("=" * 60)

    all_passed = True
    for x, n, expected, desc in test_cases:
        result = power(x, n)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"[{status}] {desc}: power({x},{n}) = {result}, ожидалось {expected}")

    print("\n" + "=" * 60)
    print("ОБРАТНОЕ ТЕСТИРОВАНИЕ (на примере x=2, n=3)")
    print("=" * 60)

    result, trace = power_traced(2, 3)
    reverse_check(trace)

    return all_passed


if __name__ == "__main__":
    run_tests()
