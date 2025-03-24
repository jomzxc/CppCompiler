# Interactive Code Parser
---
## Description

This project is an interactive code parser with a web-based frontend, built using Python and the `ply` (Python Lex-Yacc) library for the backend, and Flask for serving the web application. The frontend is implemented using HTML and JavaScript, providing a user-friendly interface to write and parse code written in a basic C-like syntax. The backend performs lexical analysis, syntactic analysis (generating an Abstract Syntax Tree - AST), and semantic analysis, reporting any syntax or semantic errors found.

**Currently, the parser supports a subset of features, including:**

* Functions: Function definitions with return types, names, parameters (with types), and function bodies (blocks).
* Parameters: Function parameters with type and name.
* Blocks: Code blocks enclosed in curly braces `{}`.
* Statements:
    * Declaration statements (with optional initialization).
    * Expression statements (expressions followed by semicolons).
    * Return statements.
    * Block statements (nested blocks).
    * For loops (`for` loops with initialization, condition, increment, and body).
    * While loops (`while` loops with condition and body).
    * If statements (`if` and `if-else` statements with conditions and blocks).
    * Empty statements (`;`).
* Expressions:
    * Binary operations (`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`).
    * Logical operations (`&&`, `||`).
    * Assignment (`=`).
    * Function calls.
    * Identifiers (variables).
    * Number literals (integers, floats, doubles).
    * Character literals.
    * Boolean literals (`true`, `false`).
    * Grouped expressions using parentheses `()`.
* Syntax Error Reporting: Provides informative syntax error messages including line number, column, and the unexpected token.
* Semantic Analysis: Performs checks on the AST to ensure the code is semantically valid, including:
    * Type checking for declarations, assignments, and binary expressions.
    * Detection of undeclared variables.
    * Basic checks for function definitions (e.g., 'main' function parameters, return statements in non-void functions).
---
## Setup Instructions

**Prerequisites:**

* **Python 3.x** installed on your system.
* **pip** (Python package installer) - usually comes with Python installations.

**Installation:**

1.  **Clone or Download the Project:** Obtain the project files (e.g., by cloning from a Git repository or downloading as a ZIP).
2.  **Navigate to the Project Directory:** Open a terminal or command prompt and navigate to the `your_project_directory` where you have saved the files.
3.  **Install Dependencies:** The project dependencies are listed in the `requirements.txt` file. Install them using pip:

    ```bash
    pip install -r requirements.txt
    ```
    This command will install all the necessary libraries, including:
    * `flask`: The Flask web framework, used for the backend.
    * `ply`: Python Lex-Yacc, used for lexing and parsing.

## How to Run

1.  **Start the Flask Backend:** In your terminal, within the `your_project_directory`, run the Flask application:

    ```bash
    python app.py
    ```
    You should see output indicating that the Flask development server is running, typically on `http://127.0.0.1:5000/`.

2.  **Open the Frontend in a Browser:** Open your web browser and go to the address provided by Flask (usually `http://localhost:5000/index.html` or `http://127.0.0.1:5000/index.html`).
---
## How to Use

1.  **Enter Code:** In the web browser, you will see a text box labeled "Write your C++ code here...". Type or paste code written in the supported C-like syntax into this text box.
2.  **Compile & Run:** Click the "Compile & Run" button below the text box.
3.  **View Output:** The "Output will appear here..." area below the button will display the result of the parsing and semantic analysis:
    * **Successful Compilation:** If the code is syntactically and semantically correct, the output area will show a "✅ Compilation successful!" message, along with the number of tokens found and a "Semantic analysis: No errors found" message.
    * **Syntax Error:** If the code contains syntax errors, the output area will display an error message starting with "Error:" followed by the syntax error details (line number, column, and unexpected token).
    * **Semantic Error:** If the code is syntactically correct but contains semantic errors, the output area will display an error message starting with "Error:" followed by the semantic error details (e.g., type mismatch, undeclared variable).
---
## Further Development

Potential areas for future development include:

* **Expanding Language Features:** Add support for more language constructs such as:
    * More data types (e.g., arrays, structs, pointers).
    * More complex control flow statements (`switch`, `do-while`).
    * Function calls with more robust argument type checking.
    * Input/Output operations.
* **Improved Error Handling:** Enhance the parser's error recovery to attempt to continue parsing after encountering errors and provide more comprehensive error reporting, potentially listing multiple errors.
* **Abstract Syntax Tree Visualization:** Display the generated AST in a more visual and understandable format in the frontend.
* **Syntax Highlighting:** Add syntax highlighting to the code editor in the frontend to improve readability.
* **Real-time Error Checking:** Implement real-time error checking in the frontend as the user types code.
* **Code Generation or Interpretation:** Extend the project to generate an intermediate representation or directly interpret the AST to execute the parsed code.
---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---
## Team

* **Jomzxc**
* **Alatus-00**
* **Vernal-Equinox**
* **Yaps960**

---
Copyright (c) 2025
