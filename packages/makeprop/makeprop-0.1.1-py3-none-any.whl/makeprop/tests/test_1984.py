import unittest

from makeprop.core import (
    makeprop,
)  # Replace with the actual module name where makeprop is defined


class TestMakeprop(unittest.TestCase):

    def test_default_var_name(self):
        # Test using default variable name with property
        class TestClass:
            @makeprop()
            def value(self, x):
                return x * 2

        obj = TestClass()
        obj.value = 5
        # Expected to be 5 * 2 = 10
        self.assertEqual(obj._value, 10)
        self.assertEqual(obj.value, 10)

    def test_custom_var_name(self):
        # Test using a custom variable name with property
        class TestClass:
            @makeprop("_custom_value")
            def value(self, x):
                return x + 1

        obj = TestClass()
        obj.value = 7
        # Expected to be 7 + 1 = 8
        self.assertEqual(obj._custom_value, 8)
        self.assertEqual(obj.value, 8)

    def test_callable_function_transformation(self):
        # Test transformation of values using callable function in property
        class TestClass:
            @makeprop()
            def value(self, x):
                return x**2

        obj = TestClass()
        obj.value = 4
        # Expected to be 4 ** 2 = 16
        self.assertEqual(obj._value, 16)
        self.assertEqual(obj.value, 16)

    def test_docstring_inheritance(self):
        # Test that the function docstring is inherited in the property
        class TestClass:
            @makeprop()
            def value(self, x):
                """Property to test docstring inheritance."""
                return x

        obj = TestClass()
        # Check if docstring is properly inherited
        self.assertEqual(
            obj.__class__.value.__doc__, "Property to test docstring inheritance."
        )

    def test_multiple_instances_independence(self):
        # Test independence of multiple instances of the same class
        class TestClass:
            @makeprop()
            def value(self, x):
                return x + 5

        obj1 = TestClass()
        obj2 = TestClass()

        obj1.value = 3  # Expected to be 3 + 5 = 8
        obj2.value = 7  # Expected to be 7 + 5 = 12

        self.assertEqual(obj1.value, 8)
        self.assertEqual(obj2.value, 12)

    def test_no_side_effect_on_non_makeprop_attributes(self):
        # Test that makeprop does not interfere with other attributes
        class TestClass:
            def __init__(self):
                self.regular_attr = 42

            @makeprop()
            def value(self, x):
                return x * 3

        obj = TestClass()
        obj.value = 2  # Expected to be 2 * 3 = 6

        # Ensure makeprop works and does not affect regular_attr
        self.assertEqual(obj.value, 6)
        self.assertEqual(obj.regular_attr, 42)

    def test_overwrite_existing_property(self):
        # Test overwriting an existing property using makeprop
        class TestClass:
            @property
            def value(self):
                return "This should be overwritten"

            @value.setter
            def value(self, val):
                pass  # Placeholder to avoid AttributeError

            @makeprop()
            def value(self, x):
                return x * 10

        obj = TestClass()
        obj.value = 5
        # Expected to be 5 * 10 = 50
        self.assertEqual(obj.value, 50)

    def test_attribute_error_on_unset_value(self):
        # Test AttributeError when accessing property without setting it
        class TestClass:
            @makeprop()
            def value(self, x):
                return x * 2

        obj = TestClass()
        with self.assertRaises(AttributeError):
            _ = obj.value

    def test_error_handling_with_invalid_type(self):
        # Test handling of invalid type input in the property setter
        class TestClass:
            @makeprop()
            def value(self, x):
                if not isinstance(x, int):
                    raise ValueError("Expected an integer")
                return x

        obj = TestClass()
        with self.assertRaises(ValueError):
            obj.value = "invalid_type"

    def test_reset_property(self):
        # Test resetting property to None and subsequent assignment
        class TestClass:
            @makeprop()
            def value(self, x):
                return x * 2

        obj = TestClass()
        obj.value = 3  # Expected to be 3 * 2 = 6
        self.assertEqual(obj.value, 6)

        # Resetting property
        del obj._value
        with self.assertRaises(AttributeError):
            _ = obj.value

    def test_property_removal(self):
        # Test if removing the private attribute raises AttributeError
        class TestClass:
            @makeprop()
            def value(self, x):
                return x + 10

        obj = TestClass()
        obj.value = 5
        self.assertEqual(obj.value, 15)

        # Deleting the private variable
        del obj._value
        with self.assertRaises(AttributeError):
            _ = obj.value


if __name__ == "__main__":
    unittest.main()
