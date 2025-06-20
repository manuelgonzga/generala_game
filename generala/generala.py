import random
import threading
from collections import Counter
import time

CATEGORIES = [
    "1", "2", "3", "4", "5", "6",
    "Escalera", "Full", "Poker", "Generala", "Doble Generala"
]

def roll_dice(n=5):
    return [random.randint(1, 6) for _ in range(n)]

def score_category(dice, category, used_categories, generala_count=0):
    counts = Counter(dice)
    if category in "123456":
        num = int(category)
        return sum(d for d in dice if d == num)
    elif category == "Escalera":
        if sorted(dice) in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
            return 20
        return 0
    elif category == "Full":
        if 2 in counts.values() and 3 in counts.values():
            return 30
        return 0
    elif category == "Poker":
        if 4 in counts.values() or 5 in counts.values():
            return 40
        return 0
    elif category == "Generala":
        if 5 in counts.values():
            return 50
        return 0
    elif category == "Doble Generala":
        if 5 in counts.values() and "Generala" in used_categories:
            return 100
        return 0
    return 0

def intelligent_strategy():
    score_card = {}
    generala_count = 0

    for _ in range(len(CATEGORIES)):
        dice = roll_dice()
        rolls_left = 2
        keep = []

        while rolls_left > 0:
            counts = Counter(dice)
            unique_counts = list(counts.values())
            sorted_dice = sorted(set(dice))
            most_common_num, _ = counts.most_common(1)[0]

            def expected_generala(count):
                probs = {2: 0.03, 3: 0.15, 4: 0.42}
                return 50 * probs.get(count, 0)

            def expected_poker(count):
                probs = {3: 0.3, 4: 0.5}
                return 40 * probs.get(count, 0)

            def expected_full():
                return 30 * 0.6 if 3 in unique_counts else 0

            def expected_escalera():
                if sorted_dice in ([1,2,3,4], [2,3,4,5]):
                    return 20 * 0.5
                elif sorted_dice in ([1,2,3,4,5], [2,3,4,5,6]):
                    return 20
                return 0

            def expected_high_number():
                return most_common_num * counts[most_common_num]

            paths = {
                "Generala": expected_generala(counts[most_common_num]),
                "Poker": expected_poker(counts[most_common_num]),
                "Full": expected_full(),
                "Escalera": expected_escalera(),
                "Número Alto": expected_high_number()
            }

            best_path = max(paths.items(), key=lambda x: x[1])[0]

            if best_path in ["Generala", "Poker", "Número Alto"]:
                keep = [d for d in dice if d == most_common_num]
            elif best_path == "Full":
                triple = [num for num, cnt in counts.items() if cnt == 3]
                pair = [num for num, cnt in counts.items() if cnt == 2]
                keep = [d for d in dice if d in triple or d in pair]
            elif best_path == "Escalera":
                keep = [d for d in dice if d in [1,2,3,4,5,6]]

            dice = keep + roll_dice(5 - len(keep))
            rolls_left -= 1

        available = [c for c in CATEGORIES if c not in score_card]
        best_cat = max(available, key=lambda c: score_category(dice, c, score_card, generala_count))
        score = score_category(dice, best_cat, score_card, generala_count)
        score_card[best_cat] = score
        if best_cat == "Generala" and score > 0:
            generala_count += 1

    return sum(score_card.values())

def greedy_strategy():
    score_card = {}
    generala_count = 0

    for _ in range(len(CATEGORIES)):
        dice = roll_dice()
        keep = []
        rolls_left = 2

        while rolls_left > 0:
            counts = Counter(dice)
            most_common = counts.most_common(1)[0][0]
            keep = [d for d in dice if d == most_common]
            dice = keep + roll_dice(5 - len(keep))
            rolls_left -= 1

        available = [c for c in CATEGORIES if c not in score_card]
        best_cat = max(available, key=lambda c: score_category(dice, c, score_card, generala_count))
        score = score_category(dice, best_cat, score_card, generala_count)
        score_card[best_cat] = score
        if best_cat == "Generala" and score > 0:
            generala_count += 1

    return sum(score_card.values())

def random_strategy():
    score_card = {}
    generala_count = 0

    for _ in range(len(CATEGORIES)):
        dice = roll_dice()
        rolls_left = 2

        while rolls_left > 0:
            keep_indices = random.sample(range(5), random.randint(0, 5))
            keep = [dice[i] for i in keep_indices]
            dice = keep + roll_dice(5 - len(keep))
            rolls_left -= 1

        available = [c for c in CATEGORIES if c not in score_card]
        cat = random.choice(available)
        score = score_category(dice, cat, score_card, generala_count)
        score_card[cat] = score
        if cat == "Generala" and score > 0:
            generala_count += 1

    return sum(score_card.values())

def highest_immediate_score_strategy():
    score_card = {}
    generala_count = 0

    for _ in range(len(CATEGORIES)):
        dice = roll_dice()
        rolls_left = 2

        while rolls_left > 0:
            best_combination = max(
                (Counter(dice).most_common(i)[0][0] for i in range(1, 6)),
                key=lambda num: dice.count(num)
            )
            keep = [d for d in dice if d == best_combination]
            dice = keep + roll_dice(5 - len(keep))
            rolls_left -= 1

        available = [c for c in CATEGORIES if c not in score_card]
        best_cat = max(available, key=lambda c: score_category(dice, c, score_card, generala_count))
        score = score_category(dice, best_cat, score_card, generala_count)
        score_card[best_cat] = score
        if best_cat == "Generala" and score > 0:
            generala_count += 1

    return sum(score_card.values())

def simular_estrategia(nombre, funcion_estrategia, n, resumen):
    print(f"[{nombre}] Comenzando simulación en hilo...")
    start_time = time.time()
    resultados = [funcion_estrategia() for _ in range(n)]
    duration = time.time() - start_time
    resumen[nombre] = {
        "Promedio": sum(resultados) / n,
        "Máximo": max(resultados),
        "Mínimo": min(resultados),
        "Duración": duration
    }

    print(f"[{nombre}] Terminó en {duration:.2f} segundos.")

def simular_estrategias_concurrente(n=5000):
    resumen = {}
    threads = []

    estrategias = {
        "Aleatoria": random_strategy,
        "Codiciosa": greedy_strategy,
        "Puntaje inmediato": highest_immediate_score_strategy,
        "Inteligente": intelligent_strategy
    }

    for nombre, funcion in estrategias.items():
        hilo = threading.Thread(target=simular_estrategia, args=(nombre, funcion, n, resumen))
        hilo.start()
        threads.append(hilo)

    for hilo in threads:
        hilo.join()

    return resumen

if __name__ == "__main__":
    resultados = simular_estrategias_concurrente(1000)
    for estrategia, stats in resultados.items():
        print(f"Estrategia: {estrategia}")
        print(f"  Promedio: {stats['Promedio']:.2f}")
        print(f"  Máximo: {stats['Máximo']}")
        print(f"  Mínimo: {stats['Mínimo']}")
        print()
