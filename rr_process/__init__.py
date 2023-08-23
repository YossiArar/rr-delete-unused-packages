import ast
import os

REQ_FILE_NAME, INTERNAL_ENV_ITERATIONS = 'requirements.txt', 10
IGNORE_FILES = 'site-packages', 'env', 'setup', 'py_import_validation.py', 'delete_unnecessary_libraries.py', 'delete_unused_libraries.py'


def calculate_venv_size(path: str):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += calculate_venv_size(entry.path)
    return total


def get_venv_size(path: str, suffix="B"):
    num = calculate_venv_size(path)
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def get_dependencies(path, ignore_dependencies: list = None):
    dependencies = []
    if os.path.isfile(path):
        with open(path, 'r') as f:
            dependencies = f.read().splitlines()
    if not ignore_dependencies:
        return dependencies
    organize_dependencies = []
    ignore_dependencies = str(ignore_dependencies)
    for depend in dependencies:
        var = depend.split('==')[0]
        if var not in ignore_dependencies and depend not in ignore_dependencies:
            organize_dependencies.append(depend)
    return organize_dependencies


def is_valid_python_file(file_path, py_file_syntax):
    with open(file_path, 'r') as fp:
        contents = fp.read()
    try:
        ast.parse(contents)
        import_list = compile(contents, file_path, 'exec', ast.PyCF_ONLY_AST)
        for im in import_list.body:
            import_row = None
            if type(im) is ast.Import:
                import_row = f'import {im.names[0].name}\n'
            elif type(im) is ast.ImportFrom:
                import_row = f'from {im.module} import {im.names[0].name}\n'
            if import_row and import_row not in py_file_syntax:
                py_file_syntax += import_row
        return py_file_syntax
    except SyntaxError:
        return False
