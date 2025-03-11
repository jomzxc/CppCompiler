# Interactive Code Parser

## Description

This project is a simple interactive code parser built using Python and the `ply` (Python Lex-Yacc) library. It parses code written in a basic C-like syntax and generates an Abstract Syntax Tree (AST) representation of the code.  The parser also includes robust syntax error reporting to help users identify issues in their code.

This project also includes a simple web-based frontend built with Flask, HTML, and JavaScript. This frontend provides a text box where users can input code, trigger the parser, and view the generated AST or any syntax error messages directly in their browser.

**Currently, the parser supports a subset of features, including:**

*   **Functions:** Function definitions with return types, names, parameters (with types), and function bodies (blocks).
*   **Parameters:** Function parameters with type and name.
*   **Blocks:** Code blocks enclosed in curly braces `{}`.
*   **Statements:**
    *   Declaration statements (with optional initialization).
    *   Expression statements (expressions followed by semicolons).
    *   Return statements.
    *   Block statements (nested blocks).
    *   For loops (`for` loops with initialization, condition, increment, and body).
    *   While loops (`while` loops with condition and body).
    *   If statements (`if` and `if-else` statements with conditions and blocks).
*   **Expressions:**
    *   Binary operations (`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`).
    *   Assignment (`=`).
    *   Function calls.
    *   Identifiers (variables).
    *   Number literals.
    *   Grouped expressions using parentheses `()`.
*   **Syntax Error Reporting:**  Provides informative syntax error messages including line number, column, and the unexpected token.

## Setup Instructions

**Prerequisites:**

*   **Python 3.x** installed on your system.
*   **pip** (Python package installer) - usually comes with Python installations.

**Installation:**

1.  **Clone or Download the Project:**  Obtain the project files (e.g., by cloning from a Git repository or downloading as a ZIP).
2.  **Navigate to the Project Directory:** Open a terminal or command prompt and navigate to the `your_project_directory` where you have saved the files.
3.  **Install Dependencies:** Install the required Python libraries using pip:

    ```bash
    pip install flask ply
    ```
    This command installs:
    *   `flask`:  The Flask web framework.
    *   `ply`:  Python Lex-Yacc, used for lexing and parsing.

## How to Run

1.  **Start the Flask Backend:** In your terminal, within the `your_project_directory`, run the Flask application:

    ```bash
    python app.py
    ```
    You should see output indicating that the Flask development server is running, typically on `http://127.0.0.1:5000/`.

2.  **Open the Frontend in a Browser:** Open your web browser and go to the address provided by Flask (usually `http://localhost:5000/index.html` or `http://127.0.0.1:5000/index.html`).

## How to Use

1.  **Enter Code:** In the web browser, you will see a text box labeled "Code Parser".  Type or paste code written in the supported C-like syntax into this text box.
2.  **Parse Code:** Click the "Parse Code" button below the text box.
3.  **View Output:** The "Parsed Output:" area below the button will display the result of parsing:
    *   **Successful Parse:** If the code is syntactically correct, the output area will show the Abstract Syntax Tree (AST) in JSON format. This represents the structure of your code as understood by the parser.
    *   **Syntax Error:** If the code contains syntax errors, the output area will display an error message. The message will include the line number, column number, and a description of the syntax error encountered.

## Further Development

This is a basic parser and frontend. Potential areas for future development include:

*   **Expanding Language Features:** Add support for more language constructs such as:
    *   More data types (e.g., `char`, `bool`, arrays, structs).
    *   Pointers.
    *   More complex control flow statements (`switch`, `do-while`).
    *   Function calls with more complex argument types.
    *   Input/Output operations.
*   **Semantic Analysis:** Implement semantic analysis to check for type errors, undeclared variables, etc., after parsing.
*   **Code Generation or Interpretation:**  Extend the project to generate machine code or interpret the AST to execute the parsed code.
*   **Improved Error Recovery:**  Enhance the parser's error handling to attempt to recover from errors and provide more comprehensive error reporting, potentially listing multiple errors in a single parse.
*   **Frontend Enhancements:**
    *   Syntax highlighting in the code editor.
    *   More user-friendly display of the AST (e.g., a tree visualization).
    *   Real-time error checking as the user types.
 
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Jomzxc