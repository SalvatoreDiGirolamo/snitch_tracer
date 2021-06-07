import re
import riscvmodel

TRACE_IN_REGEX = r'(\d+)\s+(\d+)\s+(\d+)\s+(0x[0-9A-Fa-fz]+)\s+([^#;]*)(\s*#;\s*(.*))?'


def parse_annotation(dict_str: str):
    return {
        key: int(val, 16)
        for key, val in re.findall(r"'([^']+)'\s*:\s*([^\s,]+)", dict_str)
    }


def parse_line(line: str):
    match = re.search(TRACE_IN_REGEX, line.strip('\n'))
    if match is None:
        raise ValueError('Not a valid trace line:\n{}'.format(line))
    time_str, cycle_str, priv_lvl, pc_str, insn, _, extras_str = match.groups()
    instr_extras = parse_annotation(extras_str)

    riscv_instr = riscvmodel.insn.Instruction()

    print(riscv_instr.decode(insn))


def parse_file(filename: str):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines: parse_line(line)
    f.close()

parse_file("trace/trace_hart_00010000.dasm")
