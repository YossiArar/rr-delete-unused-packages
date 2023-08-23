import glob
import os
import sys

import rr_process as rp


class UnusedDependencies:
    def __init__(self, main_path: str, venv_path: str):
        if not main_path or not venv_path:
            raise print(f"the project required main_path and venv_path values: {main_path}, {venv_path}.")
        self.__main_path, self.__venv_path = main_path, venv_path
        self.__ignore_current_requirements = False
        self.__current_dependencies = rp.get_dependencies(path=f"{self.__main_path}/{rp.REQ_FILE_NAME}")
        self.__temp_requirements = f"{self.__main_path}/update_requirements.txt"
        self.__venv_size = rp.get_venv_size(path=self.__venv_path)

    @property
    def __find_project_imports(self, internal_iterations: int = rp.INTERNAL_ENV_ITERATIONS):
        python_files = []
        main_depth = '/*'

        def ignore_file(py_f):
            for ig_f in rp.IGNORE_FILES:
                if ig_f in py_f:
                    return True

        while internal_iterations > 0:
            internal_iterations += -1
            files = glob.glob(f"{self.__main_path}{main_depth}.py")
            for file in files:
                if not ignore_file(file):
                    python_files.append(file)
            main_depth += '/*'
        return python_files

    @property
    def __import_python_syntax(self):
        python_files = self.__find_project_imports
        py_syntax = ''
        for py_file in python_files:
            py_syntax = rp.is_valid_python_file(py_file, py_syntax)
        return py_syntax

    def __get_test_dependencies(self):
        if self.__ignore_current_requirements:
            return rp.get_dependencies(path=self.__temp_requirements, ignore_dependencies=self.__current_dependencies)
        else:
            return rp.get_dependencies(path=self.__temp_requirements)

    def run(self, save_results: bool = True):
        print(f"Current size for project environment: {self.__venv_size}")
        os.system(f'pip freeze > {self.__temp_requirements}')
        final_dependencies = []
        py_syntax = self.__import_python_syntax
        if py_syntax:
            temp_python_file = 'py_import_validation.py'
            with open(temp_python_file, 'w') as py:
                py.write(py_syntax)
            test_dependencies = self.__get_test_dependencies()
            for index, dep in enumerate(test_dependencies, 1):
                os.system(f"pip uninstall {dep} --y")
                result = os.system(f'python {temp_python_file}')
                if result > 0:
                    os.system(f"pip install --no-dependencies {dep}")
                    final_dependencies.append(dep)
                    print(f"Test dependencies count so far:"
                          f" {index}/{len(test_dependencies) + len(self.__current_dependencies)}."
                          f" for now {len(final_dependencies)} libraries are required.")
            os.remove(self.__temp_requirements)
            os.remove(temp_python_file)
            print(f"Start with {len(test_dependencies) + len(self.__current_dependencies)},"
                  f" finish with {len(final_dependencies)}")
            if save_results:
                self.__save_updated_requirements(final_dependencies=final_dependencies)
            print(f"Start with {self.__venv_size}")
            print(f"Finish with {rp.get_venv_size(path=self.__venv_path)}")

    def __save_updated_requirements(self, final_dependencies: list):
        final_requirements = ''
        for fr in final_dependencies:
            final_requirements += f"{fr}\n"
        with open(self.__temp_requirements, 'w') as req:
            req.write(final_requirements)
        print(f'Save result here: {self.__temp_requirements}')


if __name__ == '__main__':
    project_main_fp, venv_fp = None, None
    if len(sys.argv) > 1:
        project_main_fp, venv_fp = sys.argv[1], sys.argv[2]
    UnusedDependencies(main_path=project_main_fp, venv_path=venv_fp).run()
