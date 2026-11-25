"""
# Entry validated: output is 1-140 chars, one line, deterministic.
Entrypoint that writes a specific verbatim string to entry.txt in the designated output directory.
"""

import os
import pathlib

LINE = "Your email has been successfully forwarded to my closed laptop, which is currently judging both of us from the kitchen table."


def main():
    # Prepare content with a single newline
    content = LINE + "\n"

    # Validate content length and structure
    if not (1 <= len(content) <= 140 and content.strip()):
        raise ValueError("Content validation failed")
    
    # Ensure exactly one line
    if content.count("\n") != 1 or content.endswith("\n\n"):
        raise ValueError("Content must contain exactly one line")

    # Determine output directories
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    primary_dir = pathlib.Path(output_dir_env)
    default_dir = pathlib.Path("/output")

    directories_to_write = [primary_dir]
    if primary_dir.resolve() != default_dir.resolve():
        directories_to_write.append(default_dir)

    primary_path = None
    for d in directories_to_write:
        try:
            d.mkdir(parents=True, exist_ok=True)
            file_path = d / "entry.txt"
            file_path.write_text(content, encoding="utf-8")
            if d == primary_dir:
                primary_path = file_path
        except Exception:
            if d == primary_dir:
                raise

    print(f"{primary_path}\n{len(content)}")


if __name__ == "__main__":
    main()
