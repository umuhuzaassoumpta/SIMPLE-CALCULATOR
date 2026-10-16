import os
import tempfile
import webbrowser


def generate_calculator_html():
  """Generates a simple interactive HTML/JS calculator string."""
  return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Python Browser Calculator</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f0f2f5;
        }
        .calculator {
            background: #ffffff;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 260px;
        }
        #display {
            width: 100%;
            height: 50px;
            margin-bottom: 15px;
            font-size: 1.5rem;
            text-align: right;
            padding: 8px 12px;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }
        button {
            height: 50px;
            font-size: 1.1rem;
            border: none;
            border-radius: 8px;
            background: #f8f9fa;
            cursor: pointer;
            transition: background 0.1s;
        }
        button:hover { background: #e2e6ea; }
        .operator { background: #e7f5ff; color: #1c7ed6; font-weight: bold; }
        .operator:hover { background: #d0ebff; }
        .equals { background: #228be6; color: white; grid-column: span 2; }
        .equals:hover { background: #1c7ed6; }
        .clear { background: #ffe3e3; color: #c92a2a; }
        .clear:hover { background: #ffa8a8; }
    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" disabled value="0">
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button onclick="appendValue('(')">(</button>
            <button onclick="appendValue(')')">)</button>
            <button class="operator" onclick="appendValue('/')">÷</button>
            
            <button onclick="appendValue('7')">7</button>
            <button onclick="appendValue('8')">8</button>
            <button onclick="appendValue('9')">9</button>
            <button class="operator" onclick="appendValue('*')">×</button>
            
            <button onclick="appendValue('4')">4</button>
            <button onclick="appendValue('5')">5</button>
            <button onclick="appendValue('6')">6</button>
            <button class="operator" onclick="appendValue('-')">−</button>
            
            <button onclick="appendValue('1')">1</button>
            <button onclick="appendValue('2')">2</button>
            <button onclick="appendValue('3')">3</button>
            <button class="operator" onclick="appendValue('+')">+</button>
            
            <button onclick="appendValue('0')">0</button>
            <button onclick="appendValue('.')">.</button>
            <button class="equals" onclick="calculateResult()">=</button>
        </div>
    </div>

    <script>
        const display = document.getElementById('display');
        let resetNext = false;

        function appendValue(val) {
            if (display.value === '0' || display.value === 'Error' || resetNext) {
                if (['+', '*', '/', ')'].includes(val) && !resetNext && display.value !== 'Error') {
                    // allow continuing if operator pressed after result
                } else {
                    display.value = '';
                }
                resetNext = false;
            }
            display.value += val;
        }

        function clearDisplay() {
            display.value = '0';
            resetNext = false;
        }

        function calculateResult() {
            try {
                // Replace visual symbols with JS operators
                let expression = display.value.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
                // Basic safety check for allowed characters
                if (/[^0-9+\-*/().\s]/.test(expression)) throw new Error("Invalid");
                let result = Function('"use strict"; return (' + expression + ')')();
                display.value = Number.isFinite(result) ? Number(result.toFixed(8)) : 'Error';
            } catch (e) {
                display.value = 'Error';
            }
            resetNext = true;
        }
    </script>
</body>
</html>
"""


def open_calculator_in_browser():
  # Create a temporary HTML file
  fd, path = tempfile.mkstemp(suffix=".html", prefix="python_calc_")
  try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
      f.write(generate_calculator_html())

    # Open in a new browser tab/window
    print(f"Opening calculator in your default browser: {path}")
    webbrowser.open_new_tab(f"file://{path}")
  except Exception as e:
    print(f"Failed to open browser tab: {e}")


if __name__ == "__main__":
  open_calculator_in_browser()
