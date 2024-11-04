import argparse
import os
import requests
import gzip
import shutil
from pathlib import Path


def generate_tests(input_dir, output_dir):
    # Retrieve the endpoint URL from environment variables
    endpoint_url = os.getenv("TESTFORGE_ENDPOINT_URL")
    if not endpoint_url:
        print("Error: TESTFORGE_ENDPOINT_URL environment variable is not set.")
        return

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Compress the files to send to the endpoint
    with gzip.open("compressed_files.tar.gz", "wb") as f_out:
        with shutil.make_archive("files", 'tar', input_dir) as f_in:
            shutil.copyfileobj(f_in, f_out)

    # Send the compressed file to the cloud endpoint
    with open("compressed_files.tar.gz", "rb") as file_data:
        response = requests.post(endpoint_url, files={"file": file_data})

    if response.status_code == 200:
        # Save the response as test files in the output directory
        for filename, content in response.json().items():
            with open(os.path.join(output_dir, filename), 'w') as f:
                f.write(content)
    else:
        print("Error:", response.text)


def main():
    parser = argparse.ArgumentParser(description="TestForge CLI Tool")
    parser.add_argument("-v", "--version",
                        action="store_true", help="Show version")
    parser.add_argument("-g", "--generate", type=str,
                        help="Directory to generate pytest cases for")
    parser.add_argument("-o", "--output", type=str, default="tests",
                        help="Output directory for generated tests")
    args = parser.parse_args()

    if args.version:
        print("TestForge version 1.0.0")
    elif args.generate:
        generate_tests(args.generate, args.output)
    else:
        parser.print_help()
