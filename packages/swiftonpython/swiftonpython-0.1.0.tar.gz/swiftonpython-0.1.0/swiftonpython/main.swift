import Foundation

@_exported import Swift

public class SwiftExecutor {
    public init() {}

    public func execute(code: String) {
        // Sử dụng đường dẫn tương đối cho tệp tạm
        let tempFilePath = "temp.swift"

        // Ghi mã Swift vào tệp
        do {
            try code.write(toFile: tempFilePath, atomically: true, encoding: .utf8)
        } catch {
            print("Không thể ghi vào tệp: \(error)")
            return
        }

        // Tạo Process để thực thi mã Swift
        let process = Process()
        // Chúng ta chỉ định executableURL là "swift" mà không cần đường dẫn
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = ["swift", tempFilePath] // Gọi swift từ env với tệp tạm

        do {
            try process.run() // Chạy quá trình
            process.waitUntilExit() // Chờ cho đến khi quá trình kết thúc
        } catch {
            print("Không thể chạy quá trình: \(error)")
        }

        // Xóa tệp tạm sau khi thực thi
        do {
            try FileManager.default.removeItem(atPath: tempFilePath)
        } catch {
            print("Không thể xóa tệp tạm: \(error)")
        }
    }
}

// Hàm khởi tạo cho Python
@_silgen_name("PyInit_swiftonpython")
public func PyInit_swiftonpython() -> UnsafeMutableRawPointer {
    return UnsafeMutableRawPointer(Unmanaged.passRetained(SwiftExecutor()).toOpaque())
}

// Hàm C để thực thi mã Swift
@_silgen_name("swiftonpython")
public func swiftonpython(code: UnsafePointer<CChar>) {
    let swiftCode = String(cString: code)
    let executor = SwiftExecutor()
    executor.execute(code: swiftCode)
}
