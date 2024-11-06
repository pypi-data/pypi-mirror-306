# runpy_tool/runpy.py

import sys
import subprocess

def main():
    # Check if a script name and input file were provided
    if len(sys.argv) < 3:
        print("Usage: runpy script.py input.txt [args]")
        sys.exit(1)

    # Extract the script name, input file, and additional arguments
    script_name = sys.argv[1]
    input_file = sys.argv[2]
    script_args = sys.argv[3:]

    # Run the specified Python script with the input file and additional arguments
    try:
        with open("output.txt", "w") as output, open(input_file, "r") as input_data:
            subprocess.run(
                ["python3", script_name] + script_args,
                check=True,
                stdin=input_data,        # Provide input file as standard input
                stdout=output,           # Redirect stdout to output.txt
                stderr=subprocess.STDOUT  # Redirect stderr to output.txt
            )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
