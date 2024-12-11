class ShredLangInterpreter:
    def __init__(self):
        # Initialize the interpreter with a dictionary for storing variables
        self.variables = {}

    def interpret_by_filename(self, filename):
        # Read code from a file and pass it to the interpreter
        with open(filename, 'r') as file:
            code = file.read()
        self.interpret(code)

    def interpret(self, code):
        # Main entry point for interpreting code
        lines = code.splitlines()  # Split code into individual lines
        statements = self.parse_statements(lines)  # Parse the code into statements
        self.execute_statements(statements)  # Execute the parsed statements

    def parse_statements(self, lines):
        # Parse lines of code into a structured list of statements
        statements = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()  # Strip unnecessary spaces

            if line.startswith("trick"):
                # Handle variable declaration
                parts = line.split()
                name = parts[1]  # Variable name
                value = self.parse_expression(" ".join(parts[3:]).rstrip(";"))  # Expression for value
                statements.append({
                    "type": "trick",
                    "name": name,
                    "value": value
                })
            elif "=" in line and line.endswith(";"):
                # Handle variable reassignment
                name, value = map(str.strip, line.split("=", 1))
                value = self.parse_expression(value.rstrip(";"))  # Expression for new value
                statements.append({
                    "type": "assignment",
                    "name": name,
                    "value": value
                })
            elif line.startswith("shout"):
                # Handle print statements
                message = self.parse_expression(line[line.index("(") + 1:line.rindex(")")])
                statements.append({
                    "type": "shout",
                    "message": message
                })
            elif line.startswith("carve"):
                # Handle conditional blocks
                condition = self.parse_expression(line[line.index("(") + 1:line.rindex(")")])
                block_lines = []
                i += 1
                # Collect lines inside the block
                while i < len(lines) and lines[i].strip() == "{":
                    i += 1
                brace_count = 1
                while i < len(lines) and brace_count > 0:
                    inner_line = lines[i].strip()
                    if inner_line == "{":
                        brace_count += 1
                    elif inner_line == "}":
                        brace_count -= 1
                    if brace_count > 0:
                        block_lines.append(inner_line)
                    i += 1
                statements.append({
                    "type": "carve",
                    "condition": condition,
                    "block": self.parse_statements(block_lines),  # Parse nested statements
                })
                i -= 1  # Adjust for loop increment
            elif line.startswith("spin"):
                # Handle loop blocks
                parts = line[line.index("(") + 1:line.rindex(")")].strip().split()
                if len(parts) != 2 or parts[1] != "times":
                    raise ValueError(f"Invalid spin statement syntax: {line}")
                loop_count = self.parse_expression(parts[0])  # Number of iterations
                block_lines = []
                i += 1
                while i < len(lines) and lines[i].strip() == "{":
                    i += 1
                brace_count = 1
                while i < len(lines) and brace_count > 0:
                    inner_line = lines[i].strip()
                    if inner_line == "{":
                        brace_count += 1
                    elif inner_line == "}":
                        brace_count -= 1
                    if brace_count > 0:
                        block_lines.append(inner_line)
                    i += 1
                statements.append({
                    "type": "spin",
                    "loop_count": loop_count,
                    "block": self.parse_statements(block_lines),
                })
                i -= 1  # Adjust for loop increment
            elif line.startswith("bail"):
                # Handle error-throwing statements
                message = line[line.index("(") + 1:line.rindex(")")].strip()
                statements.append({
                    "type": "bail",
                    "message": self.parse_expression(message)
                })
            elif line in ["strap_in", "unstrap", "{", "}"]:
                # Ignore structural keywords
                pass
            elif line == "":
                # Ignore empty lines
                pass
            else:
                # Handle unknown statements
                raise ValueError(f"Unknown statement: {line}")
            i += 1
        return statements

    def execute_statements(self, statements):
        # Execute a list of parsed statements
        for statement in statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        # Execute an individual statement based on its type
        if statement["type"] == "trick":
            # Variable declaration
            self.variables[statement["name"]] = self.evaluate_expression(statement["value"])
        elif statement["type"] == "assignment":
            # Variable reassignment
            if statement["name"] not in self.variables:
                raise ValueError(f"Variable '{statement['name']}' not declared before assignment.")
            self.variables[statement["name"]] = self.evaluate_expression(statement["value"])
        elif statement["type"] == "shout":
            # Print statement
            print(self.evaluate_expression(statement["message"]))
        elif statement["type"] == "carve":
            # Conditional block
            condition = self.evaluate_expression(statement["condition"])
            if condition:
                self.execute_statements(statement["block"])
        elif statement["type"] == "spin":
            # Loop block
            loop_count = self.evaluate_expression(statement["loop_count"])
            if not isinstance(loop_count, int):
                raise ValueError(f"Loop count must be an integer. Got: {loop_count}")
            for iteration in range(1, loop_count + 1):
                self.variables["spin_iteration"] = iteration  # Store iteration variable
                self.execute_statements(statement["block"])
            del self.variables["spin_iteration"]  # Clean up after loop
        elif statement["type"] == "bail":
            # Error-throwing statement
            raise RuntimeError(self.evaluate_expression(statement["message"]))
        else:
            raise ValueError(f"Unknown statement type: {statement['type']}")

    def evaluate_expression(self, expr):
        # Evaluate an expression and return its value
        if isinstance(expr, str):
            if expr.isdigit():
                return int(expr)
            elif expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]  # Return string without quotes
            elif expr in self.variables:
                return self.variables[expr]
            else:
                raise ValueError(f"Unknown token: {expr}")
        elif isinstance(expr, list):
            if len(expr) == 1:
                return self.evaluate_expression(expr[0])
            try:
                # Find the first operator and split the expression
                operator_index = next(i for i, x in enumerate(expr) if x in ["+", "-", ">", "<", ">=", "<=", "==", "!="])
            except StopIteration:
                raise ValueError(f"Invalid expression: {expr}")
            left_value = self.evaluate_expression(expr[:operator_index])
            operator = expr[operator_index]
            right_value = self.evaluate_expression(expr[operator_index + 1:])
            # Perform the operation
            if operator == "+":
                if isinstance(left_value, str) or isinstance(right_value, str):
                    return str(left_value) + str(right_value)
                return left_value + right_value
            elif operator == "-":
                return left_value - right_value
            elif operator == ">":
                return left_value > right_value
            elif operator == "<":
                return left_value < right_value
            elif operator == ">=":
                return left_value >= right_value
            elif operator == "<=":
                return left_value <= right_value
            elif operator == "==":
                return left_value == right_value
            elif operator == "!=":
                return left_value != right_value
            else:
                raise ValueError(f"Unknown operator: {operator}")
        else:
            raise ValueError(f"Unknown expression: {expr}")

    def parse_expression(self, expr):
        # Tokenize an expression into a list of operands and operators
        tokens = []
        current_token = ""
        in_string = False
        i = 0
        while i < len(expr):
            char = expr[i]
            if char == '"' and not in_string:
                in_string = True
                current_token += char
            elif char == '"' and in_string:
                in_string = False
                current_token += char
                tokens.append(current_token)
                current_token = ""
            elif in_string:
                current_token += char
            elif char in "()+-*/><=! ":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                if char in "><=!":
                    if i + 1 < len(expr) and expr[i + 1] == "=":
                        tokens.append(char + "=")
                        i += 1
                    else:
                        tokens.append(char)
                elif char.strip():
                    tokens.append(char)
            else:
                current_token += char
            i += 1
        if current_token:
            tokens.append(current_token)
        return [token for token in tokens if token.strip()]

if __name__ == "__main__":
    # Entry point for the interpreter
    interpreter = ShredLangInterpreter()
    try:
        interpreter.interpret_by_filename("program5.shd")  # Replace with the desired program file
    except RuntimeError as e:
        print(e)  # Print runtime errors (e.g., from bail)
