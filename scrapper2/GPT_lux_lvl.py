import openai
import base64
import os
import json
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def load_images_from_disk(image_paths):
    images_b64 = []
    for path in image_paths:
        image_base64 = encode_image_to_base64(path)
        images_b64.append(image_base64)
    return images_b64


def analyze_apartment_photos(images):
    image_contents = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img}"},
        }
        for img in images
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś ekspertem od nieruchomości. "
                "Na podstawie kolażu zdjęć różnych pomieszczeń w mieszkaniu oceń poziom luksusu mieszkania "
                "w skali od 1 do 10, gdzie 1 to bardzo podstawowe, a 10 to najwyższy luksus. "
                "Weź pod uwagę aktualne trendy rynkowe: mieszkania najlepiej sprzedają się, gdy są czyste, przestronne, "
                "odnowione oraz utrzymane w neutralnych kolorach. "
                "Zwróć odpowiedź w formacie JSON z dwoma polami: "
                '"explanation" - krótkie uzasadnienie oceny. '
                '"luxury_level" - liczba całkowita 1-10, '
                "Nie dodawaj nic poza tym JSONem."
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Na podstawie załączonych zdjęć zwróć poziom luksusu i uzasadnienie.",
                },
                *image_contents,
            ],
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-4o", messages=messages, max_tokens=300
    )

    json_txt = response.choices[0].message.content.strip()
    # Usuń ewentualne znaczniki kodu
    if json_txt.startswith("```json"):
        json_txt = json_txt[7:-3].strip()
    try:
        result = json.loads(json_txt)
    except json.JSONDecodeError:
        result = {"luxury_level": None, "explanation": "Błąd przetwarzania odpowiedzi."}

    return result


if __name__ == "__main__":
    image_files = [
        os.path.join("../backend", "..", "photos", "1.jpg"),
    ]

    images_b64 = load_images_from_disk(image_files)
    result = analyze_apartment_photos(images_b64)
    print("Luxury level:", result.get("luxury_level"))
    print("Explanation:", result.get("explanation"))
