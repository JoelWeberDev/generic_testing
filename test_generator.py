"""
Author: Joel Weber
Date: 15/04/2024
Description: Test generator for creating test cases for the generic_testing.py module. This allows for more comprehensive testing of a function

Notes:
- The expected value will not be able to be tested since the tests are ranomly generated.

TODO:
- Allow for ranges or list of options to be passed to the test generator
- Enable a hybrid where only certain arguments are randomly generated
- Test keyword arguments and default values (This is a permutation problem so beware of combinatorial explosion)
   - The kwargs and the args must be kept separate
- Create a data structure to contain and save all the tests
- Add class generation for the test cases
- Test the iterable creators
- Enable nested iterables
"""

import random
import numpy as np

class GenTests:

    ITERABLES = [list, tuple, dict, set, np.ndarray]

    @staticmethod
    def gen_int(arg):
        """Generates an integer test case

        Args:
            arg (dict): Dictionary of the argument
        """
        if "choices" in arg:
            return int(random.choice(arg["choices"]))

        elif "range" in arg:
            return random.randint(*arg["range"])

        else:
            raise AssertionError("Integers must have a range or a list of choices")

    @staticmethod
    def gen_float(arg):
        """Generates a float test case

        Args:
            arg (dict): Dictionary of the argument
        """
        if "choices" in arg:
            return float(random.choice(arg["choices"]))

        elif "range" in arg:
            return random.uniform(*arg["range"])

        else:
            raise AssertionError("Floats must have a range or a list of choices")
    
    @staticmethod
    def gen_str(arg):
        """Generates a string test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "characters" in arg, "Strings must have a character set"
        return "".join(random.choices(arg["characters"], k=10))
    
    @staticmethod
    def gen_list(arg):
        """Generates a list test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "size_range" in arg, "Lists must have a size range"
        assert "fill_type" in arg, "Lists must have a fill type"
        return [arg["fill_type"]["func"](arg["fill_type"]) for _ in range(random.randint(*arg["size_range"]))]
    
    @staticmethod
    def gen_tuple(arg):
        """Generates a tuple test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "size_range" in arg, "Tuples must have a size range"
        assert "fill_type" in arg, "Tuples must have a fill type"
        return tuple([arg["fill_type"]["func"](arg["fill_type"]) for _ in range(random.randint(*arg["size_range"]))])
    
    @staticmethod
    def gen_dict(arg):
        """Generates a dictionary test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "size_range" in arg, "Dictionaries must have a size range"
        assert "fill_type" in arg, "Dictionaries must have a fill type"
        assert "keys" in arg, "Dictionaries must have keys"
        return {key: arg["fill_type"]["func"](arg["fill_type"]) for key in arg["keys"]}
    
    @staticmethod
    def gen_set(arg):
        """Generates a set test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "size_range" in arg, "Sets must have a size range"
        assert "fill_type" in arg, "Sets must have a fill type"
        return {arg["fill_type"]["func"](arg["fill_type"]) for _ in range(random.randint(*arg["size_range"]))}
    
    @staticmethod
    def gen_bool(arg):
        """Generates a boolean test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "choices" in arg, "Booleans must have choices"
        return random.choice(arg["choices"])
    
    @staticmethod
    def gen_np_array(arg):
        """Generates a numpy array test case

        Args:
            arg (dict): Dictionary of the argument
        """
        assert "size_range" in arg, "Numpy arrays must have a size range"
        assert "fill_type" in arg, "Numpy arrays must have a fill type"
        assert "range" in arg, "Numpy arrays must have a range"
        return np.random.randint(*arg["range"], size=random.randint(*arg["size_range"]))


    # Dictionary of the argument types and their respective functions
    # Instead of range based value generation a tuple of values to be chosen from under the key "choices" can be passed
    ARG_TYPES = {
        int: {"func": gen_int, "range": (0, 100), "alt_types": [np.int_]},
        float: {"func": gen_float, "range": (0.0, 100.0), "alt_types": [int, np.int_, np.float_]},
        str: {"func": gen_str, "characters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"},
        list: {"func": gen_list, "size_range": (0, 100), "fill_type": int},
        tuple: {"func": gen_tuple, "size_range": (0, 100), "fill_type": int},
        dict: {"func": gen_dict, "size_range": (0, 100), "fill_type": int, "keys": ["a", "b", "c"]},
        set: {"func": gen_set, "size_range": (0, 100), "fill_type": int},
        bool: {"func": gen_bool, "choices": (True, False)},
        np.ndarray: {"func": gen_np_array, "size_range": (0, 100), "fill_type": int, "range": (-100, 100)},
    }


    @staticmethod
    def gen_cases(args, num_cases = 100, kwargs=None):
        """Parent class for the generation of the test cases

        Args:
            args (list): Must be a list of dictionaries. Each dictionary must contain the key "type" and can have optional keys "range" "size_range" 
            for iterables and "characters" for strings 
            num_cases (int, optional): Number of test cases to be generated. Defaults to 100.
            kwargs (list, optional): Under each argument key have a dictionary identical to the args dictionary. Defaults to None.
        
        Returns:
            list: List of test cases
        """
        final_args = []
        for arg in args:
            final_args.append(GenTests._set_args(arg))

        test_cases = []
        for _ in range(num_cases):
            test_case = []
            for arg in final_args:
                # Call the affiliated function to generate the test case
                test_case.append(arg["func"](arg))
                # test_case.append(1)

            test_cases.append(test_case)
    
        return test_cases

    @staticmethod
    def _gen_case(arg_dict):
        """Takes the args and generates a test case for them according to the type range and other optional arguments

        Args:
            args (list): See gen_cases for the format
        """

    @staticmethod
    def _set_args(arg_dict):
        """Sets the arguments for the test case

        Args:
            arg_dict (dict): Dictionary of the argument
        """
        GenTests._verify_arg(arg_dict, verify_kwargs = False)
        arg_type = arg_dict.get("type")
        arg = GenTests.ARG_TYPES[arg_type].copy()
        arg.update(arg_dict)


        if "choices" in arg and "range" in arg:
            del arg["range"]

        GenTests._verify_arg(arg, verify_kwargs = True)
        
        return arg

    @staticmethod
    def _verify_arg(arg, verify_kwargs = True):
        """Verifies that the argument is in the correct format

        Args:
            arg (dict): Dictionary of the argument
        """
        assert type(arg) == dict, "Argument must be a dictionary"
        assert "type" in arg, "Argument must have a type key"
        arg_type = arg.get("type")
        assert arg_type in GenTests.ARG_TYPES, f"Argument type {arg_type} is not supported"

        if verify_kwargs:
            for key in arg.keys():
                if key == "choices":
                    assert type(arg[key]) in [tuple, list], "Choices must be a list or tuple"
                    ft = arg.get("fill_type")
                    valid_types = [arg_type]
                    valid_types += arg.get("alt_types") or []
                    if ft is not None:
                        valid_types.append(ft)
                        valid_types += GenTests.ARG_TYPES[ft].get("alt_types") or []

                    # Note: This may need to be changed for nested iterables to work. At the moment it only works for single level iterables
                    assert all(type(v) in valid_types for v in arg[key]), "Choices must either match the argument type or the fill type"
                
                elif key == "fill_type":
                    assert arg[key] in GenTests.ARG_TYPES, f"{arg[key]} not in the argument types"

                elif key in GenTests.ARG_TYPES[arg_type]:
                    assert GenTests._compare_type(arg[key], GenTests.ARG_TYPES[arg_type][key], soft_compare = True), f"Argument key {key} is not of same type as {GenTests.ARG_TYPES[arg_type][key]}"
            

        return True


    @staticmethod
    def _compare_type(var1, var2, soft_compare = False):
        """Compares the type of two variables

        Args:
            var1 (any): First variable
            var2 (any): Second variable
        """
        if type(var1) != type(var2):
            return False
        
        elif type(var1) in GenTests.ITERABLES:
            return iterable_handler.compare(var1, var2, compare_type = True, compare_size = False, soft_compare = soft_compare)

        else:
            return True

    @staticmethod
    def _compare_size(var1, var2):
        """Compares the type of two variables

        Args:
            var1 (any): First variable
            var2 (any): Second variable
            soft_compare (bool, optional): If True then all iterables will be considered the same type. Defaults to False.
        """
        if type(var1) in GenTests.ITERABLES:
            return iterable_handler.compare(var1, var2, compare_type = False, compare_size = True, soft_compare = False)

        else:
            return True


class iterable_handler:    
    """
    A singular class to handle all types of iterables and make operations with them simpler
    """

    ITERABLES = [list, tuple, dict, set, np.ndarray]

    ITER_CONVERSIONS = {
        list: {
            tuple: lambda x: tuple(x),
            set: lambda x: set(x),
            np.ndarray: lambda x: np.array(x)
        },
        tuple: {
            list: lambda x: list(x),
            set: lambda x: set(x),
            np.ndarray: lambda x: np.array(x)
        },
        set: {
            list: lambda x: list(x),
            tuple: lambda x: tuple(x),
            np.ndarray: lambda x: np.array(list(x))
        },
        np.ndarray: {
            list: lambda x: x.tolist(),
            tuple: lambda x: tuple(x.tolist()),
            set: lambda x: set(x.tolist())
        }
    }

    SINGLE_CONVERSIONS = {
        int: {
            float: lambda x: float(x),
            np.int_: lambda x: np.int_(x),
            np.float_: lambda x: np.float_(x)
        },
        float: {
            int: lambda x: int(x),
            np.int_: lambda x: np.int_(x),
            np.float_: lambda x: np.float_(x)
        },
        np.int_: {
            int: lambda x: int(x),
            float: lambda x: float(x),
            np.float_: lambda x: np.float_(x)
        },
    }

    @staticmethod
    def length(iterable):
        if type(iterable) in [list, tuple, set]:
            return len(iterable)
        
        elif type(iterable) == dict:
            return len(iterable.keys())
        
        elif type(iterable) in [np.ndarray]:
            return iterable.shape[0]

        else:
            return 1

    @staticmethod
    def _find_conversion_iterable(iter1, iter2):
        """Between 2 variables it determines if there is a suitable conversion between them. The conversion function is returned if it exists

        Args:
            iter1 (any): variable 1
            iter2 (any): variable 2

        Returns:
            function: The conversion function. None if it does not exist
        """
        if type(iter1) == type(iter2):
            return lambda x: x

        if type(iter1) in iterable_handler.ITERABLES and type(iter2) in iterable_handler.ITERABLES:
            return iterable_handler.ITER_CONVERSIONS[type(iter1)].get(type(iter2))

        return None

    @staticmethod
    def _find_singleton_conv(v1, v2):
        if type(v1) == type(v2):
            return lambda x: x

        if type(v1) in iterable_handler.SINGLE_CONVERSIONS:
            return iterable_handler.SINGLE_CONVERSIONS[type(v1)].get(type(v2))

        return None

    @staticmethod
    def find_conversion(v1, v2):
        """Finds the conversion function between two variables

        Args:
            v1 (any): Variable 1
            v2 (any): Variable 2

        Returns:
            function: The conversion function. None if it does not exist
        """
        conv = iterable_handler._find_conversion_iterable(v1, v2)

        if conv is None:
            conv = iterable_handler._find_singleton_conv(v1, v2)

        return conv

    @staticmethod
    def compare(iterable1, iterable2, compare_type = True, compare_size = True, soft_compare = False):
        eq = True
        if compare_size:
            eq = iterable_handler.length(iterable1) == iterable_handler.length(iterable2)
        if compare_type:
            if not soft_compare:
                eq = eq and type(iterable1) == type(iterable2)
            else:
                eq = eq and (iterable_handler.find_conversion(iterable1, iterable2) is not None)


        if iterable_handler._is_iterable(iterable1) and iterable_handler._is_iterable(iterable2):
            for v1, v2 in zip(iterable1, iterable2):
                eq = eq and iterable_handler.compare(v1, v2, compare_type, compare_size, soft_compare=soft_compare)

        return eq    

    @staticmethod
    def _is_iterable(var):
        return type(var) in iterable_handler.ITERABLES

    @staticmethod
    def compare_size_type(var1, var2):
        return iterable_handler.compare(var1, var2, True, True)


if __name__ == "__main__":
    from generic_testing import GenericTesting
    gt = GenericTesting()

    def test_iterable_compare():
        tests = [
            [[1, 2, 3], [1, 2, 3], {"expect":True}],
            [[1, 2, 3], [1, 2, 3], {"kwargs":True, "compare_type": True, "compare_size": True}, {"expect":True}],
            [[1, 2, 3], [1, 2, 3, 4], {"expect":False}],
            [[1, 2, 3], [1, 2, 3, 4], {"kwargs":True, "compare_type": True, "compare_size": False}, {"expect":True}],
            [np.array([1, 2, 3]), np.array([1, 2, 3]), {"expect":True}],
            [np.array([1, 2, 3]), [1, 2, 3], {"kwargs":True, "compare_type": False, "compare_size": True}, {"expect":True}],
            [np.array([1, 2, 3]), [1, 2, 3], {"kwargs":True, "compare_type": True, "compare_size": True}, {"expect":False}],
            [(1,2,3), (1,2,3), {"expect":True}],
            [([1,2],3), ([1,2],3), {"expect":True}],
            [(np.array([1,2]),3), ([1,2],3), {"expect":False}],
            [{"a": 1, "b": 2}, {"a": 1, "b": 2}, {"expect":True}],
            [{"a": 1, "b": 2}, [1,2], {"kwargs":True, "compare_type": False, "compare_size": True}, {"expect":True}],
            [(1,2,3), [1,2], {"kwargs":True, "compare_type": True, "compare_size": False, "soft_compare":True}, {"expect":True}],
            [np.array([1,2,3]), [1,2], {"kwargs":True, "compare_type": True, "compare_size": False, "soft_compare":True}, {"expect":True}]  #  This currently fails because type np.int32 != int
        ]

        gt.run_tests(iterable_handler.compare, tests, print_args=True, print_res=True)

    # test_iterable_compare()

    def test_compare_type():
        tests = [
            [[1, 2, 3], [1, 2, 3], {"expect":True}],
            [[1, 2, 3], [1, 2, 3, 4], {"expect":True}],
            [np.array([1, 2, 3]), np.array([1, 2, 3]), {"expect":True}],
            [np.array([1, 2, 3]), [1, 2, 3], {"expect":False}],
            [(1,2,3), (1,2,3), {"expect":True}],
            [([1,2],3), ([1,2],3), {"expect":True}],
            [(np.array([1,2]),3), ([1,2],3), {"expect":False}],
            [{"a": 1, "b": 2}, {"a": 1, "b": 2}, {"expect":True}],
            [{"a": 1, "b": 2}, [1,2], {"expect":False}],
        ]

        gt.run_tests(GenTests._compare_type, tests, print_args=True, print_res=True)

    # test_compare_type()

    ### Args Testing ### 
    def test_verify_args():
        tests = [
            [{"type": int}, {"expect":True}],
            [{"type": int, "range": (0, 100)}, {"expect":True}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100)}, {"expect":True}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}, {"expect":True}],
            [{"range": (0, 100)}, {"err": AssertionError}],
            [{"type": int, "size_range": (0, 100)}, {"expect":True}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}, {"expect":True}],
            [{"type": bool, "choices": [True, False]}, {"expect":True}],
            [{"type": bool, "choices": [1, 2]}, {"err":AssertionError}],
            [{"type": list, "choices": [1, 2]}, {"err":AssertionError}],
            [{"type": list, "choices": [1, 2], "fill_type":int}, {"expect":True}],
        ]

        gt.run_tests(GenTests._verify_arg, tests, print_args=True, print_res=True)

    # test_verify_args()

    def test_set_args():
        tests = [
            [{"type": int}, {"expect":"_"}],
            [{"type": int, "range": (0, 100)}, {"expect":"_"}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100)}, {"expect":"_"}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}, {"expect":"_"}],
            [{"range": (0, 100)}, {"err": AssertionError}],
            [{"type": int, "size_range": (0, 100)}, {"expect":"_"}],
            [{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}, {"expect":"_"}],
            [{"type": bool, "choices": [True, False]}, {"expect":"_"}],
            [{"type": bool, "choices": [1, 2]}, {"err":AssertionError}],
            [{"type": list, "choices": [1, 2]}, {"expect":"_"}],
            [{"type": list, "choices": [1, 2], "fill_type":int}, {"expect":"_"}],
            [{"type": int, "choices": [1, 2.1], "fill_type":int}, {"err":AssertionError}],
        ]

        gt.run_tests(GenTests._set_args, tests, print_args=True, print_res=True)

    # test_set_args()

    def test_gen_cases():
        int_tests = [
            [[{"type": int}, {"type": int}],4, {"expect":"_"}],
            [[{"type": int, "choices":[1,2,3.1]}, {"type": int}],4, {"err":AssertionError}],
            [[{"type": int, "range": (0, 100)}, {"type": int, "range": (0, 100)}], 4, {"expect":"_"}],
            [[{"type": int, "choices": (0, 1, 3, 5, 7)}, {"type": int, "range": (0, 100)}], 4, {"expect":"_"}],
            [[{"type": int, "range": (0, 100), "size_range": (0, 100)}, {"type": int, "range": (0, 100), "size_range": (0, 100)}], 4, {"expect":"_"}],
            [[{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}, {"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}], 4, {"expect":"_"}],
            [[{"range": (0, 100)}, {"range": (0, 100)}], 4, {"err": AssertionError}],
            [[{"type": int, "size_range": (0, 100)}, {"type": int, "size_range": (0, 100)}], 4, {"expect":"_"}],
            [[{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}, {"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}], 4, {"expect":"_"}],
            # [[{"type": bool, "choices": [True, False]}, {"type": bool, "choices": [True, False]}], 4, {"expect":"_"}],
            # [[{"type": bool, "choices": [1, 2]}, {"type": bool, "choices": [1, 2]}], 4, {"err":AssertionError}],
            # [[{"type": list, "choices": [1, 2]}, {"type": list, "choices": [1, 2]}], 4, {"expect":"_"}],
            # [[{"type": list, "choices": [1, 2], "fill_type":int}, {"type": list, "choices": [1, 2], "fill_type":int}], 4, {"expect":"_"}],
        ]

        gt.run_tests(GenTests.gen_cases, int_tests, print_args=True, print_res=True)

        float_tests = [
            [[{"type": float}, {"type": float}],4, {"expect":"_"}],
            [[{"type": float, "choices": [1,1.1]}, {"type": float}],4, {"expect":"_"}],
            [[{"type": float, "range": (0, 1)}, {"type": float, "range": (0, 100)}], 4, {"expect":"_"}],
            [[{"type": float, "range": (0, 100), "size_range": (0, 100)}, {"type": int, "range": (0, 100), "size_range": (0, 100)}], 4, {"expect":"_"}],
            # [[{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}, {"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "12345678910"}], 4, {"expect":"_"}],
            # [[{"range": (0, 100)}, {"range": (0, 100)}], 4, {"err": AssertionError}],
            # [[{"type": int, "size_range": (0, 100)}, {"type": int, "size_range": (0, 100)}], 4, {"expect":"_"}],
            # [[{"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}, {"type": int, "range": (0, 100), "size_range": (0, 100), "characters": "qwerty"}], 4, {"expect":"_"}],
        ]

        gt.run_tests(GenTests.gen_cases, float_tests, print_args=True, print_res=True)


    test_gen_cases()


