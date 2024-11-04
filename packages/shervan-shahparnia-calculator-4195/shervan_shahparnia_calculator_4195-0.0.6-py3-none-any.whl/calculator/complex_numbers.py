def add_complex(a, b):
    return complex(a) + complex(b)

def subtract_complex(a, b):
    return complex(a) - complex(b)

def multiply_complex(a, b):
    return complex(a) * complex(b)

def divide_complex(a, b):
    try:
        return complex(a) / complex(b)
    except ZeroDivisionError:
        return "Error: Division by zero"

def conjugate(a):
    return complex(a).conjugate()
