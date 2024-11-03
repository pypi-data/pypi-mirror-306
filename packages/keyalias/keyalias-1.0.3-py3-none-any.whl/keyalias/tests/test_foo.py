import unittest

from keyalias import keyalias


class TestFoo(unittest.TestCase):
    def test_foo(self):
        @keyalias(bar=6)
        class Foo:
            def __init__(self):
                self.data = list(range(10))  # Example list with 10 elements

            def __getitem__(self, index):
                return self.data[index]

            def __setitem__(self, index, value):
                self.data[index] = value

            def __delitem__(self, index):
                del self.data[index]

        # Create an instance of Foo
        my_instance = Foo()

        # Use the alias property to access index 6
        self.assertEqual(my_instance.bar, 6)  # Get the value at index 6
        my_instance.bar = 42  # Set the value at index 6
        self.assertEqual(my_instance.bar, 42)  # Check the updated value at index 6
        del my_instance.bar  # Delete the value at index 6
        self.assertEqual(my_instance.bar, 7)  # Check the updated value at index 6


if __name__ == "__main__":
    unittest.main()
