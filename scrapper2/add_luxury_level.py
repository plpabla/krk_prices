import pandas as pd
import asyncio
import aiofiles.os
import os

from GPT_lux_lvl import load_images_from_disk, analyze_apartment_photos


async def get_luxury_level(files: list[str], photos_path: str = "./") -> int:
    files = [os.path.join(photos_path, f) for f in files]
    images = load_images_from_disk(files)
    res = analyze_apartment_photos(images)
    return res.get("luxury_level", -1) or -1


async def _process_row(df, index, photos_dir: str = "otodom_photos/"):
    row = df.iloc[index]
    slug, state, market = row[["slug", "state", "market"]].values

    # skip new buildings
    if state == "to_completion" and market == "primary":
        df.at[index, "luxury_level"] = -1
        return

    photo_path = os.path.join(photos_dir, slug)

    files = await aiofiles.os.listdir(photo_path)
    if not files:
        print(f"No files found in {photo_path}")
        df.at[index, "luxury_level"] = -1
        return

    print(f"[{index}] Processing {len(files)} files in {photo_path}")

    try:
        luxury_level = await get_luxury_level(files, photo_path)
    except Exception as e:
        print(f"[{index}] Error processing files: {e}")
        luxury_level = -1

    df.at[index, "luxury_level"] = luxury_level
    print(f"[{index}] Luxury level: {luxury_level}")


def _add_suffix(filename: str, suffix: str) -> str:
    base, ext = os.path.splitext(filename)
    return f"{base}{suffix}{ext}"


async def add_luxury_level(
    filename: str, photos_dir: str = "otodom_photos/", suffix: str = "_luxury_level"
):
    df = pd.read_csv(filename)
    df.drop(columns=["photos"], inplace=True)

    tasks = []
    for index in range(len(df)):
        tasks.append(_process_row(df, index, photos_dir))
    await asyncio.gather(*tasks)

    df.to_csv(_add_suffix(filename, suffix), index=False)
