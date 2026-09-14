import SwiftUI
import PythonKit

@available(macOS 11.0, *)
struct MainAppWindow: View {
    @State private var showChatPanel = false
    @State private var selectedTab = 0
    @State private var testResult = "Click to test Python integration"
    
    func testPythonIntegration() {
        do {
            let sys = Python.import("sys")
            testResult = "Python version: \(sys.version_info.major).\(sys.version_info.minor)"
        } catch {
            testResult = "Error: \(error.localizedDescription)"
        }
    }
    
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("Test Section")) {
                    Button(action: testPythonIntegration) {
                        Text(testResult)
                    }
                }
                
                Section(header: Text("Security Status")) {
                    HStack {
                        Image(systemName: "shield.fill")
                            .foregroundColor(.green)
                        Text("System Protected")
                            .font(.headline)
                    }
                    .padding(.vertical, 5)
                }
                
                Section(header: Text("Quick Actions")) {
                    Button(action: { }) {
                        Label("Run Security Scan", systemImage: "magnifyingglass")
                    }
                    Button(action: { }) {
                        Label("Check Firewall Status", systemImage: "wifi.shield")
                    }
                    Button(action: { }) {
                        Label("View System Report", systemImage: "doc.text")
                    }
                }
                
                Section(header: Text("Recent Alerts")) {
                    ForEach(0..<3) { _ in
                        HStack {
                            Image(systemName: "exclamationmark.triangle")
                                .foregroundColor(.yellow)
                            Text("Security Update Available")
                        }
                    }
                }
            }
            .navigationTitle("DōmAI Security Assistant")
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button(action: { showChatPanel.toggle() }) {
                        Image(systemName: "message")
                    }
                }
            }
            
            // Default content view
            Text("Select an item from the sidebar")
                .font(.title)
                .foregroundColor(.secondary)
        }
        .frame(minWidth: 800, minHeight: 500)
    }
}