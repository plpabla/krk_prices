import openai
import base64
import os
from dotenv import load_dotenv

# Załaduj zmienne z pliku .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_apartment_photos(image_paths):
    # Zakoduj wszystkie obrazy
    image_contents = []
    for path in image_paths:
        image_base64 = encode_image_to_base64(path)
        image_contents.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            }
        )

    # Zbuduj zapytanie
    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś ekspertem od sprzedaży nieruchomości. "
                "Analizujesz zdjęcia mieszkań pod kątem atrakcyjności wizualnej, stylu i ogólnego wrażenia. "
                "Zwróć uwagę na wystrój, światło, porządek, kolorystykę. Oceniaj jak potencjalny kupujący."
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
                        "- typ_mieszkania: ogólny typ mieszkania (np. kawalerka, 2-pokojowe itp.),\n"
                        "- zalety: lista mocnych stron wnętrza,\n"
                        "- co_poprawić: lista rzeczy do poprawy,\n"
                        "- ocena_atrakcyjności: liczba od 1 do 10 (całościowa),\n\n"
                        "- opis: estetyczny opis mieszkania jak do ogłoszenia sprzedaży — używaj języka obrazowego, ale bez przesady. Pisz naturalnie i zachęcająco."
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

    return response.choices[0].message.content


if __name__ == "__main__":
    # ✅ Przykład użycia z 3 zdjęciami:
    image_files = [
        os.path.join("..", "..", "photos", "kuchnia.jpg"),
        os.path.join("..", "..", "photos", "lazienka.jpg"),
        os.path.join("..", "..", "photos", "sypialnia.jpg"),
        os.path.join("..", "..", "photos", "balkon.jpg"),
    ]

    result = analyze_apartment_photos(image_files)
    print(result)
