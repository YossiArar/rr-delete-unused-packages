import os.path


class PyPIArtifact:
    def __init__(self, main_path, user=None, password=None):
        self.__dist_dir = f"{main_path}/dist"
        if user is not None:
            self.__user = user
            self.__password = password
        else:
            self.__user = os.environ.get('pypi-user')
            self.__password = os.environ.get('pypi-password')
        self.__build_commands = self.__build_terminal_commands

    @property
    def __build_terminal_commands(self):
        return ["python setup.py develop", "python -m pip install --upgrade pip",
                "python -m pip install --upgrade build", "python -m build", "python setup.py sdist bdist_wheel"]

    @property
    def __upload_terminal_command(self):
        return f"twine upload -u {self.__user} -p {self.__password}" \
               f" --repository-url https://upload.pypi.org/legacy/ dist/*"

    def __delete_dist_dir(self):
        if os.path.exists(self.__dist_dir) and os.path.isdir(self.__dist_dir):
            shutil.rmtree(self.__dist_dir)
        else:
            print("The dist directory does not exist")

    def __build(self):
        for command in self.__build_commands:
            os.system(command)

    def __upload(self):
        os.system(self.__upload_terminal_command)

    def run(self):
        self.__delete_dist_dir()
        self.__build()
        self.__upload()


if __name__ == '__main__':
    PyPIArtifact(main_path=os.path.dirname(__file__)).run()
