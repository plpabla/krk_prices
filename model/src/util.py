import os


def get_filename_and_extension(filename: str) -> tuple[str, str]:
    base_name, extension = os.path.splitext(filename)
    return base_name, extension
