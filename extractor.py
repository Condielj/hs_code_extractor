import os
import re
import sys
import glob


def extract_numbers(input_file):
    """
    Extract free-standing numbers with periods or dashes,
    OR free-standing numbers with 1-3 trailing letters from a file.

    Returns a list of unique extracted numbers, excluding:
    - Single-digit numbers
    - Numbers separated by semicolons (likely times)
    """
    pattern = r"\b\d{2,}((\.\d+)+|(-\d+)+)?([a-zA-Z]{1,3})?\b"

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Process matches to get the full strings
    unique_numbers = set()
    for match in re.finditer(pattern, content):
        number = match.group(0)
        # Skip numbers containing semicolons (likely times)
        if ":" not in number:
            unique_numbers.add(number)

    return sorted(list(unique_numbers))


def process_file(input_file):
    """Process a single file and extract numbers."""
    print(f"Processing {input_file}...")

    # Extract base name for output file
    base_name = os.path.basename(input_file)
    output_file = os.path.join("output", f"OUTPUT_{base_name}")

    # Extract numbers
    numbers = extract_numbers(input_file)

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        for number in numbers:
            f.write(f"{number}\n")

    print(f"Extracted {len(numbers)} numbers. Results saved to {output_file}")


def main():
    """Main function to handle command line arguments and process files."""
    # Create input and output directories if they don't exist
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Check if a specific file was provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            input_file = os.path.join("input", input_file)

        if os.path.exists(input_file):
            process_file(input_file)
        else:
            print(f"Error: File '{input_file}' not found.")
            sys.exit(1)
    else:
        # Process all files in input directory
        input_files = glob.glob(os.path.join("input", "*"))
        if not input_files:
            print("No files found in input directory.")
            sys.exit(1)

        for input_file in input_files:
            process_file(input_file)


if __name__ == "__main__":
    main()
