from commenter import CodeCommenter

# Example code to be documented
code_string = """
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> None:
    print(f"Hello, {name}!")
"""

# Create a CodeCommenter instance and provide code
commenter = CodeCommenter()

# Use the from_string method
commenter.from_string(code_string)

# Generate docstrings
docstrings = commenter.generate_docstrings()

# Print the generated docstrings
for docstring in docstrings:
    print(docstring)
