#packages
import argparse
import sys

#project includes
from entry_points.run_test import RunTest

def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='module', required=True)

    # module data_utility
    p_testing = subparsers.add_parser('testing')
    p_testing.add_argument('mode', choices=['echo_msg'])
    p_testing.add_argument('arg0', type=str, nargs='?')


    args = parser.parse_args()

    if args.module == 'testing':
        if args.mode == 'help' or args.arg0 is None:
            print("Usage:")
            print("main.py testing help")
            print("main.py testing echo_msh <message>")
            sys.exit(0)
        elif args.mode == 'echo_msg':
            try:
                msg: str = args.arg0
            except (TypeError, ValueError):
                print("[ERROR] Invalid or missing arguments for 'echo_msh'.")
                p_testing.print_help()
                sys.exit(1)
            # Replace this with your actual function call
            RunTest.run_test(
                msg
            )
        else:
            print("[ERROR] Invalid mode for testing.")
            p_testing.print_help()
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    # For debugging, uncomment the next line:
    msg = "hello from beyond the entry point"
    sys.argv = ["main.py", "testing", "echo_msg", msg]
    main()