import re
import argparse
import textwrap
from pathlib import Path

import whisper


def _print(text):
    for line in textwrap.wrap(text):
        print(line)
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-by", required=False)
    parser.add_argument("path")
    args = parser.parse_args()
    model = whisper.load_model("small")

    path_txt = Path(f"{args.path}.txt")
    if not path_txt.exists():
        result = model.transcribe(args.path)
        path_txt.write_text(result["text"])

    text = path_txt.read_text()
    if args.split_by is None:
        print(text)
    else:
        matches = list(re.compile(args.split_by).finditer(text))

        for a, b in zip(matches[:-1], matches[1:], strict=False):
            _print(text[a.span()[0] : b.span()[0]])
        _print(text[matches[-1].span()[0] :])


if __name__ == "__main__":
    main()
