import argparse
from .textify import process_file

def main():
    parser = argparse.ArgumentParser(description="Process one argument.")
    parser.add_argument("file_path")
    args = parser.parse_args()
    file_path = args.file_path
    print(f"Processing {file_path}...")
    print(process_file(file_path))

if __name__ == "__main__":
    main()