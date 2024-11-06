import typer
from pathlib import Path
from typing import Optional, List, Set
import pathspec
import pyperclip

app = typer.Typer()

# Default directories to ignore
DEFAULT_IGNORE_DIRS = {
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "build",
    "dist",
    "target",
    ".vs",
    "bin",
    "obj",
    "publish",
}

# Default files to ignore
DEFAULT_IGNORE_FILES = {
    "poetry.lock",
    "package-lock.json",
    "Cargo.lock",
    ".DS_Store",
    "yarn.lock",
    "copcon_output.txt"
}


def parse_copconignore(ignore_file: Path) -> pathspec.PathSpec:
    """
    Parses the ignore patterns from a given .copconignore file using pathspec.

    Args:
        ignore_file (Path): Path to the .copconignore file.

    Returns:
        pathspec.PathSpec: A PathSpec object for pattern matching.
    """
    if not ignore_file.exists():
        return pathspec.PathSpec.from_lines("gitwildmatch", [])

    try:
        with ignore_file.open() as f:
            patterns = [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    except Exception as e:
        typer.echo(f"Error reading ignore file: {e}", err=True)
        return pathspec.PathSpec.from_lines("gitwildmatch", [])


def should_ignore(path: Path, ignore_spec: pathspec.PathSpec) -> bool:
    """
    Determines if a given path should be ignored based on the ignore patterns.

    Args:
        path (Path): The path to check.
        ignore_spec (pathspec.PathSpec): PathSpec object with ignore patterns.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    # Convert Path to string and add a trailing slash for directories
    path_str = str(path)
    if path.is_dir():
        path_str += "/"
    return ignore_spec.match_file(path_str)


def generate_tree(
    directory: Path,
    prefix: str = "",
    depth: int = -1,
    ignore_dirs: Set[str] = DEFAULT_IGNORE_DIRS,
    ignore_files: Set[str] = DEFAULT_IGNORE_FILES,
    ignore_spec: pathspec.PathSpec = pathspec.PathSpec([]),
    root: Optional[Path] = None,
) -> str:
    if depth == 0:
        return ""

    if root is None:
        root = directory

    output = []
    contents = list(directory.iterdir())
    contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

    visible_contents = []

    for path in contents:
        relative_path = path.relative_to(root)
        if path.is_dir() and path.name in ignore_dirs:
            continue
        if path.is_file() and path.name in ignore_files:
            continue
        if should_ignore(relative_path, ignore_spec):
            continue
        visible_contents.append(path)

    for i, path in enumerate(visible_contents):
        is_last = i == len(visible_contents) - 1
        current_prefix = "└── " if is_last else "├── "

        if path.is_dir():
            subtree_prefix = "    " if is_last else "│   "
            subtree = generate_tree(
                path,
                prefix + subtree_prefix,
                depth - 1 if depth > 0 else -1,
                ignore_dirs,
                ignore_files,
                ignore_spec,
                root,
            )
            if subtree:  # Only include non-empty directories
                output.append(f"{prefix}{current_prefix}{path.name}")
                output.append(subtree)
        else:
            output.append(f"{prefix}{current_prefix}{path.name}")

    return "\n".join(output)


def get_file_content(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file: {file_path}\nError: {str(e)}\n"


def copy_to_clipboard(text: str):
    """
    Copies the given text to the system clipboard using pyperclip.
    """
    try:
        pyperclip.copy(text)
        typer.echo("Directory structure and file contents have been copied to clipboard.")
    except pyperclip.PyperclipException as e:
        raise e


@app.command()
def main(
    directory: Path = typer.Argument(..., help="The directory to process"),
    depth: Optional[int] = typer.Option(
        -1, help="Depth of directory tree to display (-1 for unlimited)"
    ),
    exclude_hidden: bool = typer.Option(
        True, help="Exclude hidden files and directories"
    ),
    ignore_dirs: Optional[List[str]] = typer.Option(
        None, help="Additional directories to ignore"
    ),
    ignore_files: Optional[List[str]] = typer.Option(
        None, help="Additional files to ignore"
    ),
    copconignore: Optional[Path] = typer.Option(
        None, help="Path to .copconignore file"
    ),
    output_file: Optional[Path] = typer.Option(
        None, help="Output file path (if not using clipboard)"
    ),
):
    """
    Generate a report of directory structure and file contents, then copy it to clipboard.
    """
    if not directory.is_dir():
        typer.echo(f"Error: {directory} is not a valid directory.", err=True)
        raise typer.Exit(code=1)

    dirs_to_ignore = DEFAULT_IGNORE_DIRS.copy()
    if ignore_dirs:
        dirs_to_ignore.update(ignore_dirs)

    files_to_ignore = DEFAULT_IGNORE_FILES.copy()
    if ignore_files:
        files_to_ignore.update(ignore_files)

    ignore_spec = pathspec.PathSpec([])
    if copconignore:
        ignore_spec = parse_copconignore(copconignore)
    else:
        default_copconignore = directory / ".copconignore"
        if default_copconignore.exists():
            ignore_spec = parse_copconignore(default_copconignore)

    output = []
    output.append("Directory Structure:")
    output.append(directory.name)
    output.append(
        generate_tree(
            directory,
            depth=depth,
            ignore_dirs=dirs_to_ignore,
            ignore_files=files_to_ignore,
            ignore_spec=ignore_spec,
        )
    )
    output.append("\nFile Contents:")

    for file_path in directory.rglob("*"):
        if file_path.is_file():
            if exclude_hidden and (
                file_path.name.startswith(".")
                or any(part.startswith(".") for part in file_path.parts)
            ):
                continue
            if any(ignore_dir in file_path.parts for ignore_dir in dirs_to_ignore):
                continue
            if file_path.name in files_to_ignore:
                continue
            relative_path = file_path.relative_to(directory)
            if should_ignore(relative_path, ignore_spec):
                continue
            output.append(f"\nFile: {relative_path}")
            output.append("-" * 40)
            output.append(get_file_content(file_path))
            output.append("-" * 40)

    full_output = "\n".join(output)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_output)
            typer.echo(f"Output written to {output_file}")
        except Exception as e:
            typer.echo(f"Error writing to file: {e}", err=True)
            raise typer.Exit(code=1)
    else:
        try:
            copy_to_clipboard(full_output)
        except pyperclip.PyperclipException as e:
            typer.echo(f"Error copying to clipboard: {e}", err=True)
            typer.echo("Falling back to file output: copcon_output.txt")
            try:
                with open('copcon_output.txt', 'w', encoding='utf-8') as f:
                    f.write(full_output)
                typer.echo("Output written to copcon_output.txt")
            except Exception as file_e:
                typer.echo(f"Error writing to file: {file_e}", err=True)
                raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
