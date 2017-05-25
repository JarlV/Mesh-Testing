import random

def get_random_number(min, max):
    divisor = 255/(max-min)
    rand = random.randint(0, 255)
    return int(min + rand / divisor)

min = 2
max = 4
distribution = [[min + j, 0] for j in range(max - min + 1)]

for i in range(10^1000000):
    rand = get_random_number(min, max)
    if min <= rand <= max:
        distribution[rand-min][1] += 1
    else:
        print("fail")

for i in distribution:
    print(i)