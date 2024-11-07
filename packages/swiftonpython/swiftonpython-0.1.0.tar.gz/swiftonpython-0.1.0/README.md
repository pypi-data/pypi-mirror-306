swiftonpython
swiftonpython là một thư viện Python giúp thực thi mã Swift từ Python, tích hợp linh hoạt để bạn có thể chạy mã Swift mà không cần biên dịch .so riêng biệt. Chỉ cần cài đặt và sử dụng ngay trong dự án Python.

Cài Đặt
Đảm bảo rằng bạn đã cài đặt Swift và có thể truy cập từ dòng lệnh.

Cài đặt thư viện từ PyPI:
Link github:
```bash
https://github.com/hqmdokkai/swiftonpython.git
```
```bash
pip install swiftonpython
```
Sử Dụng
Sau khi cài đặt, bạn chỉ cần import thư viện và thực thi mã Swift trực tiếp từ Python.

Ví dụ sử dụng:
```bash
import swiftonpython

# Mã Swift bạn muốn chạy
swift_code = """
print("Hello from Swift!")
"""

# Gọi hàm để thực thi mã Swift
swiftonpython.swiftonpython(swift_code)
```
Vậy là xong! Mã Swift sẽ được thực thi trực tiếp trong môi trường Python mà không cần phải cấu hình phức tạp.