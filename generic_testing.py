"""
Author: Joel Weber
Date: 06/04/2024
Desciption: Generic unit testing for a variety of functions

Notes:
- At the moment this does not allow for keyword arguments to be passed to the function
- The tests must be a list of lists and the last argument may be an expected exception, but does not have to be

TODO:
- Add support for keyword arguments
- Test generator for creating test cases 

"""
from pynput.keyboard import Key, Controller 

class GenericTesting:
    def __init__(self):
        self.keyboard = Controller()    

    def run_tests(self, func, test_cases, print_args=False, print_res=False):
        print(f"Running tests for {func.__name__}:\n")
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
                print(f"    result: {res}")

            print()


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
        func_args, kwargs, expected_exception, expected_value = self._get_args_and_exception(args)

        res = None
        failure = None

        try:
            res = func(*func_args, **kwargs)
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
        kwargs = {}
        new_args = []
        err = None
        expect = None

        for arg in args:
            if isinstance(arg, dict) and "err" in arg:
                assert issubclass(arg["err"], BaseException), "Expected exception must be a subclass of BaseException"
                err = arg["err"]

            elif isinstance(arg, dict) and "expect" in arg:
                expect = arg["expect"]

            elif isinstance(arg, dict) and "kwargs" in arg and arg["kwargs"] is True:
                kwargs_copy = arg.copy()
                del kwargs_copy["kwargs"]
                kwargs = kwargs_copy 

            else:
                new_args.append(arg)

        return new_args, kwargs, err, expect


    def get_kwargs(self, args):
        """This function is used to extract the keyword arguments from the test cases

        Args:
            args (list): List of arguments for the function

        Returns:
            dict: Dictionary of keyword arguments
        """
        arg_dict = {"args": [], "kwargs": {}}
        for arg in args:
            if isinstance(arg, dict) and "kwargs" in arg and arg["kwargs"] is True:
                arg_dict["kwargs"] = arg

            else:
                arg_dict["args"].append(arg)    
        return arg_dict



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
            [1, 0, { "err": ZeroDivisionError}],
            [1, "a", { "err": TypeError}],
            [10, 5, { "expect": 2}],
            [11, 5, { "expect": 3}], # This test should fail
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

    def test_kwargs():
        def simple_func(a, b, **kwargs):
            return a + b, kwargs

        tests = [
            [1, 1],
            [1, 1, { "expect": (2, {})}],
            [1, 1, {"kwargs":True, "c": 3, "d": 4}, { "expect": (2, {"c": 3, "d": 4})}],
            [1, 1, {"kwargs":True, "c": 3, "d": 4}, { "expect": (2, {"c": 3})}], # This test should fail
        ]

        gt.run_tests(simple_func, tests, print_args=True, print_res=True)

    test_kwargs()