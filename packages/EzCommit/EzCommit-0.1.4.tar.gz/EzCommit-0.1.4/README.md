# EzCommit

A simple tool for generating and managing Git commits using OpenAI for commit message suggestions.

## Description

EzCommit is a command-line tool designed to simplify the process of generating commit messages and managing Git commits. It leverages OpenAI to suggest commit messages based on the changes in your repository, making it easier to create meaningful and descriptive commit messages. The tool also provides options for displaying a visual log of commits and generating pull request content.

## Getting Started

### Dependencies

* Python 3.11 or higher
* Git
* OpenAI API key (for commit message suggestions)

### Installing

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ezcommit.git
   cd ezcommit
   ```

2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Executing program

1. Initialize the configuration:
   ```
   python main.py --init
   ```

2. Generate a commit message:
   ```
   python main.py --gc
   ```

3. Display a visual log of commits:
   ```
   python main.py --visual
   ```

4. Summarize the changes:
   ```
   python main.py --sum
   ```

5. Create a pull request:
   ```
   python main.py --gen_pr
   ```

6. Create a README file:
   ```
   python main.py --readme
   ```

## Help

If you encounter any issues, you can run the following command to display the help message:
```
python main.py --help
```

## Authors

* Your Name - [Your GitHub Profile](https://github.com/yourusername)

## Version History

* 0.2
    * Added new test functions for the `Controller` class