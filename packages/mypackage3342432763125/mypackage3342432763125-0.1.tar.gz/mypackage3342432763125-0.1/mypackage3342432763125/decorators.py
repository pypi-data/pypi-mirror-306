import time
def timeit(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()
        result = t2 - t1
        print(f'работа заняла {result} секунд')
    return wrapper

def func_one():
    my_list = [i for i in range(1,1000000)]

@timeit
def func_two():
    my_list = [i for i in range(1,1000000)]

if __name__ == "__main__":  
    func_one()
    func_two()