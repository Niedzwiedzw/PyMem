from unittest import TestCase
from unittest import main as run_tests
from pymem import PyMem


PROCESS_NAME = 'gamehacking.exe'
TARGET_VARIABLE_ADDRESS = 0x38BEBFF748

class TestCanReadMemory(TestCase):
    def setUp(self):
        self.pymem = PyMem()

    def test_basic_setup(self):
        self.assertIsNotNone(self.pymem)

    def test_process_can_be_found(self):
        self.assertIsNotNone(self.pymem.open_process(PROCESS_NAME))

    def test_can_read_memory(self):
        process = self.pymem.open_process(PROCESS_NAME)
        value = self.pymem.read_process_memory(
            process,
            TARGET_VARIABLE_ADDRESS
        )
        print(value)


if __name__ == '__main__':
    run_tests()
