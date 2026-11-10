import json
from wer import calculate_wer_metrics

def main():
    # Читання файлів
    try:
        with open("ref.txt", "r", encoding="utf-8") as f_ref:
            reference = f_ref.read()
        
        with open("hyp.txt", "r", encoding="utf-8") as f_hyp:
            hypothesis = f_hyp.read()
    except FileNotFoundError as e:
        print(f"Помилка: Не знайдено файл - {e.filename}")
        return

    # Обчислення метрик
    print("Обчислення метрик WER...")
    metrics = calculate_wer_metrics(reference, hypothesis)
    
    print("\nРезультати:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Збереження у JSON
    output_file = "wer_metrics.json"
    with open(output_file, "w", encoding="utf-8") as f_json:
        json.dump(metrics, f_json, indent=4, ensure_ascii=False)
    
    print(f"\nМетрики успішно збережено у файл: {output_file}")

if __name__ == "__main__":
    main()