import unittest
from typing import *

from setdoc.core import setdoc


class TestSetDocDecorator(unittest.TestCase):

    def test_setdoc_on_function(self):
        # Test the decorator on a standalone function
        @setdoc("This is a test function")
        def test_func():
            pass

        self.assertEqual(test_func.__doc__, "This is a test function")

    def test_setdoc_on_class(self):
        # Test the decorator on a class
        @setdoc("This is a test class")
        class TestClass:
            pass

        self.assertEqual(TestClass.__doc__, "This is a test class")

    def test_setdoc_on_class_method(self):
        # Test the decorator on a class method
        class MyClass:
            @setdoc("This is a test method")
            def my_method(self):
                pass

        instance = MyClass()
        self.assertEqual(instance.my_method.__doc__, "This is a test method")

    def test_setdoc_on_static_method(self):
        # Test the decorator on a static method
        class MyClass:
            @staticmethod
            @setdoc("This is a static method")
            def my_static_method():
                pass

        self.assertEqual(MyClass.my_static_method.__doc__, "This is a static method")

    def test_setdoc_on_class_with_init(self):
        # Test the decorator on a class that has an __init__ method
        @setdoc("This is a class with __init__")
        class InitClass:
            def __init__(self, x):
                self.x = x

        instance = InitClass(5)
        self.assertEqual(InitClass.__doc__, "This is a class with __init__")
        self.assertEqual(instance.__doc__, "This is a class with __init__")

    def test_setdoc_with_none_doc(self):
        # Test with None to see if it handles absence of documentation
        @setdoc(None)
        def none_doc_func():
            pass

        self.assertIsNone(none_doc_func.__doc__)

    def test_setdoc_on_class_property(self):
        # Test the decorator on a property
        class PropertyClass:
            def __init__(self, value):
                self._value = value

            @property
            @setdoc("This is a property")
            def value(self):
                return self._value

        instance = PropertyClass(10)
        self.assertEqual(PropertyClass.value.__doc__, "This is a property")
        self.assertEqual(instance.value, 10)

    def test_setdoc_on_classmethod(self):
        # Test the decorator on a class method
        class MyClass:
            @classmethod
            @setdoc("This is a class method")
            def my_class_method(cls):
                pass

        self.assertEqual(MyClass.my_class_method.__doc__, "This is a class method")

    def test_setdoc_on_nested_function(self):
        # Test the decorator on a nested function
        def outer_func():
            @setdoc("This is a nested function")
            def inner_func():
                pass

            return inner_func

        nested_func = outer_func()
        self.assertEqual(nested_func.__doc__, "This is a nested function")

    def test_setdoc_on_function_with_existing_doc(self):
        # Test if decorator replaces an existing docstring
        @setdoc("New docstring")
        def pre_doc_func():
            """Old docstring"""
            pass

        self.assertEqual(pre_doc_func.__doc__, "New docstring")


if __name__ == "__main__":
    unittest.main()
