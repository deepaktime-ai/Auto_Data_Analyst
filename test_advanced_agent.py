from advanced_agent import AdvancedDataAgent

file_path = r"C:\Users\Dell\Desktop\Auto_Data_Analyst\diabetes.csv"

agent = AdvancedDataAgent(file_path)

while True:
    query = input("\n💬 Ask complex question (type 'exit'): ")

    if query.lower() == "exit":
        break

    response = agent.run(query)

    print("\n🤖 Agent:", response)