import sys
import unittest
from types import ModuleType
from unittest.mock import patch

from src.utils.module_exports import get_module_exports


class MockModule(ModuleType):

    def __init__(self, name, **kwargs):
        super().__init__(name)
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestModuleExporter(unittest.TestCase):

    def setUp(self):
        # Create mock modules
        self.mock_module1 = MockModule("mock_module1",
                                       public_var=1,
                                       public_func=lambda: None,
                                       _private_var=2,
                                       __private_func=lambda: None)

        self.mock_module2 = MockModule(
            "mock_module2",
            public_var=3,
            public_func=lambda: None,
            _private_var=4,
            __all__=['public_var', 'public_func', '_private_var'])

    def test_nonexistent_module(self):
        with self.assertRaises(ImportError):
            get_module_exports('nonexistent_module')

    @patch.dict(sys.modules, {'empty_module': MockModule("empty_module")})
    def test_empty_module(self):
        result = get_module_exports('empty_module', as_dict=True)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
