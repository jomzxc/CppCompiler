document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    const runButton = document.getElementById('run-button');
    const output = document.getElementById('output');

    // Initialize line numbers
    updateLineNumbers();

    // Update line numbers when text changes
    codeEditor.addEventListener('input', updateLineNumbers);

    // Update line numbers when scrolling to keep them in sync
    codeEditor.addEventListener('scroll', function() {
        lineNumbers.scrollTop = codeEditor.scrollTop;
    });

    function updateLineNumbers() {
        const lines = codeEditor.value.split('\n');
        const lineCount = lines.length;

        let lineNumbersHTML = '';
        for (let i = 1; i <= lineCount; i++) {
            lineNumbersHTML += '<p>' + i + '</p>';
        }

        lineNumbers.innerHTML = lineNumbersHTML;
    }

    runButton.addEventListener('click', function() {
        runCode();
    });

    function runCode() {
        const code = codeEditor.value;
        output.textContent = '';
        runButton.disabled = true;
        runButton.innerHTML = 'Running...';
        const lines = codeEditor.value.split('\n');
        const lineCount = lines.length;

        // Send the code to the backend
        fetch('/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                lineCount: lineCount
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                output.textContent = `Error: ${data.error}`;
                // Keep the existing styling for errors
            } else {
                // Display successful compilation result
                let resultText = "✅ Compilation successful!";

                // If you want to display tokens or AST information
                if (data.output && data.output.tokens) {
                    const tokenCount = data.output.tokens.length;
                    resultText += `\n\nTokens found: ${tokenCount}`;

                    // Add semantic analysis success message
                    resultText += "\n\nSemantic analysis: No errors found";
                }

                output.textContent = resultText;
            }
        })
        .catch(error => {
            output.textContent = `Error: ${error.message}`;
        })
        .finally(() => {
            runButton.disabled = false;
            runButton.innerHTML = '<span class="play-icon"></span>Compile & Run';
        });
    }

    // Add keyboard shortcut (Ctrl+Enter or Cmd+Enter) to run code
    codeEditor.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            runCode();
        }
    });
    codeEditor.addEventListener('keydown', function(event) {
        if (event.key === 'Tab') {
            event.preventDefault(); // Prevent focus change
    
            const start = this.selectionStart;
            const end = this.selectionEnd;
    
            // Insert tab at the current cursor position
            this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
    
            // Move the cursor to be after the inserted tab
            this.selectionStart = this.selectionEnd = start + 1;
        }
    });
});