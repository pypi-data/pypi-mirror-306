from commenter import CodeCommenter

# Example functions for string input
code_string = """
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> None:
    print(f"Hello, {name}!")
"""

# Define the file path for file input
code_file = "C:\\Users\\DSN\\Desktop\\FileTransfer\\fake.py"

# Create an instance of CodeCommenter based on your preferred input method
# Uncomment one of the lines below based on your input choice:

# For file input:
commenter = CodeCommenter().from_file(code_file)

# For string input:
# commenter = CodeCommenter().from_string(code_string)

# Generate docstrings
docstrings = commenter.generate_docstrings()

# Print the generated docstrings
for comment in docstrings:
    print(comment)

# Save docstrings to a file
output_file = "C:\\Users\\DSN\\Desktop\\FileTransfer\\docstrings.txt"
with open(output_file, 'w') as f:
    for comment in docstrings:
        f.write(comment + "\n\n")  # Add double newlines for separation

"""

PyCodeCommenter/
├── myenvt/                   # This is your virtual environment; it's not needed in your package structure
├── src/                      # Source directory for your code
│   ├── PyCodeCommenter/      # This should be the package name (change the folder name)
│   │   ├── __init__.py       # Can be empty, but must be present
│   │   ├── main.py           # Your main entry point (if applicable)
│   │   └── commenter.py       # Your library code
├── setup.py                  # Your setup script
├── LICENSE                   # License file
└── README.md                 # ReadMe file


"""