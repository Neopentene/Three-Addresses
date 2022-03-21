import prettytable


class IntermediateCode:
    def __init__(self, expression: str):
        self.original_expression = expression
        expression = expression.replace(" ", "").split(sep="=", maxsplit=1)
        self.expression = expression[1]
        self.assignment_var = expression[0]

        self.postfix = []
        self.operator = []
        self.three_addresses = []
        self.evaluator = []
        self.machine_code = []

        self.operatorList = ['-', '+', '*', '×', 'x', '/', '÷', '^']
        self.operator_code = {
            '*': 'MULT',
            '×': 'MULT',
            'x': 'MULT',
            '/': 'DIV',
            '÷': 'DIV',
            '-': 'SUB',
            '+': 'ADD'
        }

    @staticmethod
    def __priority(operator: str):
        if operator == '-' or operator == '+':
            return 1
        elif operator == '*' or operator == '×' or operator == 'x' or operator == '/' or operator == '÷':
            return 2
        else:
            return 0

    def generate_postfix(self):
        last_priority = 0

        for character in self.expression:
            if character in self.operatorList:
                if last_priority > self.__priority(character) and len(self.operator) > 0:
                    popped = self.operator.pop()
                    self.postfix.append(popped)

                    if len(self.operator) > 0:
                        popped = self.operator.pop()

                        while self.__priority(character) < self.__priority(popped):
                            self.postfix.append(popped)

                            if len(self.operator) > 0:
                                popped = self.operator.pop()

                                if self.__priority(character) >= self.__priority(popped):
                                    self.operator.append(popped)
                                    break
                            else:
                                break

                    self.operator.append(character)
                    last_priority = self.__priority(character)
                else:
                    self.operator.append(character)
                    last_priority = self.__priority(character)
            else:
                self.postfix.append(character)

        if len(self.operator) > 0:
            while len(self.operator):
                self.postfix.append(self.operator.pop())

        return self.postfix

    def evaluate_intermediate_code(self):

        if len(self.postfix) == 0:
            self.generate_postfix()

        count = 1
        for character in self.postfix:
            if character in self.operatorList:

                a = self.evaluator.pop()

                if len(self.evaluator) > 0:
                    b = self.evaluator.pop()
                else:
                    b = 't' + str(count - 1)

                operator = character
                result = 't' + str(count)

                self.evaluator.append(result)

                self.three_addresses.append([result, operator, a, b])

                count = count + 1

            else:
                self.evaluator.append(character)

        if len(self.evaluator) > 0:
            self.three_addresses.append([self.assignment_var, '=', self.evaluator.pop()])

        return self.three_addresses

    def generate_machine_code(self):

        if len(self.three_addresses) == 0:
            self.evaluate_intermediate_code()

        addresses: list
        for addresses in self.three_addresses:
            if len(addresses) == 4:
                self.machine_code.append(['MOV' + ' R0, ' + addresses[3]])
                self.machine_code.append([self.operator_code[addresses[1]] + ' R0, ' + addresses[2]])
                self.machine_code.append(['MOV ' + addresses[0] + ', R0'])
                self.machine_code.append([''])

            if len(addresses) == 3:
                self.machine_code.append(['MOV ' + addresses[0] + ', ' + addresses[2]])

        return self.machine_code


if __name__ == '__main__':
    intermediate_code = IntermediateCode(input('Enter an expression: '))

    postfix = intermediate_code.generate_postfix()
    intermediate_code_list = intermediate_code.evaluate_intermediate_code()
    machine_code = intermediate_code.generate_machine_code()
    print()

    intermediate_code_prettytable = prettytable.PrettyTable()
    machine_code_prettytable = prettytable.PrettyTable()

    intermediate_code_prettytable.field_names = ["result", "operator", "arg - 2", "arg - 1"]
    for addresses in intermediate_code_list:
        if len(addresses) == 4:
            intermediate_code_prettytable.add_row(addresses)
        if len(addresses) == 3:
            intermediate_code_prettytable.add_row([addresses[0], addresses[1], '?', addresses[2]])

    machine_code_prettytable.field_names = ['Machine Code']
    machine_code_prettytable.add_rows(machine_code)

    print("The expression was evaluated to the following postfix: \"" + "".join(postfix) + "\"" + "\n")
    print("Intermediate Code:")
    print(intermediate_code_prettytable.get_string(), "\n")
    print("Machine Code:")
    print(machine_code_prettytable.get_string())

    with open('intermediate_code_output.txt', 'w+') as file:
        file.write(
            "The results are for the following expression:\n--> " + intermediate_code.original_expression + "\n\n")
        file.write("The expression was evaluated to the following postfix:\n--> " + "".join(postfix) + "\n\n")
        file.write("Intermediate Code:\n")
        file.write(intermediate_code_prettytable.get_string() + "\n\n")
        file.write("Machine Code:\n")
        file.write(machine_code_prettytable.get_string() + "\n\n")
