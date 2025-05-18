import openai
import base64
import json
import os
from dotenv import load_dotenv

# Załaduj zmienne z pliku .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def load_apartment_metadata(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def load_images_from_disc(image_paths):
    images_b64 = []
    for path in image_paths:
        image_base64 = encode_image_to_base64(path)
        images_b64.append(image_base64)

    return images_b64


def analyze_apartment_photos(images, metadata=None):
    image_contents = []
    for img in images:
        image_contents.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
            }
        )

    metadata_description = ""
    if metadata:
        metadata_description = (
            "\nOto dane ogłoszenia, które możesz uwzględnić w opisie mieszkania:\n"
            f"{json.dumps(metadata, ensure_ascii=False, indent=2)}"
        )

    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś ekspertem od sprzedaży nieruchomości. "
                "Analizujesz zdjęcia mieszkań pod kątem atrakcyjności wizualnej, stylu i ogólnego wrażenia. "
                "Zwracasz uwagę na wystrój, światło, porządek i kolorystykę. Oceniasz je z perspektywy potencjalnego kupującego. "
                "**Odpowiedź zwróć w formacie JSON bez dodatkowego formatowania**. "
                "W przypadku braku danych, zwróć pustą listę lub null w odpowiednich polach, zachowując pełną strukturę JSON."
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Na podstawie **wszystkich załączonych zdjęć** oraz poniższych danych o mieszkaniu:\n"
                        f"{metadata_description}\n\n"
                        "Zwróć odpowiedź w formacie JSON (po polsku), zawierającym:\n"
                        "- pros: lista mocnych stron wnętrza,\n"
                        "- to_fix: lista **niewiążących sugestii** poprawy estetyki i atrakcyjności wnętrza zgodnie z zasadami home stagingu – mających na celu **zwiększenie wizualnej wartości mieszkania**. To mogą być np. pomalowanie ścian na biało lub beżowo, wymiana kolorowych dodatków na neutralne, reorganizacja przestrzeni, usunięcie zbędnych mebli, poprawa oświetlenia, dodanie minimalistycznych dekoracji. Uwzględnij aktualne trendy: **minimalizm, neutralne kolory, uporządkowanie przestrzeni**,\n"
                        "- luxury_level: liczba całkowita od 1 do 10, gdzie 1 oznacza bardzo podstawowe mieszkanie, a 10 luksusowe,\n"
                        "- description: atrakcyjny, naturalnie brzmiący opis mieszkania do ogłoszenia — połącz dane ze zdjęć i z metadanych (np. lokalizacja, powierzchnia, piętro, liczba pokoi, balkon, garaż, dostępność itd.). Używaj języka obrazowego, ale unikaj przesady.\n\n"
                        "Poniższy przykład służy jedynie jako kontekst, **nie kopiuj go dosłownie**:\n"
                        "{\n"
                        '  "pros": [\n'
                        '    "nowoczesny wystrój",\n'
                        '    "dużo naturalnego światła",\n'
                        '    "przestronny balkon"\n'
                        "  ],\n"
                        '  "to_fix": [\n'
                        '    "można rozważyć pomalowanie ścian na biało, aby rozjaśnić wnętrze i nadać mu bardziej nowoczesny charakter",\n'
                        '    "usunąć rzeczy osobiste z sypialni i kuchni, aby wnętrza były bardziej neutralne i uniwersalne",\n'
                        '    "dodać minimalistyczne dekoracje, np. rośliny doniczkowe lub jasne poduszki na sofie",\n'
                        '    "uporządkować balkon i ewentualnie wstawić prosty zestaw mebli ogrodowych w stonowanej kolorystyce"\n'
                        '    "w salonie można zastąpić ciężkie zasłony lekkimi, jasnymi firanami, a także rozważyć ustawienie mebli w sposób optycznie powiększający przestrzeń",\n'
                        '    "w przedpokoju warto zadbać o dobre oświetlenie i usunąć nadmiar kurtek, butów lub drobnych przedmiotów, aby stworzyć czyste pierwsze wrażenie"\n'
                        "  ],\n"
                        '  "luxury_level": 7,\n'
                        '  "description": "Przestronne mieszkanie z dużym balkonem, idealne dla rodziny lub pary. Nowoczesny wystrój i dużo naturalnego światła sprawiają, że wnętrza są przytulne i komfortowe. Mieszkanie znajduje się w spokojnej okolicy Podgórza, w budynku z windą i garażem. Warto jednak rozważyć drobne zabiegi odświeżające, takie jak rozjaśnienie kolorystyki i uporządkowanie przestrzeni, co dodatkowo podniesie jego atrakcyjność."\n'
                        "}"
                    ),
                },
                *image_contents,
            ],
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-4o", messages=messages, max_tokens=3000
    )

    json_txt = response.choices[0].message.content
    if json_txt.startswith("```json"):
        json_txt = json_txt[7:-3]
    return json.loads(json_txt)



if __name__ == "__main__":
    image_files = [
        os.path.join("..", "..", "photos", "1.jpg"),
        os.path.join("..", "..", "photos", "2.jpg"),
        os.path.join("..", "..", "photos", "3.jpg"),
        os.path.join("..", "..", "photos", "4.jpg"),
        os.path.join("..", "..", "photos", "5.jpg"),
        os.path.join("..", "..", "photos", "6.jpg"),
    ]
    metadata_path = os.path.join("..", "..", "user_input", "json.txt")

    images_b64 = load_images_from_disc(image_files)
    metadata = load_apartment_metadata(metadata_path)
    result = analyze_apartment_photos(images_b64, metadata=metadata)
    print(result)

#<3