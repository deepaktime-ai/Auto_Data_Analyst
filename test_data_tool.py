from data_tool import DataTool

# Replace with your CSV path
file_path = r"C:\Users\Dell\Desktop\Auto_Data_Analyst\diabetes.csv"

data_tool = DataTool(file_path)

print("\n📊 Shape:", data_tool.get_shape())
print("\n📌 Columns:", data_tool.get_columns())
print("\n📌 Data Types:", data_tool.get_dtypes())
print("\n📌 Preview:\n", data_tool.preview())
print("\n📌 Summary:\n", data_tool.summary())
print("\n📌 Missing Values:\n", data_tool.missing_values())
print("\n📌 Unique Values:\n", data_tool.unique_values())