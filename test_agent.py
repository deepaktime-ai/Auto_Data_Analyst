from agent import DataAgent

file_path = r"C:\Users\Dell\Desktop\Auto_Data_Analyst\diabetes.csv"

agent = DataAgent(file_path)

while True:
    query = input("\n💬 Ask your data question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    response = agent.run(query)
    print("\n🤖 Agent:", response)