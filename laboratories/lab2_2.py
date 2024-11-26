def check_if_pow_of_m(n: int, k: int, p=0) -> bool:
    if n == k == 0:
        return True
    if n < k ** p:
        return False
    elif n == k ** p:
        return True
    return check_if_pow_of_m(n, k, p + 1)


def requirements(number: str) -> bool:
    try:
        ng = int(number)
        if ng < 0:
            return False
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    n = input('n=')
    while not requirements(n):
        n = input('n=')
    k = input('k=')
    while not requirements(k):
        k = input('k=')
    print(check_if_pow_of_m(int(n), int(k)))
