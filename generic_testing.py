"""
Author: Joel Weber
Date: 06/04/2024
Desciption: Generic unit testing for a variety of functions

Notes:
- At the moment this does not allow for keyword arguments to be passed to the function
- The tests must be a list of lists and the last argument may be an expected exception, but does not have to be

TODO:
- Add support for keyword arguments
- Add support for multiple expected exceptions (can be done by passing a tuple or list to the expected value)
- Clear error messages for the expected value

"""
from pynput.keyboard import Key, Controller 

class GenericTesting:
    def __init__(self):
        self.keyboard = Controller()    

    def run_tests(self, func, test_cases, print_args=False, print_res=False):
        print(f"Running tests for {func.__name__}:")
        for i, test in enumerate(test_cases):
            assert isinstance(test, list), "Test cases must be a list of lists"

            print(f"  Running test {i+1}: {func.__name__}:")
            if print_args:
                print(f"  args: ({self._get_args_and_exception(test)[0]}) ->")

            res, failure = self._test_function(func, test)

            if failure is not None:
                print(f"    Test {i+1} failed with error: {failure}")
            else:
                print(f"    Test {i+1} passed")

            if print_res:
                print(res)


        print(f"Tests for {func.__name__} complete\n")

    def _test_function(self, func, args = []):
        """This is a formatting and testing function for any of the test cases below. 
        The inital function name and arguments are printed, The function is called within
        a try block and if an exception is raised and the expected exception (always the last argument)
        the the test passes. If the exception is not raised or the wrong exception is raised then the test fails.

        Args:
            func (python function): Function to be tested
            args (list): List of arguments with the last parameter as an expected exception
        """
        func_args, expected_exception, expected_value = self._get_args_and_exception(args)

        res = None
        failure = None

        try:
            res = func(*func_args)
            if expected_exception is not None:
                failure = f"Expected exception {expected_exception} was not raised"
            elif expected_value is not None and res != expected_value:
                failure = f"Expected value {expected_value} but got {res}"

        except Exception as e:
            if expected_exception is None:
                failure = f"Unexpected exception: {e}"

            elif expected_exception is not None and not isinstance(e, expected_exception):
                failure = f"Expected exception {expected_exception} but got {e}"

        return res, failure

    def _get_args_and_exception(self, args):
        """Besided the arguments for the function the test cases may have an exception or expected value. This function separates the arguments from the exprected values

        Args:
            args (list): List of arguments for the function if there is and expected exception it will be in a dictionary with either the key "err" or "expect" 

        Returns:
            list: List of arguments for the function
            type: Expected error 
            any value: Expected value
        """
        if len(args) > 0 and isinstance(args[-1], dict):
            if "err" in args[-1]:
                assert issubclass(args[-1]["err"], BaseException), "Expected exception must be a subclass of BaseException"
                return args[:-1], args[-1]["err"], None
            elif "expect" in args[-1]:
                return args[:-1], None, args[-1]["expect"]

        return args, None, None
    

    def _spoof_keypress(self, key):
        """Enters a key press into the system during runtime

        Args:
            key (str): Single key to be pressed
        """
        self.keyboard.press(key)
        self.keyboard.release(key)

    
    def _spoof_keypresses(self, keys):
        """Enters a sequence of key presses into the system during runtime

        Args:
            keys (list): List of keys to be pressed
        """
        for key in keys:
            self._spoof_keypress(key)


if __name__ == "__main__":
    gt = GenericTesting()

    ### Testing with simple division function ###
    def test_simple_func():
        def divide(a, b):
            return a / b
        
        tests = [
            [1, 1],
            [1, 0, {"err": ZeroDivisionError} ],
            [1, "a", {"err": TypeError}],
            [10, 5, {"expect": 2}],
            [11, 5, {"expect": 3}], # This test should fail
        ]

        gt.run_tests(divide, tests, print_args=True, print_res=True)

    # test_simple_func()

    ### Testing with keypress spoofing ###
    def test_keypresses():
        # Note: This will put characters wherever your cursor is. You have been warned.
        def keypresses(keys):
            gt._spoof_keypresses(keys)

        tests = [
            [["a"]],
            [["a", "b"]],
            [["a", "b", "c"]],
            [["a", "b", "c", "d"]],
            [["a", "b", "c", "d", "e"]],
            # [["a","k","j"]*100] # More fun in vim insert mode
        ]

        gt.run_tests(keypresses, tests, print_args=True, print_res=False)
    
    # test_keypresses()
