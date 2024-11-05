from commenter import PyCodeCommenter

# Example functions for code_string input
code_string = """
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> None:
    print(f"Hello, {name}!")
"""

# Define the file path for file input
code_file = "C:\\Users\\DSN\\Desktop\\FileTransfer\\fake.py"

# Choose the input method: 'file' or 'string'
input_method = 'file'  # Set to 'string' if you want to use the string input

# Create an instance of CodeCommenter based on the chosen input method
if input_method == 'file':
    commenter = PyCodeCommenter().from_file(code_file)
elif input_method == 'string':
    commenter = PyCodeCommenter().from_string(code_string)
else:
    raise ValueError("Invalid input method. Choose either 'file' or 'string'.")

# Generate docstrings and print them
docstrings = commenter.generate_docstrings()
for comment in docstrings:
    print(comment)
