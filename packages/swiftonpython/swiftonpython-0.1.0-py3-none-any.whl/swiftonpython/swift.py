import ctypes
import os

# Xác định đường dẫn thư viện
lib_path = os.path.join(os.path.dirname(__file__), 'swiftonpython.so')

# Tải thư viện Swift
swiftpython = ctypes.CDLL(lib_path)

# Khai báo hàm từ thư viện Swift
swiftpython.swiftonpython.argtypes = [ctypes.c_char_p]  # Đối số là chuỗi ký tự
swiftpython.swiftonpython.restype = None  # Hàm không trả về giá trị

def swift(code):
    # Mã hóa chuỗi thành UTF-8 và gọi hàm Swift
    swift_code = code.encode('utf-8')
    swiftpython.swiftonpython(swift_code)
