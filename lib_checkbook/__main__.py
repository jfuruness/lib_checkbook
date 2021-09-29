from argparse import ArgumentParser
import os

from .check_sender import CheckSender

def main():
    try:
        parser = ArgumentParser(description="Runs a DDOS simulation")
        parser.add_argument("csv_path", type=str)
        parser.add_argument("err_csv_path", type=str)
        args = parser.parse_args()
    except Exception as e:
        # Convert to logging in a real app
        parser.print_help()
        return

    CheckSender().send_checks(args.csv_path, args.err_csv_path)
