from pathlib import Path


def find_files_on_path_with_patterns(d: str, patterns: list) -> list:
    return [str(p.resolve()) for p in Path(d).glob("**/*") if p.suffix in patterns]

