from .simple.shapes import triangle, square  # relative import


def house(n=8):
    triangle(n, "^")
    square(n, "=")


if __name__ == '__main__':
    print("TESTING THIS MODULE")
    house(5)
