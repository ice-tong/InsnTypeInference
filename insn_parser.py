import angr
import re

from insn_type import *
from insn_variable import InsnVariable, VariableManagement
from utils import parse_offset, parse_regs
from utils import REGS, BYTE_WIDTHS_size
from utils import guess_basic_type


class InsnVariableParser:

    def __init__(self, binary_fpath):
        self.proj = angr.Project(
            binary_fpath,
            auto_load_libs=False,
            )
        self.cfg = self.proj.analyses.CFG(
                show_progressbar=True, 
                data_references=True, 
                normalize=True
                )
        for func in self.cfg.kb.functions.values():
            self._parse_func(func)
    
    def _parse_func(self, func):
        if func.name != 'main': return 
        insn_varmgr = VariableManagement(func.name)
        sorted_blocks = sorted([(b.addr, b) for b in func.blocks])
        for _, block in sorted_blocks:
            lea_idx = 0
            reg_dict = {r: None for r in REGS}
            for idx, insn in enumerate(block.capstone.insns):
                op_list = insn.op_str.split(',')
                if len(op_list) != 2: continue
                
                dest_op, src_op = op_list
                mnemonic = insn.mnemonic
                dest_regs = parse_regs(dest_op)
                src_regs = parse_regs(src_op)
                dest_byte_width, dest_base, dest_offset \
                    = parse_offset(dest_op)
                src_byte_width, src_base, src_offset \
                    = parse_offset(src_op)

                # print(insn)
                # print(dest_byte_width, dest_base, dest_offset)
                # print(src_byte_width, src_base, src_offset)
                
                # floating point number flag
                if len(src_regs) == 1 and 'MM' in src_regs[0]: 
                    fp_mode = True
                elif len(dest_regs) == 1 and 'MM' in dest_regs[0]: 
                    fp_mode = True
                else:
                    fp_mode = False

                if mnemonic == 'lea':
                    if src_regs != ['RBP']: continue
                    pt_var = insn_varmgr.find_variable_by_offset(src_offset)
                    reg_dict[dest_regs[0]] = pt_var
                    lea_idx = idx
                    continue

                if dest_regs == ['RBP'] and dest_offset != None:
                    #  memory write to stack variables. e.g. mov [rbp - 0x10], raxs
                    insn_var = insn_varmgr.find_variable_by_offset(dest_offset)
                    ty = guess_basic_type(dest_byte_width, fp_mode)
                    if lea_idx+1 == idx and len(src_regs) == 1:
                        if reg_dict[src_regs[0]] != None:
                            ty = InsnTypePoniter(pt_type=reg_dict[src_regs[0]])
                            # fp_mode = True
                    insn_var.set_type(ty, fp_mode)
                    insn_varmgr.add_isns2variable(insn.address, insn_var)
                    insn_varmgr.add_offset2variable(dest_offset, insn_var)

                elif len(dest_regs) == 2 and 'RBP' in dest_regs and dest_offset != None:
                    # memory write to stack variables(array type). e.g. mov [rbp + rax*4 - 0x10], rax
                    insn_var = insn_varmgr.find_variable_by_offset(dest_offset)
                    elem_ty = guess_basic_type(dest_byte_width, fp_mode)
                    insn_var.set_type(InsnTypeArray(elem_type=elem_ty), fp_mode)
                    insn_varmgr.add_isns2variable(insn.address, insn_var)
                    insn_varmgr.add_offset2variable(dest_offset, insn_var)
                
                elif src_regs == ['RBP'] and src_offset != None:
                    #  memory read from stack variables. e.g. mov [rbp - 0x10], rax
                    insn_var = insn_varmgr.find_variable_by_offset(src_offset)
                    ty = guess_basic_type(src_byte_width, fp_mode)
                    insn_var.set_type(ty, fp_mode)
                    insn_varmgr.add_offset2variable(src_offset, insn_var)
                    if '[' not in dest_op and 'mov' in mnemonic:
                        reg_dict[dest_regs[0]] = insn_var

                elif len(src_regs) == 2 and 'RBP' in src_regs and src_offset != None:
                    # memory read from stack variables(array type). e.g. mov [rbp + rax*4 - 0x10], rax
                    insn_var = insn_varmgr.find_variable_by_offset(src_offset)
                    elem_ty = guess_basic_type(src_byte_width, fp_mode)
                    insn_var.set_type(InsnTypeArray(elem_type=elem_ty), fp_mode)
                    insn_varmgr.add_offset2variable(src_offset, insn_var)
                
                elif len(dest_regs) == 1 and dest_offset != None:
                    insn_var = reg_dict[dest_regs[0]]
                    if insn_var == None: continue
                    if not isinstance(insn_var.var_type, InsnTypePoniter):
                        insn_var.set_type(InsnTypePoniter(InsnTypeStruct()), True)
                    if len(src_regs) == 1 and reg_dict[src_regs[0]] != None:
                        number_var = reg_dict[src_regs[0]]
                        insn_var.var_type.pt_type.add_fields(
                            dest_offset, BYTE_WIDTHS_size[dest_byte_width], number_var
                            )
                    else:
                        number_ty = guess_basic_type(dest_byte_width)
                        insn_var.var_type.pt_type.add_fields(
                            dest_offset, BYTE_WIDTHS_size[dest_byte_width], number_ty
                            )

        for insn_addr in insn_varmgr.insn2var:
            var = insn_varmgr.insn2var[insn_addr]
            print(hex(insn_addr), var)
                

def main():
    # insn_var_parser = InsnVariableParser('./ctests/basic_type_test')
    insn_var_parser = InsnVariableParser('./ctests/array_test')


if __name__ == "__main__":
    main()