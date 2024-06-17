#!/usr/bin/env python

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class CommentPattern:
    base_re = r"{0}\s*{1}(\w+)\s*{2}(.*?){0}\s*end\s*{2}"
    open: str
    close: str

    def start(self, ident):
        return f"{self.open} #{ident} {self.close}"

    def end(self):
        return f"{self.open} end {self.close}"

    def re(self, tag):
        return self.base_re.format(re.escape(self.open), tag, re.escape(self.close))


comment_patterns = {
    "html": CommentPattern("<!--", "-->"),
    "css": CommentPattern("/*", "*/"),
}

captures = {}


def process(directory, recursive=False):
    base = Path(directory).rglob("*") if recursive else Path(directory).glob("*")
    files = [f for f in base if f.is_file() and f.suffix.endswith((".html", ".css"))]

    for file in files:
        extract_blocks(Path(file).read_text(), comment_patterns[file.suffix[1:]])

    for file in files:
        contents = Path(file).read_text()
        try:
            updated = replace_sub_range(contents, comment_patterns[file.suffix[1:]])
            if contents != updated:
                Path(file).write_text(updated)
        except KeyError as e:
            print(f"Error processing: {file}. Unknown identifier: {e}")
            return


def extract_blocks(s: str, pattern: CommentPattern):
    for match in re.finditer(pattern.re("@"), s, re.DOTALL):
        identifier, content = match.groups()

        if identifier in captures:
            raise ValueError(f"Duplicate identifier: {identifier}")

        captures[identifier] = content


def replace_sub_range(s, pattern: CommentPattern) -> str:
    # print(pattern)

    def sub_repl(match):
        ident = match.group(1)
        return pattern.start(ident) + captures[ident] + pattern.end()

    return re.sub(pattern.re("#"), sub_repl, s, flags=re.DOTALL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir",
        help="directory to read files from (default: '.')",
        type=str,
        default=".",
        nargs="?",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        help="process directories recursively",
        action="store_true",
    )
    args = parser.parse_args()

    process(args.dir, recursive=args.recursive)
