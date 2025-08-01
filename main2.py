```
import random

def generate_random_code():
    code = ""
    for i in range(200):
        rand_num = random.randint(1, 10)
        if rand_num == 1:
            code += "print('Hello, World!')\n"
        elif rand_num == 2:
            code += "num1 = 5\nnum2 = 10\nresult = num1 + num2\nprint('The sum is:', result)\n"
        elif rand_num == 3:
            code += "def add_numbers(num1, num2):\n    return num1 + num2\nresult = add_numbers(3, 4)\nprint('The sum is:', result)\n"
        elif rand_num == 4:
            code += "for i in range(5):\n    print(i)\n"
        elif rand_num == 5:
            code += "a = 'Hello'\nb = 'World'\nprint(a + ' ' + b)\n"
        elif rand_num == 6:
            code += "x = 10\nif x > 5:\n    print('x is greater than 5')\nelse:\n    print('x is less than or equal to 5')\n"
        elif rand_num == 7:
            code += "def multiply_numbers(num1, num2):\n    return num1 * num2\nresult = multiply_numbers(3, 4)\nprint('The product is:', result)\n"
        elif rand_num == 8:
            code += "list1 = [1, 2, 3, 4, 5]\nprint('Length of list:', len(list1))\n"
        elif rand_num == 9:
            code += "name = input('Enter your name: ')\nprint('Hello, ' + name)\n"
        else:
            code += "print('Random number:', rand_num)\n"
    
    return code

random_code = generate_random_code()
print(random_code)
```
This code generates a random selection of Python code snippets, including printing statements, arithmetic operations, loops, function definitions, conditional statements, and list operations. It creates a total of 200 lines of random Python code.