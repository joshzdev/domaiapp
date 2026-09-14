import XCTest
import SwiftUI
@testable import domai

class MainWindowTests: XCTestCase {
    func testModelSelection() {
        let mainWindow = MainWindow()
        XCTAssertEqual(mainWindow.selectedProvider, "OpenAI")
        XCTAssertEqual(mainWindow.selectedModel, "gpt-4")

        mainWindow.selectedProvider = "Google"
        XCTAssertEqual(mainWindow.models[mainWindow.selectedProvider]?.first, "gemini-pro")
    }

    func testProcessInput() {
        let mainWindow = MainWindow()
        mainWindow.userInput = "Check firewall status"
        mainWindow.processInput()

        XCTAssertFalse(mainWindow.securityResponse.isEmpty)
        XCTAssertFalse(mainWindow.educationalContent.isEmpty)
    }

    func testUIComponents() {
        let mainWindow = MainWindow()
        let view = mainWindow.body

        XCTAssertNotNil(view)
        XCTAssertTrue(view is VStack)
    }
} 