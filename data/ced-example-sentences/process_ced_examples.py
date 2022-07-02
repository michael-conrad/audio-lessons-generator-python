#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda deactivate
conda activate audio-lessons
exec python "$0" "$@"
exit $?
''"""
import pathlib

IX_VALID: int = 0
IX_PRONOUNCE: int = 6
IX_ENGLISH: int = 5


def main() -> None:
    work_dir = pathlib.Path(__file__).resolve().parent
    in_file: pathlib.Path = work_dir.joinpath("ced_example_sentences.txt")
    out_file: pathlib.Path = work_dir.joinpath("../ced-sentences.txt")

    with open(in_file, "r") as r:
        with open(out_file, "w") as w:
            w.write("ID|PSET|ALT_PRONOUNCE|PRONOUN|VERB|GENDER|SYLLABARY|PRONOUNCE|ENGLISH|INTRO NOTE|END NOTE")
            w.write("\n")
            for line in r:
                if not line.strip():
                    continue
                parts: list[str] = line.split("|")
                if len(parts) < IX_PRONOUNCE + 1:
                    print(f"- BAD LINE: {parts}")
                    continue

                is_valid: bool = parts[IX_VALID] == "*"
                pronunciations: list[str] = parts[IX_PRONOUNCE].split(";")
                english: str = parts[IX_ENGLISH]

                if not is_valid:
                    continue
                if not pronunciations:
                    continue
                alt_pronounce: str = ""
                pronounce: str = ""
                for item in pronunciations:
                    item = item.strip()
                    if not item:
                        continue
                    if not pronounce:
                        pronounce = item
                        continue
                    if alt_pronounce:
                        alt_pronounce += "; "
                    alt_pronounce += item
                gender: str = ""
                w.write(f"||{alt_pronounce}|||{gender}||{pronounce}|{english}||")
                w.write("\n")


if __name__ == '__main__':
    main()
