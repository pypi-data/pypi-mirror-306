# TestForge

**TestForge** A CLI tool to generate pytest test cases using AI.

## Features

- **Generate Tests**: Automatically generates pytest test cases for a specified directory or file.
- **Output Directory**: Specify a custom output directory for the generated test files (default is `tests`).
- **Configurable Endpoint**: Set an environment variable `TESTFORGE_ENDPOINT_URL` for the endpoint URL.

## Installation

Install TestForge via pip:

```bash
pip install testforge
```

## Usage

### Setting Up the Endpoint URL

TestForge requires an environment variable `TESTFORGE_ENDPOINT_URL` to define the cloud endpoint for uploading files. To set it up, use the following command:

```bash
export TESTFORGE_ENDPOINT_URL="https://your-cloud-endpoint.com/generate-tests"
```

Replace `"https://your-cloud-endpoint.com/generate-tests"` with the actual URL of your endpoint. This variable needs to be set in every session where you use TestForge or added to your shell configuration file (e.g., `.bashrc` or `.zshrc`) for persistence.

### Command Options

TestForge provides several options that can be used in the command line:

- **Show Version**: Check the version of TestForge.

  ```bash
  testforge -v
  ```

- **Generate Tests**: Generate pytest cases for a specified directory.

  ```bash
  testforge -g path/to/your/directory
  ```

- **Specify Output Directory**: Define a custom directory for the generated test files.
  ```bash
  testforge -g path/to/your/directory -o custom_output_directory
  ```

## Example

```bash
export TESTFORGE_ENDPOINT_URL="https://your-cloud-endpoint.com/generate-tests"
testforge -g src -o tests
```
