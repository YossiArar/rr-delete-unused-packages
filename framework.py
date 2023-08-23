from multiprocessing import Process


class RunningFramework:
    def __init__(self, app_session: Process, before: dict = None, join_session: bool = False):
        self.__before_session = before
        self.__app_session = app_session
        self.__join_session = join_session
        self.__tasks = self.__session_tasks()

    @property
    def get_session_tasks(self):
        return self.__tasks

    @property
    def is_alive(self):
        return self.__app_session.is_alive()

    def kill(self):
        return self.__after()

    def run_session(self):
        next(self.__tasks)  # before all
        next(self.__tasks)  # running session
        next(self.__tasks)  # after all

    def __session_tasks(self):
        self.__before()
        yield
        self.__running()
        yield
        self.__after()
        yield

    def __before(self):
        print('Start App Session')
        session = []
        if self.__before_session is not None:
            for before in self.__before_session.items():
                before[1].start()
                session.append(before[1])
            self.__before_session = session

    def __running(self):
        print(f'{self.__app_session.name} is running..')
        self.__app_session.start()
        if self.__join_session:
            self.__app_session.join()
            self.__after()

    def __after(self):
        for process in self.__before_session:
            if type(process) is Process:
                if process.is_alive():
                    process.kill()
                print(f"{process.name} closed successfully")
            if self.__app_session.is_alive():
                self.__app_session.kill()
            print(f"{self.__app_session.name} closed successfully")
        print('End App Session')
