import sys

PRINT_SAM      = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6

memory = [
    PRINT_SAM,
    PRINT_SAM,
    PRINT_SAM,
    PRINT_NUM,
    14,
    SAVE,
    99,
    2,
    PRINT_REGISTER,
    2,
    SAVE,
    101,
    1,
    ADD,
    1,
    2,
    PRINT_REGISTER,
    1,
    HALT
]

# R0 - R7; very limited but very fast
registers = [0] * 8

# L1, L2; shed

# RAM; warehouse

running = True
pc = 0

while running:
    command = memory[pc]

    if command == ADD:
        # reg1 = reg1 + reg2
        regidx1 = memory[pc + 1]
        regidx2 = memory[pc + 2]
        registers[regidx1] = registers[regidx1] + registers[regidx2]
        pc += 3
    
    elif command == PRINT_NUM:
        print(memory[pc + 1])
        pc += 2

    elif command == PRINT_REGISTER:
        print(registers[memory[pc + 1]])
        pc += 2

    elif command == PRINT_SAM:
        print("Sam!")
        pc += 1

    elif command == SAVE:
        registers[memory[pc + 2]] = memory[pc + 1]
        pc += 3

    elif command == HALT:
        running = False

    else:
        print("Error!")
        sys.exit(1)