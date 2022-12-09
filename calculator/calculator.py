# write your code here
from operator import methodcaller
from collections import deque


class InvalidIdentifier(Exception):
    def __init__(self):
        super().__init__("Invalid identifier")


class InvalidAssignment(Exception):
    def __init__(self):
        super().__init__("Invalid assignment")


class InvalidExpression(Exception):
    def __init__(self):
        super().__init__("Invalid expression")


class UnknownVariable(Exception):
    def __init__(self):
        super().__init__("Unknown variable")


class UnknownCommand(Exception):
    def __init__(self):
        super().__init__("Unknown command")


class Number:
    def __init__(self, value=0):
        self.value = value

    def plus(self, number):
        return self.value + number.value

    def minus(self, number):
        return self.value - number.value

    def multiplication(self, number):
        return self.value * number.value

    def division(self, number):
        return int(self.value / number.value)


class Variable:
    var_dict = {}

    def __init__(self, name, value=None):
        if name.isalpha():
            self.name = name
        else:
            raise InvalidIdentifier

        if value:
            if isinstance(value, Variable):
                self.set_val(value.value)
            elif isinstance(value, Number):
                self.set_val(value)
            else:
                raise InvalidAssignment

    def get_val(self):
        if self.name in self.var_dict:
            return self.var_dict[self.name]
        else:
            raise UnknownVariable

    def set_val(self, value):
        self.value = value
        self.var_dict[self.name] = self.value


class Operation:
    operation_map = {'+': 'plus',
                     '-': 'minus',
                     '*': 'multiplication',
                     '/': 'division'}

    precedence_rank = {'*': 0,
                       '/': 0,
                       '+': 1,
                       '-': 1}

    method = None

    def __init__(self, sign):
        self.sign = self.determine_sign(sign)

        if self.sign in self.operation_map:
            self.method = self.operation_map[self.sign]

    def determine_sign(self, sign):
        if all('+' in c or '-' in c for c in sign):
            minus_number = sign.count('-')
            if minus_number % 2:
                return '-'
            else:
                return '+'
        elif sign.count('*') > 1 or sign.count('/') > 1:
            raise InvalidExpression

        return sign


class Expression:
    split_expr = None
    parsed_expr = None

    def __init__(self, expr):
        self.expr = expr
        self.postfix = []
        self.operations = deque()

        if expr.count('(') == expr.count(')'):
            self.split()
            self.parse()
            self.to_postfix()
        else:
            raise InvalidExpression

    def split(self):
        """
        Splits the expression into the list of operands and operations.

        Example:
            '8 * 3 + 12 * (4 - 2)' -> ['8', '*', '3', '+', '12', '*', '(', '4', '-', '2', ')']
        """
        expr = self.expr.replace(' ', '')

        element = ''
        self.split_expr = []  # случай -10 всё ещё не учтён
        for ch in expr:
            if len(element) == 0:
                element += ch
            elif element[-1].isalnum() == ch.isalnum() and ch != '(' and ch != ')':
                element += ch
            else:
                self.split_expr.append(element)
                element = ch

        self.split_expr.append(element)

    def parse(self):
        """ Converts numeric types and variables to the instance of the class Number; operations to the instance of Operation class. """
        self.parsed_expr = []
        for i, el in enumerate(self.split_expr):
            try:
                parsed = Number(int(el))
            except ValueError:
                if el.isalpha():
                    if el not in Variable.var_dict:
                        raise UnknownVariable
                    parsed = Variable(el).get_val()
                elif any(c in Operation.operation_map for c in el):
                    parsed = Operation(el)
                else:
                    parsed = el

            # If the expression starts with negative number
            if i == 1 and isinstance(parsed, Number) and isinstance(self.parsed_expr[0], Operation):
                operation = self.parsed_expr[0]
                if operation.sign in '-+':
                    fun = methodcaller(operation.method, parsed)
                    self.parsed_expr[0] = Number(fun(Number()))
                else:
                    raise InvalidExpression
            else:
                self.parsed_expr.append(parsed)

    def to_postfix(self):
        """ Convert the split and parsed expression to the postfix notation.
            In this notation, operators follow their operands.
            Example:
                Infix notation: 2 * (3 + 4) + 1
                Postfix notation: 2 3 4 + * 1 +
        """
        for element in self.parsed_expr:
            if isinstance(element, Number):
                self.postfix.append(element)
            else:
                if len(self.operations) == 0 or self.operations[-1] == '(':
                    self.operations.append(element)
                elif element == ')':
                    top_operator = self.operations.pop()
                    while top_operator != '(':
                        self.postfix.append(top_operator)
                        top_operator = self.operations.pop()

                elif (element == '('
                      or Operation.precedence_rank[element.sign] < Operation.precedence_rank[self.operations[-1].sign]):
                    self.operations.append(element)
                elif Operation.precedence_rank[element.sign] >= Operation.precedence_rank[self.operations[-1].sign]:
                    while True:
                        if (len(self.operations) == 0 or self.operations[-1] == '('
                           or Operation.precedence_rank[self.operations[-1].sign] > Operation.precedence_rank[element.sign]):
                            self.operations.append(element)
                            break
                        self.postfix.append(self.operations.pop())
                else:
                    raise InvalidExpression
        else:
            for _ in range(len(self.operations)):
                self.postfix.append(self.operations.pop())

    def calculate(self):
        """
        Calculates the expression in postfix notation scanning it from left to right by following
        - If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
        - If the incoming element is the name of a variable, push its value into the stack.
        - If the incoming element is an operator, then pop twice to get two numbers and perform the operation; push the result on the stack.
        - When the expression ends, the number on the top of the stack is a final result.

        :return: the result integer value.
        """

        calculate_stack = deque()
        for element in self.postfix:
            if isinstance(element, Number):
                calculate_stack.append(element)
            else:
                second_num = calculate_stack.pop()
                first_num = calculate_stack.pop()
                fun = methodcaller(element.method, second_num)
                calculate_stack.append(Number(fun(first_num)))

        result = calculate_stack.pop()

        return result


def process_command(command):
    if command == '/exit':
        print('Bye!')
        return False
    elif command == '/help':
        print("The program does the following operations: addition +, subtraction -, multiplication *, integer division / and parentheses (...)."
              "The example of possible input: 3 + 8 * ((4 + 3) * 2 + 1) - 6 / (2 + 1)."
              "Note that two adjacent minus signs turn into a plus."
              ""
              "You can store results in variables. Note that:"
              "- The name of a variable can contain ONLY LATIN LETTERS."
              "- A variable can have a name consisting of more than one letter."
              "- A variable name is CASE-SENSITIVE."
              "- The value can be an INTEGER or a value of another VARIABLE."
              "- Assigning a new value to an existing variable will REWRITE the previous value."
              "- Type the name of a variable to print its value.")
    else:
        raise UnknownCommand
    return True


def process_expression(expression):
    if '=' in expression:                               # Assignment
        split_expression = expression.split('=')
        if len(split_expression) > 2:
            raise InvalidAssignment
        else:
            left_expr = split_expression[0].strip()
            var = Variable(left_expr)

            right_expr = split_expression[1].strip()
            try:
                result = Expression(right_expr).calculate()
            except InvalidExpression:
                raise InvalidAssignment
            else:
                var.set_val(result)
    else:                                               # Calculation
        result = Expression(expression).calculate()
        print(result.value)


if __name__ == '__main__':
    state = True
    while state:
        input_line = input()
        try:
            if input_line.startswith('/'):
                state = process_command(input_line)
            elif input_line.strip() == '':
                continue
            else:
                process_expression(input_line)
        except InvalidAssignment as err:
            print(err)
        except InvalidIdentifier as err:
            print(err)
        except InvalidExpression as err:
            print(err)
        except UnknownVariable as err:
            print(err)
        except UnknownCommand as err:
            print(err)
