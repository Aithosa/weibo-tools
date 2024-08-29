# Development Guide
## Generating `requirements.txt`
This project uses GitHub Actions to automatically generate the `requirements.txt` file 
when a pull request is created or updated. 

**Manual changes to the `requirements.txt` file may be overwritten.**

### Automatic Generation
Here's how the process works:
When a pull request is **opened or synchronized** (i.e., new commits are pushed to the source branch), 
the GitHub Action workflow will:
   1. Check out the repository.
   2. Set up the Python environment.
   3. Install necessary dependencies, including `pipreqs`.
   4. Generate the `requirements.txt` file.
   5. Commit and push the updated `requirements.txt` back to the repository if there are any changes.

### Manual Generation
If you need to manually generate the `requirements.txt` file:
1. Install pipreqs:
    ```shell
    pip install pipreqs
    ```
2. Generate the `requirements.txt` file (but be aware it may be overwritten by GitHub Actions):
    ```shell
    pipreqs /path/to/your/project --force
    ```
   Where `/path/to/your/project` is the root directory of your project.
