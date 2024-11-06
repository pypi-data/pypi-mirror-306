import logging
import os
import re
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Literal, Optional

from dockercor import get_image_info, run_docker_command
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

console = Console()
logger = logging.getLogger(__name__)

LatexEngine = Literal["xelatex", "pdflatex", "lualatex"]

def get_current_user_info():
    """Récupère l'UID et le GID de l'utilisateur courant."""
    import pwd
    uid = os.getuid()
    gid = os.getgid()
    user = pwd.getpwuid(uid).pw_name
    return uid, gid, user


@dataclass
class CompilationProgress:
    """Tracks LaTeX compilation progress."""

    total_steps: int = 2  # Two passes for packages like lastpage
    current_step: int = 0
    current_phase: str = ""
    errors: List[str] = None

    def __post_init__(self):
        self.errors = []

    def update(self, line: str) -> bool:
        """Updates progress based on LaTeX output."""
        if any(pattern in line for pattern in ["! ", "Error:", "Fatal error"]):
            self.errors.append(line)
            return True
        if "Output written on" in line or "Transcript written on" in line:
            self.current_step += 1
            return True
        return False


@dataclass
class TexFile:
    """Represents a LaTeX file with its metadata."""

    name: Path
    path: Path
    time_modification: float

    @property
    def is_main_file(self) -> bool:
        """Checks if this is a main LaTeX file."""
        try:
            content = self.name.read_text(encoding="utf-8")
            return all(
                tag in content
                for tag in ["\\documentclass", "\\begin{document}", "\\end{document}"]
            )
        except Exception:
            return False


class LatexCompiler:
    """LaTeX compiler manager with progress tracking."""

    # File extensions to clean up
    CLEAN_EXTENSIONS = {
        ".aux",
        ".log",
        ".out",
        ".toc",
        ".bbl",
        ".blg",
        ".fls",
        ".synctex.gz",
        ".nav",
        ".snm",
        ".vrb",
        ".bcf",
        ".run.xml",
        ".idx",
        ".ilg",
        ".ind",
        ".xdv",
        ".bar",
        ".bara",
        ".barb",
        ".tab",
        ".cor",
    }

    # Temporary folders to clean up
    CLEAN_PATHS = {"_minted-*", "_markdown_*", "_preview_*"}

    @staticmethod
    def parse_latex_output(output: str) -> Iterator[str]:
        """Parses LaTeX output line by line."""
        for line in output.splitlines():
            line = line.strip()
            if line:
                yield line

    @staticmethod
    def extract_error_context(log_file: Path) -> List[str]:
        """Extracts error context from the log file."""
        error_context = []
        if not log_file.exists():
            return error_context

        try:
            with log_file.open("r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                error_blocks = re.finditer(
                    r"!(.*?)\n(?:l\.\d+.*?)(?=\n\n|\Z)", content, re.DOTALL
                )
                for block in error_blocks:
                    error_context.append(block.group(0).strip())
        except Exception as e:
            logger.error(f"Error reading log file: {e}")

        return error_context

    @classmethod
    def clean_aux(cls, path: Path) -> None:
        """Cleans up LaTeX auxiliary files."""
        try:
            for item in path.rglob("*"):
                if item.is_file() and item.suffix in cls.CLEAN_EXTENSIONS:
                    try:
                        item.unlink()
                        logger.debug(f"Deleted: {item}")
                    except Exception as e:
                        logger.warning(f"Unable to delete {item}: {e}")

            # Clean temporary directories
            for clean_path in cls.CLEAN_PATHS:
                for item in path.glob(clean_path):
                    if item.is_dir():
                        try:
                            item.rmdir()
                            logger.debug(f"Directory deleted: {item}")
                        except Exception as e:
                            logger.warning(f"Unable to delete directory {item}: {e}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    @staticmethod
    def get_tex_files(path: Path) -> List[TexFile]:
        """Gets all LaTeX files in the given path."""
        try:
            return [
                TexFile(
                    name=file, path=file.parent, time_modification=file.stat().st_mtime
                )
                for file in path.rglob("*.tex")
                if file.is_file()
            ]
        except Exception as e:
            logger.error(f"Error searching for TeX files: {e}")
            return []

    @classmethod
    def compile_latex(
        cls,
        file: Path,
        latex_engine: str = "xelatex",
        progress: Optional[Progress] = None,
        task_id: Optional[TaskID] = None,
    ) -> bool:
        """Compiles a LaTeX file with progress bar."""
        # Conversion en Path si ce n'est pas déjà fait
        file = Path(file).resolve()
        log_file = file.with_suffix(".log")
        compilation_progress = CompilationProgress()

        if progress is None:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
            )

        # Sauvegarde et changement du répertoire de travail
        output_dir = file.parent
        current_dir = os.getcwd()
        os.chdir(str(output_dir))

        try:
            docker_ready = get_image_info("infocornouaille/tools:perso")
        except Exception:
            docker_ready = None

        try:
            if docker_ready:
                console.print("\n[bold green]Using docker infocornouaille/tools")
                # Utilisation de Path pour gérer correctement les chemins
                relative_file = file.name
                current_path = os.path.abspath(os.getcwd())
                
                # Adaptation du chemin pour Windows
                if os.name == 'nt':
                    current_path = current_path.replace('\\', '/')
                    if ':' in current_path:
                        drive, path = current_path.split(':', 1)
                        current_path = f"/{drive.lower()}{path}"
                    cmd = [
                        "docker",
                        "run",
                        "-i",
                        "--rm",
                        "-v",
                        f"{current_path}:/data",
                        "infocornouaille/tools:perso",
                        latex_engine,
                        "-interaction=nonstopmode",
                        "-shell-escape",
                        relative_file,
                    ]
                else:
                    # Sous Linux, on ajoute les permissions utilisateur
                    uid, gid, user = get_current_user_info()
                    cmd = [
                        "docker",
                        "run",
                        "-i",
                        "--rm",
                        #f"--user={uid}:{gid}",  # Exécuter en tant qu'utilisateur courant
                        "-v",
                        f"{current_path}:/data:Z",  # Ajouter explicitement les droits d'écriture
                        #"-w",  # Définir le répertoire de travail
                        #"/data:Z",
                        "infocornouaille/tools:perso",
                        latex_engine,
                        "-interaction=nonstopmode",
                        "-shell-escape",
                        relative_file,
                    ]
                    
                    # S'assurer que le répertoire courant a les bonnes permissions
                    os.chmod(current_path, 0o755)
            else:
                console.print("\n[bold green]Using system latex")
                cmd = [
                    latex_engine,
                    "-interaction=nonstopmode",
                    "-shell-escape",
                    str(file.name)
                ]

            #console.print(f"[dim]Debug: Executing command: {' '.join(cmd)}[/]")

            with progress:
                if task_id is None:
                    task_id = progress.add_task(f"Compiling {file.name}", total=100)

                # Run two passes
                for pass_num in range(1, 3):
                    progress.update(
                        task_id,
                        description=f"[bold blue]{file.name}[/] - Pass {pass_num}/2",
                        completed=(pass_num - 1) * 50,
                    )

                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )

                    while True:
                        line = process.stdout.readline()
                        if not line and process.poll() is not None:
                            break
                        #console.print(f"[dim]{line.strip()}[/]")  # Debug output
                        if compilation_progress.update(line):
                            progress.update(
                                task_id, completed=((pass_num - 1) * 50) + 25
                            )

                    return_code = process.wait()
                    if return_code != 0 or compilation_progress.errors:
                        error_context = cls.extract_error_context(log_file)
                        console.print("\n[bold red]Compilation errors:[/]")
                        for error in compilation_progress.errors + error_context:
                            console.print(f"[red]{error}[/]")
                        return False

                    progress.update(task_id, completed=pass_num * 50)

            return True

        except Exception as e:
            console.print(f"\n[bold red]Unexpected error:[/] {str(e)}")
            return False

        finally:
            os.chdir(current_dir)
            cls.clean_aux(file.parent)

    @classmethod
    def compile_all(
        cls, files: List[Path], latex_engine: LatexEngine = "xelatex"
    ) -> None:
        """Compiles multiple LaTeX files with multiple progress bars."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
        ) as progress:
            tasks = {
                file: progress.add_task(f"[bold blue]{file.name}", total=100)
                for file in files
            }

            for file, task_id in tasks.items():
                if TexFile(file, file.parent, file.stat().st_mtime).is_main_file:
                    cls.compile_latex(file, latex_engine, progress, task_id)
                else:
                    progress.update(task_id, description=f"[dim]{file.name} (skipped)")
                    progress.advance(task_id, 100)

    @classmethod
    def watch(cls, path_to_watch: Path, latex_engine: LatexEngine = "xelatex") -> None:
        """
        Watch LaTeX files for changes and compile them.
        Only watches the current directory and immediate subdirectories.
        Implements a 10-second delay between compilations.
        """

        class DepthLimitedLatexHandler(FileSystemEventHandler):
            def __init__(self):
                self.last_modified = (
                    {}
                )  # Dictionary to track last compilation time per file
                self.compilation_lock = (
                    {}
                )  # Dictionary to track if compilation is pending per file

            def should_process_path(self, file_path: str) -> bool:
                """
                Check if the file path should be processed based on depth and extension.
                """
                try:
                    path = Path(file_path)
                    watch_path = Path(path_to_watch)

                    if not path.suffix == ".tex":
                        return False

                    try:
                        path.relative_to(watch_path)
                    except ValueError:
                        return False

                    depth = len(path.relative_to(watch_path).parts)
                    return (
                        depth <= 2
                    )  # 1 for same directory, 2 for immediate subdirectory

                except Exception as e:
                    logger.error(f"Error checking path depth: {e}")
                    return False

            def schedule_compilation(self, path: Path):
                """
                Schedule a compilation after the cooldown period.
                """

                def delayed_compile():
                    time.sleep(
                        max(
                            0, 10 - (time.time() - self.last_modified.get(str(path), 0))
                        )
                    )
                    if path.is_file():  # Ensure file still exists
                        if TexFile(
                            path, path.parent, path.stat().st_mtime
                        ).is_main_file:
                            relative_path = path.relative_to(path_to_watch)
                            console.print(f"\n[bold blue]Compiling:[/] {relative_path}")
                            cls.compile_latex(path, latex_engine)
                        self.compilation_lock[str(path)] = False

                if not self.compilation_lock.get(str(path), False):
                    self.compilation_lock[str(path)] = True
                    threading.Thread(target=delayed_compile, daemon=True).start()

            def on_modified(self, event):
                if not event.is_directory and self.should_process_path(event.src_path):
                    path = Path(event.src_path)
                    current_time = time.time()
                    file_path = str(path)

                    if current_time - self.last_modified.get(file_path, 0) >= 10:
                        self.last_modified[file_path] = current_time
                        self.schedule_compilation(path)
                    else:
                        remaining = 10 - (
                            current_time - self.last_modified.get(file_path, 0)
                        )
                        logger.debug(
                            f"Skipping compilation, {remaining:.1f} seconds remaining in cooldown"
                        )

        # Set up the observer
        observer = Observer()
        handler = DepthLimitedLatexHandler()
        observer.schedule(handler, str(path_to_watch), recursive=True)

        try:
            console.print(f"[bold green]Watching directory:[/] {path_to_watch}")
            console.print(
                "[bold yellow]Note:[/] Only watching current directory and immediate subdirectories"
            )
            console.print("[dim]Press Ctrl+C to stop watching...[/]")
            observer.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Stopping watch mode...[/]")
            observer.stop()
        finally:
            observer.join()
