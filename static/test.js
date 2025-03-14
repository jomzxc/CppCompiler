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
        runButton.textContent = 'Running...';
        
        // Send the code to the backend
        fetch('/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                output.textContent = `Error: ${data.error}`;
            } else {
                output.textContent = "✅ ok";
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
});