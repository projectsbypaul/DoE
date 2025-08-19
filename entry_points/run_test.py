import testing.testing
from testing.testing import echo_test_msg

class RunTest:
    @staticmethod
    def run_test(test_msg : str):
        echo_test_msg(test_msg)
        return 0


def main():
    pass

if __name__ == "__main__":
    main()