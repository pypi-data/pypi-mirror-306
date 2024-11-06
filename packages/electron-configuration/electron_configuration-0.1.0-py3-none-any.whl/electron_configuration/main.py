# electron_configuration/main.py

import argparse
from .configuration import ElectronConfiguration

def main():
    parser = argparse.ArgumentParser(description="Get electron configuration of elements.")
    parser.add_argument("atomic_number", type=int, help="Atomic number of the element")
    args = parser.parse_args()

    # Initialize the ElectronConfiguration object
    ec = ElectronConfiguration()

    # Get and print the electron configuration
    print(f"\n{ec.pretty_print(args.atomic_number)}")

if __name__ == "__main__":
    main()
