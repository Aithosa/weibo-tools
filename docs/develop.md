# Development Guide
## Generating `requirements.txt`
This project currently uses the `pipreqs` tool.
### Using pipreqs
1. Install pipreqs:
    ```shell
        pip install pipreqs
    ```
2. Generate the requirements.txt file:
    ```shell
        pipreqs /path/to/your/project --force
    ```
   Where /path/to/your/project is the root directory of your project.
