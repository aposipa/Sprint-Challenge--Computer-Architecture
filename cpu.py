"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111 # Print
HLT = 0b00000001 # Halt
ADD = 0b10100000 # Add
SUB = 0b10100001 # Subtract
MUL = 0b10100010 # Multiply
DIV = 0b10100011 # Divide
PUSH = 0b01000101 # Stack Push
POP = 0b01000110 # Stack Pop
CALL = 0b01010000 # Call stack
RET = 0b00010001 # Ret

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7
        self.flags = 0b00000000
        
        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value 

    def load(self, filename):
        """Load a program into memory."""
        # file_path = f
        # program = open(f"{filename}", "r")
        # for line in program:
        #     if line[0] == "0" or line[0] == "1":
        #         cmd = line.split("#", 1)[0]
        #         self.ram[address] = int(cmd, 2)
        #         address += 1
        
        # filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                else:
                    self.ram[address] = int(line, 2)
                    address += 1


        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
        # self.load()
        while self.running == True:
            instruction_register = self.ram[self.pc]
            if instruction_register == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3

            elif instruction_register == PRN:
                reg_num = self.ram[self.pc + 1]
                print("Print num: ", self.reg[reg_num])
                self.pc += 2
            
            elif instruction_register == HLT:
                # self.running == False
                # self.pc += 1
                sys.exit(1)
            
            elif instruction_register == MUL:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] *= self.reg[value]
                self.pc += 3

            elif instruction_register == PUSH:
                self.sp -= 1
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                self.ram[self.sp] = value
                self.pc += 2

            elif instruction_register == POP:
                value = self.ram[self.sp]
                self.reg[self.ram[self.pc + 1]] = value
                self.sp += 1
                self.pc += 2

            elif instruction_register == CALL:
                return_address = self.pc +2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_address
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                self.pc = value

            elif instruction_register == RET:
                return_address = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.pc = return_address

            elif instruction_register == ADD:
                op_a = self.ram[self.pc + 1]
                op_b = self.ram[self.pc + 2]
                self.alu("ADD", op_a, op_b)
                self.pc +=3

            elif instruction_register == CMP:
                reg_a = self.reg[self.ram[self.pc + 1]]
                reg_b = self.reg[self.ram[self.pc + 2]]
                if reg_a == reg_b:
                    self.flags = 1
                else:
                    self.flags = 0
                self.pc += 3

            elif instruction_register == JMP:
                reg_a = self.ram[self.pc + 1]
                self.pc = self.reg[reg_a]

            elif instruction_register == JEQ:
                a = self.flags
                if a == 1:
                    self.pc = self.reg[self.ram[self.pc +1]]
                elif a == 0:
                    self.pc += 2

            elif instruction_register == JNE:
                a = self.flags
                if a == 0:
                    self.pc = self.reg[self.ram[self.pc +1]]
                else:
                    self.pc += 2

            else:
                print(f'unknown register {instruction_register} at address {self.pc}')
                sys.exit(1)
