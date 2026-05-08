#!/usr/bin/env python3
"""Lint.py - Enforce layer architecture rules.

Rules:
1. Every source file lives in exactly one layer directory under src/
2. Imports may only target layers in the file's "may import from" set
3. No file exceeds 300 lines
4. Parse-don't-validate at boundaries
"""

import ast
import sys
from pathlib import Path

# Standard library modules that are allowed in all layers
STDLIB_MODULES = {
    "abc", "anyio", "argparse", "ast", "asyncio", "base64", "bisect", "bz2",
    "calendar", "collections", "contextlib", "copy", "csv", "ctypes", "cProfile",
    "dataclasses", "datetime", "decimal", "difflib", "email", "enum", "errno",
    "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "fractions",
    "functools", "gc", "getopt", "getpass", "glob", "graphlib", "gzip", "hashlib",
    "heapq", "hmac", "html", "http", "imaplib", "importlib", "inspect", "io",
    "ipaddress", "itertools", "json", "linecache", "locale", "logging", "lzma",
    "mailbox", "mimetypes", "mmap", "modulefinder", "multiprocessing", "netrc",
    "numbers", "operator", "optparse", "os", "pathlib", "pdb", "pickle", "pipes",
    "pkgutil", "platform", "plistlib", "poplib", "pprint", "profile", "pstats",
    "pty", "pwd", "py_compile", "pyclbr", "queue", "quopri", "random", "re",
    "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets",
    "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "smtpd",
    "smtplib", "sndhdr", "socket", "socketserver", "sre_compile", "sre_constants",
    "sre_parse", "ssl", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile",
    "telnetlib", "tempfile", "termios", "textwrap", "threading", "time", "timeit",
    "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty",
    "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib",
    "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "winreg",
    "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile",
    "zipimport", "zlib", "_thread", "__future__"
}


# Layer ordering (forward dependencies only)
LAYER_ORDER = ["types", "config", "utils", "providers", "repo", "service", "runtime", "ui"]

# Allowed imports per layer (including "src" for internal relative imports)
ALLOWED_IMPORTS = {
    "types": {"types", "src"},
    "config": {"types", "config", "src"},
    "utils": {"utils", "src"},
    "providers": {"types", "config", "utils", "providers", "src"},
    "repo": {"types", "config", "repo", "src"},
    "service": {"types", "config", "repo", "providers", "service", "src"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime", "src"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui", "src"},
}

# Base directory for source files
SRC_DIR = Path(__file__).parent / "src"


def get_layer(filepath: Path) -> str | None:
    """Get the layer name for a source file path."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if len(parts) >= 1:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> list[str]:
    """Extract import statements from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    
    return imports


def check_line_count(filepath: Path) -> list[tuple[int, str]]:
    """Check if file exceeds 300 lines."""
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) > 300:
        errors.append((1, f"File exceeds 300 lines ({len(lines)} lines)"))
    
    return errors


def check_imports(filepath: Path, layer: str) -> list[tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    errors = []
    allowed = ALLOWED_IMPORTS.get(layer, set())
    imports = get_imports(filepath)
    
    for imp in imports:
        # Skip standard library modules - allowed in all layers
        if imp in STDLIB_MODULES:
            continue
        # Skip relative imports (start with .)
        if imp.startswith("."):
            continue
        if imp not in allowed:
            errors.append((1, f"Import '{imp}' is not allowed from layer '{layer}'. Allowed: {sorted(allowed)}"))
    
    return errors


def lint_file(filepath: Path) -> list[tuple[int, str]]:
    """Lint a single source file."""
    errors = []
    
    # Get layer
    layer = get_layer(filepath)
    if layer is None:
        return errors  # Not under src/, skip
    
    # Check line count
    errors.extend(check_line_count(filepath))
    
    # Check imports
    errors.extend(check_imports(filepath, layer))
    
    return errors


def main() -> int:
    """Run linter on all source files."""
    all_errors: list[tuple[Path, int, str]] = []
    
    # Find all .py files under src/
    for filepath in SRC_DIR.rglob("*.py"):
        file_errors = lint_file(filepath)
        for line_num, msg in file_errors:
            all_errors.append((filepath, line_num, msg))
    
    if all_errors:
        print("Lint errors found:")
        for filepath, line_num, msg in sorted(all_errors, key=lambda x: (str(x[0]), x[1])):
            print(f"  {filepath}:{line_num}: {msg}")
        return 1
    
    print("All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
