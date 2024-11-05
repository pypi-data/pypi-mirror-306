import sys
import os
import pytest
import ast

# Add the directory containing commenter.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from commenter import CodeCommenter


# Test `from_string` method for empty and valid code strings
def test_from_string_empty():
    commenter = CodeCommenter()
    commenter.from_string("")
    assert commenter.code == ""
    assert isinstance(commenter.parsed_code, ast.Module)  # Expecting an empty AST module for empty input
    assert commenter.parsed_code.body == []  # Ensure the AST module is empty


def test_from_string_syntax_error():
    commenter = CodeCommenter()
    commenter.from_string("def function(:")
    assert commenter.parsed_code is None

def test_from_string_valid_code():
    commenter = CodeCommenter()
    commenter.from_string("def add(a, b): return a + b")
    assert commenter.code == "def add(a, b): return a + b"
    assert isinstance(commenter.parsed_code, ast.Module)

# Test `from_file` method with non-existent file
def test_from_file_not_found():
    commenter = CodeCommenter()
    commenter.from_file("non_existent_file.py")
    assert commenter.parsed_code is None

# Test `generate_docstrings` with simple function
def test_generate_docstrings_function():
    commenter = CodeCommenter()
    code = "def add(a, b): return a + b"
    commenter.from_string(code)
    docstrings = commenter.generate_docstrings()

    assert len(docstrings) == 1  # Expecting one docstring to be generated
    assert "add" in docstrings[0]  # Check for just the function name
    assert "Args" in docstrings[0]  # Checking if "Args" section is present
    assert "Returns" in docstrings[0]  # Checking if "Returns" section is present


# Test `_generate_function_docstring` for function description generation
def test_generate_function_docstring():
    commenter = CodeCommenter()
    func_node = ast.parse("def multiply(a, b): return a * b").body[0]
    docstring = commenter._generate_function_docstring(func_node)
    assert "multiply" in docstring
    assert "Args" in docstring
    assert "Example" in docstring
    assert "Returns" in docstring

# Test `_generate_class_docstring` with a simple class
def test_generate_class_docstring():
    commenter = CodeCommenter()
    code = """
    class Calculator:
        def add(self, a, b):
            return a + b
    """
    class_node = ast.parse(code).body[0]
    docstring = commenter._generate_class_docstring(class_node)
    assert "Calculator" in docstring
    assert "Attributes" in docstring
    assert "Methods" in docstring
    assert "add" in docstring

# Test `_infer_type` method with different node types
def test_infer_type():
    commenter = CodeCommenter()
    assert commenter._infer_type(ast.parse("123").body[0].value) == "int"
    assert commenter._infer_type(ast.parse("'text'").body[0].value) == "str"
    assert commenter._infer_type(ast.parse("[1, 2, 3]").body[0].value) == "list"
    assert commenter._infer_type(ast.parse("{}").body[0].value) == "dict"

# Test `generate_variable_descriptions` for variable description generation
def test_generate_variable_descriptions():
    commenter = CodeCommenter()
    code = "count = 0\nitems = []"
    commenter.from_string(code)
    variable_descriptions = commenter.generate_variable_descriptions()
    assert len(variable_descriptions) == 2
    assert "count" in variable_descriptions[0]
    assert "items" in variable_descriptions[1]

# if __name__ == "__main__":
#     pytest.main()



"""
CodeCommenter/
├──  myenvt/
├──  src/
├──  __init__.py
├──   commenter.py
├──   main.py
├──   templates.py
├──   utils.py
├──   docstring_generator.py
├──   users.py
├──   test_codecommenter.py
└── pyproject.toml  
└── README.md
└── LICENSE

"""
