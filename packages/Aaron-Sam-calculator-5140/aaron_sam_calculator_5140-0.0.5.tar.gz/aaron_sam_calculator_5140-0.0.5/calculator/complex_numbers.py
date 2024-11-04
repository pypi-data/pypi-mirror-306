def complex_add(a, b):
    return complex(a) + complex(b) 

def complex_subtract(a, b):
    return complex(a.real - b.real, a.imag - b.imag)
    
def complex_multiply(a, b):
    real_part = a.real * b.real - a.imag * b.imag
    imag_part = a.real * b.imag + a.imag * b.real
    return complex(real_part, imag_part)

def complex_divide(a, b):
    if b.real == 0 and b.imag == 0:
        raise ValueError("Cannot divide by zero")
    real_part = (a.real * b.real + a.imag * b.imag) / (b.real**2 + b.imag**2)
    imag_part = (a.imag * b.real - a.real * b.imag) / (b.real**2 + b.imag**2)
    return complex(real_part, imag_part)
    
def complex_conjugate(a):
    return complex(a.real, -a.imag)