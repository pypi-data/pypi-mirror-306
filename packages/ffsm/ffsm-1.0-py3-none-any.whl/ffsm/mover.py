import os
import glob
import argparse

def move_files(pattern, new_name):
    files = glob.glob(pattern)
    for file in files:
        # Get the base name without the extension
        base = os.path.splitext(file)[0]
        # Construct the new filename with the given new_name
        # Ensure the new_name reflects the expected filename
        new_filename = f"{base}.{new_name}" if not new_name.startswith('.') else f"{base}{new_name}"
        os.rename(file, new_filename)
        print(f"Renamed '{file}' to '{new_filename}'")

def cli():
    parser = argparse.ArgumentParser(description='Rename files using wildcards.')
    parser.add_argument('pattern', type=str, help='Wildcard pattern to match files or single filename.')
    parser.add_argument('new_name', type=str, help='New filename to apply, not just the extension.')
    args = parser.parse_args()
    
    move_files(args.pattern, args.new_name)

if __name__ == "__main__":
    cli()
