import sys
import random

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Expected 2 arguments:")
        print("generate.py [count] [length]")
        sys.exit()

    count = int(sys.argv[1])
    length = int(sys.argv[2])

    with open("static.txt", 'w') as static:
        static.write("{}\n{}\n".format(count, length))
        for _ in range(count):
            radius = random.uniform(0, 1)
            static.write("{} 1.0\n".format(radius))

    with open("dynamic.txt", 'w') as dynamic:
        dynamic.write("0\n")
        for _ in range(count):
            x = random.uniform(0, length)
            y = random.uniform(0, length)
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            dynamic.write("{} {} {} {}\n".format(x, y, vx, vy))
