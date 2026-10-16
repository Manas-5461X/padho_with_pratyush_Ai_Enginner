"""
Coding agent ke 3 tools. Har tool ek normal Python function hai jo string return karta hai
(LLM ko sirf text samajh aata hai).

    search_files    -> bug se related files ke paths
    search_in_file  -> file ke andar keyword wali lines, line numbers ke saath
    replace_line    -> ek line ko nayi line se badlo
"""

from pathlib import Path


CODE_EXTENSIONS = {".cpp", ".cc", ".c", ".h", ".hpp"}


def code_files(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.rglob("*") if p.is_file() and p.suffix in CODE_EXTENSIONS)


def make_tools(workspace: Path) -> dict:
    """Saare tools sirf is ek folder ke andar kaam karte hain."""
    workspace = workspace.resolve()

    def rel(path: Path) -> str:
        return path.relative_to(workspace).as_posix()

    def resolve(path: str) -> Path | None:
        # LLM workspace ke bahar ki file na chhu paaye (jaise ../../.env)
        full = (workspace / path).resolve()
        if not full.is_relative_to(workspace) or not full.is_file():
            return None
        return full

    def read_lines(full: Path) -> list[str]:
        # newline="" -> Windows ke \r\n jaise the waise hi rehte hain
        with open(full, encoding="utf-8", newline="") as f:
            return f.read().splitlines(keepends=True)

    # --------------------------------------------------------
    # TOOL 1 -- SEARCH FILES
    # --------------------------------------------------------

    def search_files(keyword: str) -> str:
        files = code_files(workspace)
        if not files:
            return "The workspace has no code files."

        found = []
        for f in files:
            hits = f.read_text(encoding="utf-8").lower().count(keyword.lower()) if keyword else 0
            if not keyword or hits or keyword.lower() in f.name.lower():
                found.append(f"{rel(f)}  ({hits} matches)" if keyword else rel(f))

        if not found:
            # kuch nahi mila to bhi saari files dikha do, LLM wahan se aage badhe
            return f"No file mentions '{keyword}'. All code files:\n" + "\n".join(rel(f) for f in files)
        return "\n".join(found)

    # --------------------------------------------------------
    # TOOL 2 -- SEARCH IN FILE
    # --------------------------------------------------------

    def search_in_file(path: str, keyword: str) -> str:
        full = resolve(path)
        if full is None:
            return f"File '{path}' not found. Use a path exactly as search_files returned it."

        lines = [line.rstrip("\r\n") for line in read_lines(full)]
        matches = [(n, line) for n, line in enumerate(lines, 1) if keyword.lower() in line.lower()]

        if not matches:
            return f"'{keyword}' not found in {path}. Try another keyword, or an empty keyword to see the whole file."
        return "\n".join(f"{n:>4}: {line}" for n, line in matches)

    # --------------------------------------------------------
    # TOOL 3 -- REPLACE LINE
    # --------------------------------------------------------

    def replace_line(path: str, line_number: int, new_line: str) -> str:
        full = resolve(path)
        if full is None:
            return f"File '{path}' not found. Use a path exactly as search_files returned it."
        if "\n" in new_line or "\r" in new_line:
            return "new_line must be ONE line. Put multiple statements on the same line if needed."

        lines = read_lines(full)
        line_number = int(line_number)  # LLM kabhi "17" string bhej deta hai
        if not 1 <= line_number <= len(lines):
            return f"{path} has {len(lines)} lines, there is no line {line_number}."

        old = lines[line_number - 1]
        old_text = old.rstrip("\r\n")
        ending = old[len(old_text):]

        # LLM indentation bhool jaaye to purani line wali indentation rakh lo
        if new_line.strip() and not new_line[0].isspace():
            new_line = old_text[: len(old_text) - len(old_text.lstrip())] + new_line

        lines[line_number - 1] = new_line + ending
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.writelines(lines)

        return f"Line {line_number} of {path} replaced.\nbefore: {old_text.strip()}\nafter : {new_line.strip()}"

    return {
        "search_files": search_files,
        "search_in_file": search_in_file,
        "replace_line": replace_line,
    }


# ============================================================
# TOOL DEFINITIONS FOR THE LLM
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": (
                "Find which code files are related to the bug. Returns file paths whose name "
                "or content contains the keyword. An empty keyword lists every code file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "A function name, variable or word from the bug, e.g. 'factorial'.",
                    }
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": (
                "Show the lines of one file that contain the keyword, with their line numbers. "
                "An empty keyword shows the whole file with line numbers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path exactly as search_files returned it."},
                    "keyword": {"type": "string", "description": "Text to look for. Empty string = whole file."},
                },
                "required": ["path", "keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "replace_line",
            "description": "Replace one whole line of a file with a new line. Line numbers come from search_in_file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path exactly as search_files returned it."},
                    "line_number": {"type": "integer", "description": "1-based number of the line to replace."},
                    "new_line": {"type": "string", "description": "The complete new line of code (one line only)."},
                },
                "required": ["path", "line_number", "new_line"],
            },
        },
    },
]
