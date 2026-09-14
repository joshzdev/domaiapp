// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "DomaiApp",
    platforms: [
        .macOS(.v11)
    ],
    products: [
        .executable(name: "DomaiApp", targets: ["DomaiApp"]),
    ],
    dependencies: [
        .package(url: "https://github.com/pvieito/PythonKit.git", from: "0.3.1")
    ],
    targets: [
        .executableTarget(
            name: "DomaiApp",
            dependencies: ["PythonKit"]
        )
    ]
) 