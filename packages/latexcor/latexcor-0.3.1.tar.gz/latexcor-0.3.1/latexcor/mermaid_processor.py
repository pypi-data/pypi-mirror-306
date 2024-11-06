import re
import subprocess
from pathlib import Path
import hashlib
import os


class MermaidProcessor:
    @staticmethod
    def mermaid_to_image(mermaid_code: str, output_file: str) -> None:
        try:
            subprocess.run(
                ["mmdc", "-i", "-", "-o", output_file],
                input=mermaid_code,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error converting Mermaid to image: {str(e)}")

    @classmethod
    def process_mermaid(cls, file_path: Path) -> None:
        try:
            Path("mermaid").mkdir(exist_ok=True)
            content = file_path.read_text(encoding="utf-8")
            hash_text = hashlib.md5(content.encode()).hexdigest()
            hash_file_path = Path(f"mermaid/{hash_text}.mermaid")
            if hash_file_path.exists():
                return
            hash_file_path.write_text("processed", encoding="utf-8")

            def replace_mermaid(match):
                mermaid_block = match.group(0)
                mermaid_code = match.group(1).replace("%", "")
                old_hash = match.group(2) if match.group(2) else None
                new_hash = hashlib.md5(mermaid_code.encode()).hexdigest()

                old_image_file = f"mermaid_diagram_{old_hash}.png" if old_hash else None
                new_image_file = f"mermaid_diagram_{new_hash}.png"

                # Supprimer l'ancienne image si elle existe et est différente de la nouvelle
                if old_image_file and old_image_file != new_image_file:
                    old_image_path = Path(old_image_file)
                    if old_image_path.exists():
                        old_image_path.unlink()

                if not Path(new_image_file).exists():
                    cls.mermaid_to_image(mermaid_code, new_image_file)

                include = (
                    f"\n\\includegraphics{{{new_image_file}}}"
                    if Path(new_image_file).exists()
                    else ""
                )
                commented_block = "\n".join(
                    f"%{line}" for line in mermaid_block.split("\n")
                )
                return f"{commented_block}{include}\n%MERMAID_HASH:{new_hash}"

            pattern = r"(?<!%)\\begin\{mermaid\}(.*?)\\end\{mermaid\}(?:\n%MERMAID_HASH:([a-f0-9]+))?"
            new_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

            file_path.write_text(new_content, encoding="utf-8")
            print(f"Processed Mermaid diagrams in {file_path}")
        except Exception as e:
            print(f"Error processing Mermaid diagrams in {file_path}: {str(e)}")

    @classmethod
    def process_all_mermaid(cls, path_to_watch: Path) -> None:
        for file in path_to_watch.rglob("*.tex"):
            cls.process_mermaid(file)
