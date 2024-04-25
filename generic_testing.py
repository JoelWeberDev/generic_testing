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
- Add run time option for the tests

"""
from pynput.keyboard import Key, Controller 
import time

class GenericTesting:
    def __doc__(self):
        """
        Generic Testing for all python functions. The class allows for any python function to be tested with any arguments and compared to an expected value
        or exception. The class also allows for keypresses to be spoofed during runtime. Each test passed to the class must be a list of test cases to be run.
        The expected value and exceptions must be passed in a dictionary with the key "err" or "expect" respectively. The kwargs parameter must also be a 
        dictionary with the key "kwargs" set to True.
        """
    def __init__(self):
        self.keyboard = Controller()    

    def run_tests(self, func, test_cases, print_args=False, print_res=False):
        failed_tests = []
        print(f"Running tests for {func.__name__}:\n")
        for i, test in enumerate(test_cases):
            assert isinstance(test, list), "Test cases must be a list of lists"

            print(f"  Running test {i+1}: {func.__name__}:")
            if print_args:
                print(f"  args: ({self._get_args_and_exception(test)[0]}) ->")

            res, failure = self._test_function(func, test)

            if failure is not None:
                print(f"    Test {i+1} failed with error: {failure}")
                failed_tests.append(i+1)
            else:
                print(f"    Test {i+1} passed")

            if print_res:
                print(f"    result: {res}")

            print()

        if len(failed_tests) == 0:
            print(f"Tests for {func.__name__} all passed\n")

        else:
            print(f"Tests for {func.__name__} failed on tests: {failed_tests}\n")

    def _test_function(self, func, args = []):
        """This is a formatting and testing function for any of the test cases below. 
        The inital function name and arguments are printed, The function is called within
        a try block and if an exception is raised and the expected exception (always the last argument)
        the the test passes. If the exception is not raised or the wrong exception is raised then the test fails.

        Args:
            func (python function): Function to be tested
            args (list): List of arguments with the last parameter as an expected exception
        """
        func_args, kwargs, expected_exception, expected_value, not_expect, raise_err = self._get_args_and_exception(args)

        res = None
        failure = None

        try:
            res = func(*func_args, **kwargs)
            if expected_exception is not None:
                failure = f"Expected exception {'any exception' if expected_exception == '_' else expected_exception} was not raised"
            elif expected_value is not None:
                if not self._compare_results(res, expected_value):
                    failure = f"Expected value {expected_value} but got {res}"
            elif not_expect is not None:
                if self._compare_results(res, not_expect):
                    failure = f"Did not expect {res} to equal {not_expect if not_expect != '_' else 'any value'}"

            if raise_err and failure is not None:
                raise Exception(failure)

        except Exception as e:
            if expected_exception is None:
                failure = f"Unexpected exception: {e}"

            elif expected_exception is not None and expected_exception != "_" and not isinstance(e, expected_exception):
                failure = f"Expected exception {expected_exception} but got {e}"

            if raise_err and failure is not None:
                raise e


        return res, failure

    def _compare_results(self, res, expected_value):
        """Compares the result of the function to the expected value

        Args:
            res (any): Result of the function
            expected_value (any): Expected value if there are multiple expected values an iterable of expected values can be passed in. If the string "_" is passed in the expected value it will not be compared.

        Returns:
            bool: True if the result is equal to the expected value
        """
        if type(expected_value) in [list, tuple] and type(res) in [list, tuple]:
            if len(expected_value) != len(res):
                return False

            for res_val, exp_val in zip(res, expected_value):
                if exp_val != "_" and res_val != exp_val:
                    return False

        else:
            if expected_value != "_" and res != expected_value:
                return False
        
        return True
            

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
        not_expect = None
        raise_err = False

        for arg in args:
            if isinstance(arg, dict) and "err" in arg:
                assert arg["err"] == "_" or issubclass(arg["err"], BaseException), "Expected exception must be a subclass of BaseException"
                err = arg["err"]


            elif isinstance(arg, dict) and "expect" in arg:
                expect = arg["expect"]

            elif isinstance(arg, dict) and "not_expect" in arg:
                not_expect = arg["not_expect"]

            elif isinstance(arg, dict) and "kwargs" in arg and arg["kwargs"] is True:
                kwargs_copy = arg.copy()
                del kwargs_copy["kwargs"]
                kwargs = kwargs_copy 

            else:
                new_args.append(arg)
            
            if isinstance(arg, dict) and "raise_err" in arg:
                assert isinstance(arg["raise_err"], bool), "raise_err must be a boolean"
                raise_err = arg["raise_err"]

        return new_args, kwargs, err, expect, not_expect, raise_err


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

    
    def _spoof_keypresses(self, keys, delay=0.1):
        """Enters a sequence of key presses into the system during runtime

        Args:
            keys (list): List of keys to be pressed
        """
        for key in keys:
            self._spoof_keypress(key)
            print(delay)
            time.sleep(delay)


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

        tests = [
            [["a", "k", "j"]],
            [["k", "j", "i", "k", "j"]],
            [["k", "j"]+list("k"*10)],
            [["k", "j"]+list("k"*10), {"kwargs": True, "delay": 1}],
            # [["a","k","j"]*100] # More fun in vim insert mode
        ]

        gt.run_tests(gt._spoof_keypresses, tests, print_args=True, print_res=False)
    
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

    # test_kwargs()

    def test_multiple_expected_values():
        def simple_func(a, b):
            return a, b, a+b

        tests = [
            [1, 1, { "expect": [1, 1, 2]}],
            [1, 1, { "expect": ["_", "_", 2]}],
            [1, 1, { "expect": ["_", 1, 3]}], # This test should fail
            [1, 1, { "expect": "_"}]
        ]

        gt.run_tests(simple_func, tests, print_args=True, print_res=True)

    # test_multiple_expected_values()

    def test_not_expect():
        def simple_func(a, b):
            return a, b, a+b

        tests = [
            [1, 1, { "not_expect": 3}],
            [1, 1, { "not_expect": 2}], 
            [1, 1, { "not_expect": (1, 1, "_")}], # This test should fail
            [1, 1, { "not_expect": (1, 1, 3)}], # This test should fail
            [1, 1, { "not_expect": (2, "_", 2)}], # This test should fail
        ]

        gt.run_tests(simple_func, tests, print_args=True, print_res=True)

    # test_not_expect()

    def test_any_exception():
        def simple_func(a, b):
            return a, b, a/b

        tests = [
            [1, 1, { "expect": "_"}],
            [1, "1", { "err": "_"}],
            [1, "1", { "err": TypeError}], 
            [1, 0, { "err": ZeroDivisionError}], 
            [1, 0, { "err": "_"}], 
        ]

        gt.run_tests(simple_func, tests, print_args=True, print_res=True)

    # test_any_exception()

    def test_raise_err():
        def simple_func(a, b):
            return a, b, a/b

        # When raise_err is true we expect the test to raise an exception and exit the execution
        tests = [
            [1, 1, { "expect": "_"}],
            [1, "1", { "err": "_", "raise_err": True}],
            [1, 0, { "err": TypeError, "raise_err": True}], # Will fail because expected exception is ZeroDivisionError
            [1, 0, { "err": ZeroDivisionError, "raise_err": True}], 
            [1, 0, { "err": "_", "raise_err": True}], 
        ]

        gt.run_tests(simple_func, tests, print_args=True, print_res=True)

    # test_raise_err()