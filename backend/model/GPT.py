import openai
import base64
import json
import os
from dotenv import load_dotenv

# Załaduj zmienne z pliku .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def load_images_from_disc(image_paths):
    images_b64 = []
    for path in image_paths:
        image_base64 = encode_image_to_base64(path)
        images_b64.append(image_base64)

    return images_b64


def analyze_apartment_photos(images):
    image_contents = []
    for img in images:
        image_contents.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
            }
        )

    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś ekspertem od sprzedaży nieruchomości. "
                "Analizujesz zdjęcia mieszkań pod kątem atrakcyjności wizualnej, stylu i ogólnego wrażenia. "
                "Zwróć uwagę na wystrój, światło, porządek, kolorystykę. Oceniaj jak potencjalny kupujący."
                "**Odpowiedź zwróć w formacie JSON bez dodatkowego formatowania**. W przypadku braku danych zwróć pustą listę lub null w poszczególnych polach zachowując przedstawiony format. "
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Na podstawie **wszystkich załączonych zdjęć** mieszkania:\n\n"
                        "1. Odpowiedz w formacie JSON (po polsku), zawierającym:\n"
                        "- type: ogólny typ mieszkania (np. kawalerka, 2-pokojowe itp.). unknown, jeżeli nie możesz tego określić\n"
                        "- pros: lista mocnych stron wnętrza,\n"
                        "- to_fix: lista rzeczy do poprawy,\n"
                        "- luxury_level: liczba od 1 do 10 (całościowa),\n\n"
                        "- description: estetyczny opis mieszkania (lub pomieszczenia w przypadku zbyt małej ilości zdjęć) jak do ogłoszenia sprzedaży — używaj języka obrazowego, ale bez przesady. Pisz naturalnie i zachęcająco.\n\n"
                        " Przykład odpowiedzi:\n"
                        "{\n"
                        '  "type": "kawalerka",\n'
                        '  "pros": [\n'
                        '    "nowoczesny wystrój",\n'
                        '    "dużo naturalnego światła",\n'
                        '    "przestronny balkon"\n'
                        "  ],\n"
                        '  "to_fix": [\n'
                        '    "brak porządku",\n'
                        '    "stare meble",\n'
                        '    "nieodpowiednie oświetlenie"\n'
                        "  ],\n"
                        '  "luxury_level": 7,\n'
                        '  "description": "Przestronna kawalerka z dużym balkonem, idealna dla singla lub pary. Nowoczesny wystrój i dużo naturalnego światła sprawiają, że mieszkanie jest przytulne i komfortowe. Warto jednak zwrócić uwagę na porządek oraz nieco przestarzałe meble, które można by wymienić na nowsze."\n'
                        "}\n\n"
                    ),
                },
                *image_contents,  # dodajemy obrazy jako kolejne elementy
            ],
        },
    ]

    # Wysyłamy zapytanie
    response = openai.chat.completions.create(
        model="gpt-4o", messages=messages, max_tokens=2000
    )

    json_txt = response.choices[0].message.content
    # jeżeli odpowiedź zaczyna się od ```json, to usuwamy ten prefix
    if json_txt.startswith("```json"):
        json_txt = json_txt[7:-3]
    return json.loads(json_txt)


if __name__ == "__main__":
    # ✅ Przykład użycia z 3 zdjęciami:
    image_files = [
        os.path.join("..", "..", "photos", "kuchnia.jpg"),
        os.path.join("..", "..", "photos", "lazienka.jpg"),
        os.path.join("..", "..", "photos", "sypialnia.jpg"),
        os.path.join("..", "..", "photos", "balkon.jpg"),
    ]

    files = load_images_from_disc(image_files)
    result = analyze_apartment_photos(files)
    print(result)
