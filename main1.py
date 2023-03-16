import openai
import csv

# Установите свой API-ключ напрямую
openai.api_key = "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"

# Функция для отправки запроса API OpenAI для получения оценки отзыва
def get_review_score(review_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"Rate the following review from 1 to 10, where 10 is the most positive and 1 is the most negative:\n\n{review_text}\n\nScore:"),
        temperature=0.7,
        max_tokens=1,
        n=1,
        stop=None,
        timeout=10.0,
    )
    score = int(response.choices[0].text.strip())
    return score

# Открытие файла и добавление столбца "rate" с рейтингами отзывов
with open('reviews.csv', 'r', newline='') as input_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames + ['rate']
    with open('reviews_with_rate.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            row['rate'] = get_review_score(row['review text'])
            writer.writerow(row)

# Сортировка созданной копии файла по убыванию рейтинга
with open('reviews_with_rate.csv', 'r', newline='') as input_file:
    reader = csv.DictReader(input_file)
    sorted_rows = sorted(reader, key=lambda row: int(row['rate']), reverse=True)
    fieldnames = reader.fieldnames
    with open('reviews_analyzed.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)