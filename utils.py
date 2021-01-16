import re
from insn_type import InsnTypeInt, InsnType, InsnTypeChar, InsnTypeFloat, InsnTypeDouble


REGS = [
    # 8-bit general-purpose reg
    'AL', 'BL', 'CL', 'DL', 'AH', 'BH', 'CH', 'DH',
    'DIL', 'SIL', 'BPL', 'SPL',
    'R8L', 'R9L', 'R10L', 'R11L', 'R12L', 'R13L', 'R14L', 'R15L',
    # 16-bit general-purpose reg
    'AX', 'BX', 'CX', 'DX', 'DI', 'SI', 'BP', 'SP',
    'R8W', 'R9W', 'R10W', 'R11W', 'R12W', 'R13W', 'R14W', 'R15W',
    # 32-bit general-purpose reg
    'EAX', 'EBX', 'ECX', 'EDX', 'EDI', 'ESI', 'EBP', 'ESP',
    'R8D', 'R9D', 'R10D', 'R11D', 'R12D', 'R13D', 'R14D', 'R15D',
    # 64-bit general-purpose reg
    'RAX', 'RBX', 'RCX', 'RDX', 'RDI', 'RSI', 'RBP', 'RSP',
    'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15',
    # Instruction Pointer Register
    'RIP',
    # MMX and XMM Register
    'MMX0', 'MMX1', 'MMX2', 'MMX3', 'MMX4', 'MMX5', 'MMX6', 'MMX7',
    'XMM0', 'XMM1', 'XMM2', 'XMM3', 'XMM4', 'XMM5', 'XMM6', 'XMM7', 'MXCSR', 
    ] 
"""
# FPU Register
'ST0', 'ST1', 'ST2'，'ST3', 'ST4', 'ST5', 'ST6', 'ST7', 
# segment reg
'CS', 'DS', 'SS', 'ES', 'FS', 'GS',
# control reg
'CR0', 'CR2', 'CR3', 'CR4', 
# debug reg
'DR0', 'DR1', 'DR2', 'DR3', 'DR6', 'DR7',
"""

BYTE_WIDTHS = ['', 'byte ptr', 'word ptr', 'dword ptr', 'qword ptr']
BYTE_WIDTHS_size = {
    '': -1, 'byte ptr': 1, 'word ptr': 2, 
    'dword ptr': 4, 'qword ptr': 8
    }

def parse_regs(op):
    register_list = re.findall(
        r'(%s)' % '|'.join(REGS), 
        op.upper(), flags=re.IGNORECASE
        )
    return register_list


def parse_offset(op):
    """
    :return:    byte_width, base, offset
    """
    result = re.findall(
        r'(%s)\s\[(%s).*?\s([+-]?\s[xa-f\d]+)\]' % (
            '|'.join(BYTE_WIDTHS), '|'.join(REGS)
            ),
        op, re.IGNORECASE
        )
    if result: 
        return result[0][0], result[0][1], \
            int(result[0][2].replace(' ', ''), 16) # e.g. "- 0x4"
    elif '[' in op: 
        r = re.findall(
            r'(%s)\s\[(%s)\]' % (
                '|'.join(BYTE_WIDTHS), '|'.join(REGS)
                ),
            op, re.IGNORECASE
            )
        if r: return r[0][0], r[0][1], 0,
        else: return None, None, None
    else: 
        return None, None, None


def guess_basic_type(byte_width, fp_mode=False):
    if byte_width == 'byte ptr':
        return InsnTypeChar()
    elif byte_width == 'word ptr':
        return InsnTypeInt(size=2, label='short int')
    elif byte_width == 'dword ptr' and not fp_mode:
        return InsnTypeInt(size=4, label='int')
    elif byte_width == 'dword ptr' and fp_mode:
        return InsnTypeFloat(size=4, label='float')
    elif byte_width == 'qword ptr' and not fp_mode:
        return InsnTypeInt(size=8, label='long int')
    elif byte_width == 'qword ptr' and fp_mode:
        return InsnTypeDouble(size=8, label='double')
    elif byte_width == 'qword ptr' and pt_mode:
        return InsnTypeDouble(size=8, label='double')
    else: 
        return InsnType(label='unknow')


if __name__ == "__main__":
    print(parse_offset('dword ptr [rbp + rax*4 - 0x30]'))