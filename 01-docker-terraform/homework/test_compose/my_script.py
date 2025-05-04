import sys
import argparse

if __name__ == "__main__":
    print("Arguments:", sys.argv)
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--param1')
    parser.add_argument('--param2')
    args = parser.parse_args()
    print("Parsed arguments:", args)
