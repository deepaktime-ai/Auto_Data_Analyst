import requests

class OllamaLLM:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt, temperature=0.7):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            
            elif response.status_code != 200:
             return f"❌ LLM Error: {response.text}"
            
            else:
                return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"LLM Connection Error: {str(e)}"


# -------------------------------
# TEST FUNCTION (IMPORTANT)
# -------------------------------
if __name__ == "__main__":
    llm = OllamaLLM()

    prompt = "Explain what is mean in statistics in simple terms."
    output = llm.generate(prompt)

    print("\n🧠 LLM Response:\n")
    print(output)