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
├──build/
    ├──bdist.win-amd64/
    ├──lib/
        ├──PyCodeCommenter
            ├── __init__.py
├──dist/
    ├── PyCodeCommenter-0.0.3-py3-none-any.whl
├── myenvt/                   
├── src/                      
│   ├── PyCodeCommenter/     
│   │   ├── __init__.py       
│   │   ├── main.py           
│   │   └── commenter.py       
├── setup.py                  
├── LICENSE                   
└── README.md                 


"""

