import re
from pathlib import Path
import argparse

def clean_text(text):
    # remove standalone filler words ("um", "uh")
    text, filler_replacements = re.subn(r'(?i)(?<!\w)(um|uh)(?!\w)', ' ', text)

    # capitalize standalone "i" and "i'" contractions like "i'm"
    text, i_capitalizations = re.subn(r"\bi(?=\b|')", "I", text)

    # normalize spaces
    text = re.sub(r'\s{2,}', ' ', text).strip()
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)

    return text, filler_replacements, i_capitalizations


def process_vtt(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = []
    stats = {
        "removed_um": 0,
        "removed_uh": 0,
        "capitalized_i": 0,
    }
    i = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")

        # Always preserve header
        if line.startswith("WEBVTT"):
            output.append(line)
            i += 1
            continue

        # Timing line → copy exactly
        if "-->" in line:
            output.append(line)
            
            # next line(s) = caption text
            i += 1
            text_block = []

            while i < len(lines) and lines[i].strip() != "":
                text_block.append(lines[i].strip())
                i += 1

            # process each caption line directly (no line reflow)
            if text_block:
                for caption_line in text_block:
                    # Track per-word removals before substitution for accurate counts.
                    stats["removed_um"] += len(
                        re.findall(r'(?i)(?<!\w)um(?!\w)', caption_line)
                    )
                    stats["removed_uh"] += len(
                        re.findall(r'(?i)(?<!\w)uh(?!\w)', caption_line)
                    )
                    cleaned, _, i_count = clean_text(caption_line)
                    stats["capitalized_i"] += i_count
                    output.append(cleaned)

            output.append("")  # preserve cue spacing
            i += 1
            continue

        # fallback (blank lines etc.)
        output.append(line)
        i += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    return stats


def parse_args():
    parser = argparse.ArgumentParser(description="Clean caption text from a .vtt file.")
    parser.add_argument("input_vtt", help="Path to the input .vtt file")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Optional output .vtt path (defaults to in-place overwrite of input)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input_vtt)
    output_path = Path(args.output) if args.output else input_path

    if input_path.suffix.lower() != ".vtt":
        raise ValueError("Input file must have a .vtt extension.")
    if output_path.suffix.lower() != ".vtt":
        raise ValueError("Output file must have a .vtt extension.")

    stats = process_vtt(str(input_path), str(output_path))
    print(
        "Changes made: "
        f"removed_um={stats['removed_um']}, "
        f"removed_uh={stats['removed_uh']}, "
        f"capitalized_i={stats['capitalized_i']}"
    )


if __name__ == "__main__":
    main()