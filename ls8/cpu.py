"""CPU functionality."""

import sys

ADD  = 0b10100000
CALL = 0b01010000
DIV  = 0b10100011
HLT  = 0b00000001
LDI  = 0b10000010
MUL  = 0b10100010
POP  = 0b01000110
PRN  = 0b01000111
PUSH = 0b01000101
RET  = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = False
        # Set up Registers
        self.registers = {
            "PC":  0,   # R0 : Program Counter
            "IR":  0,   # R1 : Instruction Register
            "MAR": 0,   # R2 : Memory Address Register
            "MDR": 0,   # R3 : Memory Data Register
            "FL":  0,   # R4 : Flags
            "IM":  0,   # R5 : Interrupt Mask
            "IS":  0,   # R6 : Interrupt Status
            "SP":  0xF4 # R7 : Stack Pointer
        }
        # Set up dispatch branch table
        self.dispatch = {
            ADD:  self.add,
            CALL: self.call,
            DIV:  self.div,
            HLT:  self.hlt,
            LDI:  self.ldi,
            MUL:  self.mul,
            POP:  self.pop,
            PRN:  self.prn,
            PUSH: self.push,
            RET:  self.ret
        }


    def load(self):
        """Load a program into memory."""

        address = 0

        # If no file given, just hardcode a program:
        if len(sys.argv) == 1:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]
        # If file given, load file
        elif len(sys.argv) == 2:
            try:
                program = []
                with open(sys.argv[1], "r") as f:
                    for line in f:
                        if line[0] != "#":
                            program.append(int(line.split("#")[0].strip("\n"), 2))

            except FileNotFoundError:
                print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
                sys.exit(2)
        else:
            print("Too many arguments given!")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    ### OPERATIONS ###
    def add(self):
        self.alu("ADD", self.ram_read(self.registers["PC"] + 1), self.ram_read(self.registers["PC"] + 2))
        self.registers["PC"] += 3


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                print("Error: Cannot divide by 0!")
                self.hlt()
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def call(self):
        self.registers["SP"] -= 1
        self.ram[self.registers["SP"]] = self.registers["PC"] + 2
        self.registers["PC"] = self.reg[self.ram[self.registers["PC"] + 1]]


    def div(self):
        self.alu("DIV", self.ram_read(self.registers["PC"] + 1), self.ram_read(self.registers["PC"] + 2))
        self.registers["PC"] += 3


    def hlt(self):
        self.running = False


    def ldi(self):
        self.ram_write(self.ram_read(self.registers["PC"] + 1), self.ram_read(self.registers["PC"] + 2))
        self.registers["PC"] += 3


    def mul(self):
        self.alu("MUL", self.ram_read(self.registers["PC"] + 1), self.ram_read(self.registers["PC"] + 2))
        self.registers["PC"] += 3


    def pop(self):
        self.reg[self.ram[self.registers["PC"] + 1]] = self.ram[self.registers["SP"]]
        # No need to reset to 0 because push will overwrite later
        # self.ram[self.registers["SP"]] = 0
        self.registers["SP"] += 1
        self.registers["PC"] += 2
        return self.reg[self.ram[self.registers["PC"] - 1]]


    def prn(self):
        print(self.reg[self.ram_read(self.registers["PC"] + 1)])
        self.registers["PC"] += 2


    def push(self):
        self.registers["SP"] -= 1
        self.ram[self.registers["SP"]] = self.reg[self.ram[self.registers["PC"] + 1]]
        self.registers["PC"] += 2


    def ret(self):
        self.registers["PC"] = self.ram[self.registers["SP"]]
        self.ram[self.registers["SP"]] = 0
        self.registers["SP"] += 1
    ### END OF OPERATIONS ###

    def ram_read(self, address):
        return self.ram[address]


    def ram_write(self, address, value):
        self.reg[address] = value


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.registers["PC"],
            #self.fl,
            #self.ie,
            self.ram_read(self.registers["PC"]),
            self.ram_read(self.registers["PC"] + 1),
            self.ram_read(self.registers["PC"] + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            self.dispatch[self.ram[self.registers["PC"]]]()
