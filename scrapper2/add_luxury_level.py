import pandas as pd
import asyncio
import aiofiles.os
import os


async def get_luxury_level(files: list[str]) -> int:
    await asyncio.sleep(0)  # Simulate async operation
    return 5


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

    print(f"Processing {len(files)} files in {photo_path}")

    luxury_level = await get_luxury_level(files)
    df.at[index, "luxury_level"] = luxury_level


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
