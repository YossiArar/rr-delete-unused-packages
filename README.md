# Description

This library reduces the size of the Python virtual environment according to the use of the libraries in the project.
The goal is to ensure that no library is left unused to optimize the use of existing resources.
ֿ
Applying the process is very easy and clear. It is important to know that you must not work in the tested environment until the end of the run. At the end of the process, you can decide whether to keep the newly created environment or return to the previous one, according to your considerations.


# Environment and Installations
- Install python version >= 3.10
- Go to the relevant project for test the virtual environment
- requirements.txt file should be in the project root path  
- Install rr-delete-unused-packages package from pypi:
```sh
pip install rr-delete-unused-packages
```


# Test your virtual environment
### option 1 - run this script from project root path, and put your project_env_file_path before start the process:
```code
import os
from rr_process.delete_unused_libs import UnusedDependencies

if __name__ == '__main__':
    project_main_fp, venv_fp = os.getcwd(), f"<project_env_file_path>"  
    UnusedDependencies(main_path=project_main_fp, venv_path=venv_fp).run()
```



### option 2 - run this script by terminal commands
