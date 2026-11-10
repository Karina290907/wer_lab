import string

def normalize_text(text):
    """Очищує текст від пунктуації та зводить до нижнього регістру."""
    text = text.lower()
    # Видаляємо пунктуацію, але залишаємо апострофи всередині слів
    punctuation_to_remove = string.punctuation.replace("'", "") + "—«»"
    text = text.translate(str.maketrans('', '', punctuation_to_remove))
    return text

def calculate_wer_metrics(ref_text, hyp_text):
    """Обчислює метрики WER, S, D, I, N."""
    r = normalize_text(ref_text).split()
    h = normalize_text(hyp_text).split()

    # Створення матриці Левенштейна
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]

    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    # Зворотний прохід (backtracing) для точного підрахунку S, D, I
    i = len(r)
    j = len(h)
    S = 0
    D = 0
    I = 0

    while i > 0 or j > 0:
        if i > 0 and j > 0 and r[i-1] == h[j-1]:
            # Збіг слова
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and d[i][j] == d[i-1][j-1] + 1:
            # Заміна (Substitution)
            S += 1
            i -= 1
            j -= 1
        elif i > 0 and d[i][j] == d[i-1][j] + 1:
            # Видалення (Deletion)
            D += 1
            i -= 1
        elif j > 0 and d[i][j] == d[i][j-1] + 1:
            # Вставка (Insertion)
            I += 1
            j -= 1

    N = len(r)
    wer_score = (S + D + I) / N if N > 0 else 0.0

    return {
        "WER": round(wer_score, 4),
        "S": S,
        "D": D,
        "I": I,
        "N": N
    }