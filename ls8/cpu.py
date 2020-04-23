"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0


    def load(self, file=""):
        """Load a program into memory."""

        address = 0

        # If no file given, just hardcode a program:
        if file == "":
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
        else:
            program = []
            f = open(file, "r")
            for line in f:
                if line[0] != "#":
                    program.append(int(line[:8], 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")


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
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        HLT = 0b00000001
        LDI = 0b10000010
        MUL = 0b10100010
        PRN = 0b01000111

        while running:
            if self.ram_read(self.pc) == LDI:
                self.ram_write(self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            elif self.ram_read(self.pc) == MUL:
                self.trace()
                self.ram_write(self.ram_read(self.pc + 1), (self.reg[self.ram_read(self.pc + 1)] * self.reg[self.ram_read(self.pc + 2)]))
                self.pc += 3
            elif self.ram_read(self.pc) == PRN:
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 2
            elif self.ram_read(self.pc) == HLT:
                running = False
