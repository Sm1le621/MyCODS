def digit_sum(n: int) -> int: #recursion
    if n < 10:
        return n

    sum = (n%10) + digit_sum(n // 10)
    return sum

def digit_sum_cycles(n: int) -> int: 
    num_list = []
    for i in str(n):
        num_list.append(int(i))
    return sum(num_list)



print(digit_sum(1234))
print(digit_sum(987))
print(digit_sum(5))
print(digit_sum_cycles(1))