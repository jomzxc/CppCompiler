from flask import Flask, render_template, request, jsonify
from lexer import lexer
from parser import parser, syntax_errors
from semantic import semantic_analyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def adjust_line_numbers(error_messages, code, lineCount, trailing_blank_lines):
    """Adjust line numbers in error messages to account for empty lines."""
    adjusted_messages = []
    code_lines = code.split('\n')
    actual_code_line_count = len(code_lines)

    # Calculate leading blank lines
    leading_blank_lines = 0
    for line in code_lines:
        if not line.strip():
            leading_blank_lines += 1
        else:
            break

    for error_message in error_messages:
        if "line" in error_message:
            try:
                # Extract the reported line number
                line_part = error_message.split("line ")[1]
                reported_line = int(line_part.split(",")[0] if "," in line_part else line_part.split(":")[0] if ":" in line_part else line_part.split(" ")[0])

                # Adjust the line number by adding the number of leading blank lines
                adjusted_line = reported_line + leading_blank_lines

                # Update the error message
                adjusted_message = error_message.replace(f"line {reported_line}", f"line {adjusted_line}")
                adjusted_messages.append(adjusted_message)
            except (IndexError, ValueError):
                # If we can't parse the line number, keep the original message
                adjusted_messages.append(error_message)
        else:
            # If there's no line number in the message, keep it as is
            adjusted_messages.append(error_message)

    return adjusted_messages

@app.route('/run_code', methods=['POST'])
def parse_code():
    code = request.json['code']
    line_count = request.json['lineCount']

    # Calculate the number of trailing blank lines
    trailing_blank_lines = 0
    temp_code = code
    while temp_code.endswith('\n'):
        trailing_blank_lines += 1
        temp_code = temp_code[:-1]

    code = code.rstrip('\n')

    try:
        # Reset the lexer state and syntax errors
        lexer.lineno = 1
        lexer.lexdata = ''
        lexer.input(code)

        # Clear any previous syntax errors
        global syntax_errors
        syntax_errors.clear() if hasattr(syntax_errors, 'clear') else None

        # Tokenize the input code
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append({'type': tok.type, 'value': tok.value})

        # Parse the input code
        parsed = parser.parse(code, lexer=lexer)

        # Check for syntax errors
        if syntax_errors and len(syntax_errors) > 0:
            adjusted_syntax_errors = adjust_line_numbers(syntax_errors, code, line_count, trailing_blank_lines)
            return jsonify({'error': '\n'.join(adjusted_syntax_errors) + "\n❌ invalid"})

        # Perform semantic analysis if parsing was successful
        if parsed:
            semantic_errors = semantic_analyzer(parsed)
            if semantic_errors and len(semantic_errors) > 0:
                adjusted_semantic_errors = adjust_line_numbers(semantic_errors, code, line_count, trailing_blank_lines)
                return jsonify({'error': '\n'.join(adjusted_semantic_errors) + "\n❌ invalid"})

        # Send the tokens and parsed result as 'output'
        output = {
            'tokens': tokens,
            'parsed': "Valid program"  # You might want to serialize the AST here
        }

        return jsonify({'output': output})

    except Exception as e:
        error_message = f"Unexpected error: {str(e)}\n❌ invalid"
        return jsonify({'error': error_message})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)