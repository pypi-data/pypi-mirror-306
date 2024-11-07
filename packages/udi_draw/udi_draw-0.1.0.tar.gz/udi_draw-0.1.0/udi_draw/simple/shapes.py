def square(h=5, c="*"):
    for i in range(h):
        print(c * h)


def triangle(n=5, c="*"):
    for i in range(n):
        print(c * (i+1))


def hash_square():
    square(9, "#")
