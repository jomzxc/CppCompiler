from flask import Flask, render_template, request, jsonify
from lexer import lexer  # Importing the lexer
from parser import parser  # Importing the parser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/run_code', methods=['POST'])
def parse_code():
    code = request.json['code'].rstrip('\n')  # Remove trailing newlines
    
    try:
        # Reset the lexer state
        lexer.lineno = 1
        lexer.lexdata = ''
        lexer.input(code)

        # Tokenize the input code
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append({'type': tok.type, 'value': tok.value})

        # Parse the input code
        parsed = parser.parse(code, lexer=lexer)

        # Send the tokens and parsed result as 'output'
        output = {
            'tokens': tokens,
            'parsed': parsed
        }

        return jsonify({'output': output})

    except SyntaxError as e:
        # Adjust the line number if the error occurs on an empty line
        error_message = str(e)
        if "Unexpected identifier" in error_message and "line" in error_message:
            # Extract the reported line number
            reported_line = int(error_message.split("line ")[1].split(",")[0])
            # Count the number of empty lines before the error
            lines = code.split('\n')
            lines_before_error = 0
            for line in lines[:reported_line - 1]:
                lines_before_error += 1
            lines_before_error -= 1
            print(lines_before_error)
            # Adjust the line number
            reported_line -= lines_before_error
            # Update the error message
            error_message = error_message.replace(f"line {reported_line + lines_before_error}", f"line {reported_line}")
        error_message += "\n❌ invalid"
        return jsonify({'error': error_message})
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}\n❌ invalid"
        return jsonify({'error': error_message})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
