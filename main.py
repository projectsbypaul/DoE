# packages
import argparse
import sys

# project includes
from entry_points.run_test import RunTest
from entry_points.run_taguchi import RunTaguchi  # NEW

def main():
    parser = argparse.ArgumentParser(prog="main.py")
    subparsers = parser.add_subparsers(dest="module", required=True)

    # ---- testing ------------------------------------------------------------
    p_testing = subparsers.add_parser("testing", help="simple echo test")
    p_testing.add_argument("mode", choices=["echo_msg", "help"])
    p_testing.add_argument("arg0", type=str, nargs="?")

    # ---- taguchi ------------------------------------------------------------
    p_taguchi = subparsers.add_parser("taguchi", help="Generate DoE schedules from inner/outer spec")
    p_taguchi.add_argument("mode", choices=["schedule", "help"])
    p_taguchi.add_argument("--spec", required=False, help="Path to semicolon-separated spec file")
    p_taguchi.add_argument("--design", choices=["AUTO", "GRID", "L9", "SUBSET"], default="AUTO")
    p_taguchi.add_argument("--subset-size", type=int, default=None, help="For SUBSET design")
    p_taguchi.add_argument("--add-center", action="store_true", help="Include center point")
    p_taguchi.add_argument("--order", choices=["by-design", "nested", "interleave-first"], default="by-design")
    p_taguchi.add_argument("--out", default="schedule.csv", help="Output CSV path")
    p_taguchi.add_argument("--base-rng", type=int, default=1234, help="Base RNG for schedule shuffling")

    args = parser.parse_args()

    # ---- dispatch -----------------------------------------------------------
    if args.module == "testing":
        if args.mode == "help" or args.arg0 is None:
            print("Usage:")
            print("  main.py testing help")
            print("  main.py testing echo_msg <message>")
            sys.exit(0)
        elif args.mode == "echo_msg":
            try:
                msg: str = args.arg0
            except (TypeError, ValueError):
                print("[ERROR] Invalid or missing arguments for 'echo_msg'.")
                p_testing.print_help()
                sys.exit(1)
            RunTest.run_test(msg)
            sys.exit(0)

    elif args.module == "taguchi":
        if args.mode == "help" or not args.spec:
            print("Usage:")
            print("  main.py taguchi help")
            print("  main.py taguchi schedule --spec <file> [--design AUTO|GRID|L9|SUBSET] "
                  "[--subset-size K] [--add-center] [--order by-design|nested|interleave-first] "
                  "[--out schedule.csv] [--base-rng 1234]")
            sys.exit(0)
        elif args.mode == "schedule":
            # hand off to entry point wrapper
            try:
                RunTaguchi.run_taguchi(
                    spec=args.spec,
                    design=args.design,
                    subset_size=args.subset_size,
                    add_center=args.add_center,
                    order=args.order,
                    out=args.out,
                    base_rng=args.base_rng,
                )
                sys.exit(0)
            except Exception as e:
                print(f"[ERROR] taguchi schedule failed: {e}")
                sys.exit(1)

    # fallback
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    # Dev shortcut (comment out in prod)
    spec = r"C:\00_MyDocuments\09_Veröffentlichungen\01_2025_SDF_Datasets\00_Vorversuche\taguchi_plan_1.csv"
    schedule = r"C:\00_MyDocuments\09_Veröffentlichungen\01_2025_SDF_Datasets\00_Vorversuche\taguchi_schedule_plan_1.csv"
    sys.argv = ["main.py", "taguchi", "schedule", "--spec", spec, "--add-center", "--out", schedule]
    main()
