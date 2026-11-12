"""Hack assembler (Nand to Tetris) - Capstone, K = 84.
Usage: python assembler.py Prog.asm   ->  Prog.hack  (+ symbols.txt)
Extra feature (K mod 3 == 0): save all labels and variables with
their addresses in symbols.txt.
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        t["R%d" % i] = i
    return t


def clean(line):
    """Remove comment and all spaces."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def first_pass(lines, table):
    """Remember where each (LABEL) is. Labels do not take a ROM line."""
    rom = 0
    for line in lines:
        line = clean(line)
        if not line:
            continue
        if line.startswith("("):
            table[line[1:-1]] = rom
        else:
            rom += 1


def c_instruction(line):
    dest, jump = "", ""
    if "=" in line:
        dest, line = line.split("=", 1)
    if ";" in line:
        line, jump = line.split(";", 1)
    return "111" + COMP[line] + DEST[dest] + JUMP[jump]


def second_pass(lines, table, variables):
    out, next_var = [], 16
    for line in lines:
        line = clean(line)
        if not line or line.startswith("("):
            continue
        if line.startswith("@"):
            sym = line[1:]
            if sym.isdigit():
                n = int(sym)
            else:
                if sym not in table:          # new variable
                    table[sym] = next_var
                    variables[sym] = next_var
                    next_var += 1
                n = table[sym]
            out.append(format(n, "016b"))
        else:
            out.append(c_instruction(line))
    return out


def main():
    path = sys.argv[1]
    lines = open(path).read().splitlines()
    table = predefined()
    first_pass(lines, table)
    labels = {k: v for k, v in table.items()
              if k not in predefined()}
    variables = {}
    code = second_pass(lines, table, variables)
    open(path.rsplit(".", 1)[0] + ".hack", "w").write("\n".join(code) + "\n")

    # ---- Extra feature (K mod 3 = 0): symbols.txt ----
    with open("symbols.txt", "w") as f:
        f.write("# Labels (ROM addresses)\n")
        for name, addr in labels.items():
            f.write("%s = %d\n" % (name, addr))
        f.write("# Variables (RAM addresses)\n")
        for name, addr in variables.items():
            f.write("%s = %d\n" % (name, addr))
    print("Wrote %d instructions, symbols.txt saved." % len(code))


if __name__ == "__main__":
    main()
