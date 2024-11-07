#simple_generator
numbers = [1, 2, 2, 2, 3, 4, 5]  

result_list = [numbers[i] == numbers[i+1] == numbers[i+2] for i in range(len(numbers) - 2)]

if __name__ == "__main__":  
    result = any(result_list)

    print(result)