

def oddNumbers(l, r):
    arr = list(range(l, r))
    result = []
    
    for number in arr:
        if number % 2 != 0:
            result.append(number)
    
    return result


print(oddNumbers(2,10))

