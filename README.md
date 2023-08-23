# rr-delete-unused-packages

This library is designed to reduce the size of your Python virtual environment based on the actual usage of libraries in
your project. The primary objective is to eliminate any unused libraries to optimize resource utilization effectively.
The process is straightforward and user-friendly. However, it's crucial to refrain from working within the tested
environment until the process is complete. At the conclusion of the process, you'll have the flexibility to decide
whether to retain the newly created environment or revert to the previous one, depending on your specific requirements.

# Environment and Installations

- Ensure that you have Python version 3.10 or higher installed.
- Navigate to the relevant project where you want to test the virtual environment.
- Ensure that a requirements.txt file is present in the project's root path.
- Install the rr-delete-unused-packages package from PyPI using the following command:

```sh
pip install rr-delete-unused-packages
```

# Test your virtual environment

### Run this script from the project's root path:

```sh
import os
from rr_process.delete_unused_libs import UnusedDependencies

if __name__ == '__main__':
    project_main_fp, venv_fp = os.getcwd(), f"<project_env_file_path>"  
    UnusedDependencies(main_path=project_main_fp, venv_path=venv_fp).run()
```

### The second option is start a new session by terminal command:
```sh
python3 ./<script_env_file_path>/delete_unused_libs.py ./ ./<project_env_file_path>
```

#### Please make sure to replace <project_env_file_path> & <script_env_file_path> with the actual path to your project's environment path.

