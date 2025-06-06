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
    return [encode_image_to_base64(path) for path in image_paths]


def analyze_apartment_photos(images_b64, metadata=None):
    images_attached = len(images_b64) > 0
    image_contents = []
    prompt_system = ""

    prompt_json_structure = (
        "{\n"
        '  "attractiveness_level": <integer>,\n'
        '  "attractiveness_reason": "<string>",\n'
        '  "pros": [<string>],\n'
        '  "to_fix": [<string>],\n'
        '  "description": "<string>"\n'
        "}"
    )
    prompt_json_details = ""

    metadata_description = ""
    if metadata:
        metadata_description = (
            "\nOto dane ogłoszenia, które możesz uwzględnić w opisie mieszkania:\n"
            f"{json.dumps(metadata, ensure_ascii=False, indent=2)}"
        )

    if images_attached:
        image_contents = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
            }
            for img_b64 in images_b64
        ]

        prompt_system = (
            "Jesteś ekspertem od nieruchomości.\n"
            "Na podstawie zdjęć oceń atrakcyjność mieszkania z punktu widzenia sprzedaży, "
            "w skali od 1 do 10, gdzie 1 to bardzo mało atrakcyjne, a 10 to wyjątkowo atrakcyjne wnętrze gotowe do sprzedaży.\n"
            "Bierz pod uwagę aktualne trendy: mieszkania najlepiej sprzedają się, gdy są czyste, jasne, odświeżone, urządzone minimalistycznie i schludnie.\n"
            "Uwaga: pola `attractiveness_level`, `attractiveness_reason`, `pros`, `to_fix` generuj wyłącznie na podstawie zdjęć — ignoruj metadane.\n"
            "W przypadku braku wystarczających informacji na zdjęciach, zwróć taką samą strukturę JSON, ale z pustymi polami (np. pustą tablicą).\n\n"
            "Pole `description` generuj na podstawie zarówno zdjęć, jak i danych z ogłoszenia (metadanych).\n"
            "Wynik zwróć jako surowy JSON bez formatowania tekstowego.\n"
        )

        prompt_json_details = (
            "Struktura JSON powinna wyglądać następująco:\n"
            f"{prompt_json_structure}\n\n"
            "Na podstawie **wyłącznie kolażu zdjęć** mieszkania (ignoruj dane tekstowe i metadane) wygeneruj:\n"
            "- `attractiveness_level`: liczba całkowita od 1 do 10 (gdzie 1 to bardzo nieatrakcyjne wnętrze, a 10 to idealnie przygotowane do sprzedaży),\n"
            "- `attractiveness_reason`: krótkie uzasadnienie oceny atrakcyjności (na podstawie zdjęć),\n"
            "**W tej części odpowiedzi zastosuj ten sam styl, co w poniższym przykładzie —\n"
            "uzasadnienie powinno być konkretne, wyważone, napisane z taktem i empatią, tak aby nie urazić odbiorcy — "
            "powinno zawierać przynajmniej 2–3 zdania, które konstruktywnie opisują cechy mieszkania, "
            "{\n"
            '  "attractiveness_level": 7,\n'
            '  "attractiveness_reason": "Wnętrze mieszkania jest jasne, estetycznie urządzone i dobrze przygotowane do sprzedaży. Dominuje neutralna kolorystyka i minimalistyczny styl, co trafia w gusta szerokiego grona kupujących. Brakuje jedynie drobnych akcentów, które mogłyby dodać ciepła i indywidualnego charakteru." '
            "}\n\n"
            "- `pros`: lista mocnych stron widocznych na zdjęciach,\n"
            "- `to_fix`: lista sugestii poprawy estetyki wnętrza (wg zasad home stagingu oraz aktualnych trendów).\n\n"
            "**Następnie**, tylko pole `description` wygeneruj na podstawie **zarówno zdjęć, jak i poniższych danych o mieszkaniu**:\n"
            f"{metadata_description}\n\n"
            "Wygeneruj:\n"
            "- `description`: atrakcyjny, naturalnie brzmiący opis mieszkania do ogłoszenia.\n\n"
            "**Zwróć wynik w formacie JSON, z polami dokładnie w tej kolejności:**\n"
            "`attractiveness_level`, `attractiveness_reason`, `pros`, `to_fix`, `description`.\n\n"
            "Nie dodawaj komentarzy, tekstów wstępnych ani formatowania Markdown — tylko surowy JSON."
        )
    else:
        prompt_system = (
            "Jesteś ekspertem od nieruchomości.\n"
            "Na podstawie danych o mieszkaniu wygeneruj opis ogłoszenia.\n"
            "Wynik zwróć jako surowy JSON bez formatowania tekstowego."
        )

        prompt_json_details = (
            "Struktura JSON powinna wyglądać następująco:\n"
            f"{prompt_json_structure}\n\n"
            "attractiveness_level, attractiveness_reason, pros i to_fix wygeneruj dokładnie jak w przykładzie poniżej. Tylko pole description będzie zależeć od opisu:\n"
            "{\n"
            '  "attractiveness_level": 0,\n'
            '  "attractiveness_reason": "",\n'
            '  "pros": [],\n'
            '  "to_fix": [],\n'
            '  "description": "string" wygeneruj na podstawie poniższych danych o mieszkaniu:\n'
            "}\n"
            f"{metadata_description}\n\n"
            "Wygeneruj:\n"
            "- `description`: atrakcyjny, naturalnie brzmiący opis mieszkania do ogłoszenia.\n\n"
            "**Zwróć wynik w formacie JSON, z polami dokładnie w tej kolejności:**\n"
            "Nie dodawaj komentarzy, tekstów wstępnych ani formatowania Markdown — tylko surowy JSON."
        )

    messages = [
        {
            "role": "system",
            "content": prompt_system,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_json_details,
                },
                *image_contents,
            ],
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=4000,
    )

    json_txt = response.choices[0].message.content.strip()
    if json_txt.startswith("```json"):
        json_txt = json_txt[7:-3].strip()

    return json.loads(json_txt)


if __name__ == "__main__":
    image_files = [
        os.path.join("..", "..", "photos", "1.jpg"),
    ]
    metadata_path = os.path.join("..", "..", "user_input", "json.txt")

    images_b64 = load_images_from_disc(image_files)
    metadata = load_apartment_metadata(metadata_path)

    result = analyze_apartment_photos(images_b64, metadata=metadata)
    print(json.dumps(result, ensure_ascii=False, indent=2))

# <3
