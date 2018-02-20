import ctypes, psutil
from typing import Callable

# DLLs needed
kernel32 = ctypes.windll.kernel32

# Permissions
PROCESS_VM_OPERATION = 0x0008
PROCESS_SET_INFORMATION = 0x0200
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

# this is the final permission that we need:
PERMISSION = (
        PROCESS_VM_OPERATION |
        PROCESS_SET_INFORMATION |
        PROCESS_VM_READ |
        PROCESS_VM_WRITE
)

# Windows API functions
open_process: Callable = kernel32.OpenProcess
close_handle: Callable = kernel32.CloseHandle
get_last_error: Callable = kernel32.GetLastError
read_process_memory: Callable = kernel32.ReadProcessMemory
write_process_memory: Callable = kernel32.WriteProcessMemory

class PyMem:
    def open_process(self, process_name: str):
        processes = (proc for proc in psutil.process_iter() if proc.name() == process_name)
        process = next(processes, None)

        if process is None:
            print(f'No such process: {process_name}')
            return None

        return open_process(
            PERMISSION,
            False,
            process.pid,
        )

    def _close_handle(self, process):
        close_handle(h_process)

    def _get_last_error(self):
        return get_last_error()

    def pointer_offset(self, base_address):
        pass

    def read_process_memory(self, process, base_address):
        try:
            buffer = ctypes.c_uint()
            buffer_pointer = ctypes.byref(buffer)
            size = ctypes.sizeof(buffer)
            number_of_bytes_read = ctypes.c_ulong(0)

            read_process_memory(
                process,
                base_address,
                buffer_pointer,
                size,
                number_of_bytes_read
            )
            return buffer
        except Exception as e:
            print(e)
            print('\windows response:\n', get_last_error())
            close_handle(process)
            raise e

    def write_process_memory(self, process, base_address, value: int):
        try:
            buffer = ctypes.c_uint(value)
            buffer_pointer = ctypes.byref(buffer)
            buffer_size = ctypes.sizeof(buffer)
            number_of_bytes_written = ctypes.c_ulong(0)

            write_process_memory(
                process,
                base_address,
                buffer_pointer,
                buffer_size,
                number_of_bytes_written
            )

        except Exception as e:
            close_handle(process)
            print(e)
            print('[writing] Windows response:\n', get_last_error())
            raise e


if __name__ == '__main__':
    pymem = PyMem()
