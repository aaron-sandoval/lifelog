import re
from pathlib import Path

def correct_yaml_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    corrected_lines = []
    for line in lines:
        # Correction 1: Wrap lines containing "\x" in double quotes
        if r'\x' in line and '"' not in line:
            # Preserve leading whitespace
            leading_whitespace = re.match(r'^(\s*)', line).group(1)
            # Remove leading/trailing whitespace and the trailing colon (if present)
            stripped = line.strip().rstrip(':')
            # Wrap in double quotes and add back the colon if it was present
            line = f'{leading_whitespace}"{stripped}"{":" if line.strip().endswith(":") else ""}\n'

        # Correction 2: Remove $ symbols not in comments or followed by "SUBJECTMATTER"
        # First, handle comments
        parts = line.split('#', 1)
        main_part = parts[0]
        comment = f'#{parts[1]}' if len(parts) > 1 else ''

        # Remove $ symbols in the main part of the line
        main_part = re.sub(r'\$(?!SUBJECTMATTER)', '', main_part)

        # Reconstruct the line
        line = f'{main_part}{comment}'

        corrected_lines.append(line)

    # Write corrected lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(corrected_lines)


if __name__ == "__main__":
    file = Path('catalogs')/'Catalog_SubjectMatter.yaml'
    correct_yaml_file(file)
