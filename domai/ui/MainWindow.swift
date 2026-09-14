import SwiftUI
import PythonKit

struct MainWindow: View {
    @State private var selectedProvider = "OpenAI"
    @State private var selectedModel = "gpt-4"
    @State private var userInput = ""
    @State private var securityResponse = ""
    @State private var educationalContent = ""

    let providers = ["OpenAI", "Google", "Mistral"]
    let models = [
        "OpenAI": ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
        "Google": ["gemini-pro", "gemini-pro-vision"],
        "Mistral": ["mistral-tiny", "mistral-small", "mistral-medium", "mistral-large-latest"]
    ]

    var body: some View {
        VStack {
            // Model Selection
            HStack {
                Text("Provider:")
                Picker("Provider", selection: $selectedProvider) {
                    ForEach(providers, id: \ .self) { provider in
                        Text(provider)
                    }
                }
                .pickerStyle(MenuPickerStyle())

                Text("Model:")
                Picker("Model", selection: $selectedModel) {
                    ForEach(models[selectedProvider] ?? [], id: \ .self) { model in
                        Text(model)
                    }
                }
                .pickerStyle(MenuPickerStyle())
            }
            .padding()

            // Response Area
            HStack {
                VStack {
                    Text("Security Response")
                        .font(.headline)
                    Text(securityResponse)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                }
                VStack {
                    Text("Learn More")
                        .font(.headline)
                    Text(educationalContent)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                }
            }
            .padding()

            // Input Area
            HStack {
                TextField("Ask me about MacOS security...", text: $userInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                Button("Send") {
                    processInput()
                }
                .padding()
            }
        }
        .frame(minWidth: 800, minHeight: 600)
        .background(Color.black.edgesIgnoringSafeArea(.all))
        .foregroundColor(.white)
    }

    func processInput() {
        let domai = Python.import("domai.main")
        let response = domai.DomAI().process_query(userInput)
        securityResponse = response[0]
        educationalContent = response[1]
    }
}

struct MainWindow_Previews: PreviewProvider {
    static var previews: some View {
        MainWindow()
    }
} 