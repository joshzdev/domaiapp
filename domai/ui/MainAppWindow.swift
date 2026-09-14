import SwiftUI
import PythonKit

struct MainAppWindow: View {
    @State private var selectedTab = 0
    @State private var showChatPanel = false

    var body: some View {
        NavigationView {
            TabView(selection: $selectedTab) {
                // General Overview
                GeneralOverviewView()
                    .tabItem {
                        Label("Overview", systemImage: "house")
                    }
                    .tag(0)

                // Network Module
                NetworkModuleView()
                    .tabItem {
                        Label("Network", systemImage: "network")
                    }
                    .tag(1)

                // Files Module
                FilesModuleView()
                    .tabItem {
                        Label("Files", systemImage: "doc")
                    }
                    .tag(2)

                // System Module
                SystemModuleView()
                    .tabItem {
                        Label("System", systemImage: "gear")
                    }
                    .tag(3)

                // Identity Module
                IdentityModuleView()
                    .tabItem {
                        Label("Identity", systemImage: "person")
                    }
                    .tag(4)
            }
            .navigationTitle("DōmAI Security Assistant")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showChatPanel.toggle() }) {
                        Image(systemName: "message")
                    }
                }
            }

            if showChatPanel {
                AIChatPanel()
                    .frame(minWidth: 300, idealWidth: 400, maxWidth: 500)
                    .transition(.move(edge: .trailing))
            }
        }
    }
}

struct NetworkModuleView: View {
    @State private var firewallStatus = ""
    @State private var firewallRules: [String] = []

    var body: some View {
        VStack {
            Text("Network Module")
                .font(.largeTitle)
                .padding()

            // Firewall Status
            Text("Firewall Status: \(firewallStatus)")
                .padding()

            // Firewall Rules
            List(firewallRules, id: \ .self) { rule in
                Text(rule)
            }

            Button("Refresh Firewall Status") {
                refreshFirewallStatus()
            }
            .padding()
        }
        .onAppear(perform: refreshFirewallStatus)
    }

    func refreshFirewallStatus() {
        do {
            let network = Python.import("modules.network.firewall")
            let manager = network.FirewallManager()
            let status = manager.get_status()
            firewallStatus = status["status"].description
            firewallRules = manager.get_rules().map { $0.description }
        } catch {
            firewallStatus = "Error fetching status"
            firewallRules = []
        }
    }
}

struct AIChatPanel: View {
    @State private var chatInput = ""
    @State private var chatHistory = ""

    var body: some View {
        VStack {
            Text("AI Chat")
                .font(.headline)
                .padding()

            ScrollView {
                Text(chatHistory)
                    .padding()
            }

            HStack {
                TextField("Type your message...", text: $chatInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                Button("Send") {
                    sendMessage()
                }
                .padding()
            }
        }
        .background(Color.gray.opacity(0.1))
    }

    func sendMessage() {
        do {
            let domai = Python.import("domai.main")
            let response = domai.DomAI().process_query(chatInput)
            chatHistory += "\nUser: \(chatInput)\nAI: \(response[0])"
            chatInput = ""
        } catch {
            chatHistory += "\nError processing query"
        }
    }
}

struct GeneralOverviewView: View {
    @State private var overallSecurityStatus = ""
    @State private var keyMetrics: [String] = []

    var body: some View {
        VStack {
            Text("General Security Overview")
                .font(.largeTitle)
                .padding()

            // Overall Security Status
            Text("Overall Security Status: \(overallSecurityStatus)")
                .padding()

            // Key Security Metrics
            List(keyMetrics, id: \ .self) { metric in
                Text(metric)
            }

            Button("Refresh Overview") {
                refreshOverview()
            }
            .padding()
        }
        .onAppear(perform: refreshOverview)
    }

    func refreshOverview() {
        do {
            // Example: Aggregate data from all modules
            overallSecurityStatus = "Secure"
            keyMetrics = [
                "Firewall: Enabled",
                "File Integrity: Intact",
                "Process Status: Normal",
                "User Accounts: Secure"
            ]
        } catch {
            overallSecurityStatus = "Error fetching overview"
            keyMetrics = []
        }
    }
}

struct FilesModuleView: View {
    @State private var integrityStatus = ""
    @State private var permissionsStatus = ""
    @State private var recentChanges: [String] = []
    @State private var storageUsage = ""

    var body: some View {
        VStack {
            Text("Files Module")
                .font(.largeTitle)
                .padding()

            // File Integrity Status
            Text("Integrity Status: \(integrityStatus)")
                .padding()

            // File Permissions Status
            Text("Permissions Status: \(permissionsStatus)")
                .padding()

            // Recent File Changes
            List(recentChanges, id: \ .self) { change in
                Text(change)
            }

            // Storage Usage
            Text("Storage Usage: \(storageUsage)")
                .padding()

            Button("Refresh File Status") {
                refreshFileStatus()
            }
            .padding()
        }
        .onAppear(perform: refreshFileStatus)
    }

    func refreshFileStatus() {
        do {
            let files = Python.import("modules.files")
            let integrityMonitor = files.IntegrityMonitor()
            let permissionsMonitor = files.PermissionsMonitor()
            let changeMonitor = files.ChangeMonitor()
            let storageMonitor = files.StorageMonitor()

            integrityStatus = integrityMonitor.get_status().description
            permissionsStatus = permissionsMonitor.get_status().description
            recentChanges = changeMonitor.get_recent_changes().map { $0.description }
            storageUsage = storageMonitor.get_usage().description
        } catch {
            integrityStatus = "Error fetching status"
            permissionsStatus = "Error fetching status"
            recentChanges = []
            storageUsage = "Error fetching usage"
        }
    }
}

struct SystemModuleView: View {
    @State private var processStatus = ""
    @State private var kernelStatus = ""
    @State private var hardwareStatus = ""
    @State private var serviceStatus = ""

    var body: some View {
        VStack {
            Text("System Module")
                .font(.largeTitle)
                .padding()

            // Process Status
            Text("Process Status: \(processStatus)")
                .padding()

            // Kernel Status
            Text("Kernel Status: \(kernelStatus)")
                .padding()

            // Hardware Status
            Text("Hardware Status: \(hardwareStatus)")
                .padding()

            // Service Status
            Text("Service Status: \(serviceStatus)")
                .padding()

            Button("Refresh System Status") {
                refreshSystemStatus()
            }
            .padding()
        }
        .onAppear(perform: refreshSystemStatus)
    }

    func refreshSystemStatus() {
        do {
            let system = Python.import("modules.system")
            let processMonitor = system.ProcessMonitor()
            let kernelMonitor = system.KernelMonitor()
            let hardwareMonitor = system.HardwareMonitor()
            let serviceMonitor = system.ServiceMonitor()

            processStatus = processMonitor.get_status().description
            kernelStatus = kernelMonitor.get_status().description
            hardwareStatus = hardwareMonitor.get_status().description
            serviceStatus = serviceMonitor.get_status().description
        } catch {
            processStatus = "Error fetching status"
            kernelStatus = "Error fetching status"
            hardwareStatus = "Error fetching status"
            serviceStatus = "Error fetching status"
        }
    }
}

struct IdentityModuleView: View {
    @State private var userStatus = ""
    @State private var permissionStatus = ""
    @State private var sessionStatus = ""
    @State private var accessStatus = ""

    var body: some View {
        VStack {
            Text("Identity Module")
                .font(.largeTitle)
                .padding()

            // User Status
            Text("User Status: \(userStatus)")
                .padding()

            // Permission Status
            Text("Permission Status: \(permissionStatus)")
                .padding()

            // Session Status
            Text("Session Status: \(sessionStatus)")
                .padding()

            // Access Status
            Text("Access Status: \(accessStatus)")
                .padding()

            Button("Refresh Identity Status") {
                refreshIdentityStatus()
            }
            .padding()
        }
        .onAppear(perform: refreshIdentityStatus)
    }

    func refreshIdentityStatus() {
        do {
            let identity = Python.import("modules.identity")
            let userManager = identity.UserManager()
            let permissionManager = identity.PermissionManager()
            let sessionMonitor = identity.SessionMonitor()
            let accessMonitor = identity.AccessMonitor()

            userStatus = userManager.get_status().description
            permissionStatus = permissionManager.get_status().description
            sessionStatus = sessionMonitor.get_status().description
            accessStatus = accessMonitor.get_status().description
        } catch {
            userStatus = "Error fetching status"
            permissionStatus = "Error fetching status"
            sessionStatus = "Error fetching status"
            accessStatus = "Error fetching status"
        }
    }
}

struct MainAppWindow_Previews: PreviewProvider {
    static var previews: some View {
        MainAppWindow()
    }
} 