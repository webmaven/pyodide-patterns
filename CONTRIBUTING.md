# Contributing to Pyodide Patterns Cookbook

We welcome contributions to the Pyodide Patterns Cookbook! Whether you're fixing a bug, adding a new pattern, or improving documentation, your help is appreciated.

## Getting Started

To get started, you'll need to have Python 3.8+ and [Hatch](https://hatch.pypa.io/latest/) installed.

1.  **Fork and Clone:** Fork the repository on GitHub and clone your fork locally.
2.  **Install Dependencies:** Navigate to the project directory and install the dependencies using Hatch:

    ```bash
    hatch shell
    ```

3.  **Run Tests:** To ensure everything is set up correctly, run the test suite:

    ```bash
    hatch run test
    ```

## Making Changes

1.  **Create a Branch:** Create a new branch for your changes:

    ```bash
    git checkout -b my-new-feature
    ```

2.  **Make Your Changes:** Make your changes to the code and add or update tests as needed.
3.  **Run the Linter:** Before committing, run the linter to ensure your code follows the project's style guidelines:

    ```bash
    hatch run lint
    ```

4.  **Commit Your Changes:** Commit your changes with a clear and descriptive commit message.
5.  **Push to Your Fork:** Push your changes to your fork on GitHub.
6.  **Create a Pull Request:** Open a pull request from your fork to the main repository.

## Reporting Bugs

If you find a bug, please open an issue on GitHub. Include a clear description of the bug, steps to reproduce it, and any relevant error messages.

## Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one, please open an issue on GitHub to discuss it.
