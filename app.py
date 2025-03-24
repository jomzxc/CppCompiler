from flask import Flask, render_template, request, jsonify
from lexer import lexer
from parser import parser  # Importing the parser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/run_code', methods=['POST'])
def parse_code():
    code = request.json['code']
    
    try:
        # Tokenize and parse the input code
        lexer.input(code)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append({'type': tok.type, 'value': tok.value})

        parsed = parser.parse(code)

        # Send the tokens and parsed result as 'output'
        output = {
            'tokens': tokens,
            'parsed': parsed
        }

        return jsonify({'output': output})

    except Exception as e:
        error_message = f"{str(e)}\n❌ invalid"
        return jsonify({'error': error_message})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
