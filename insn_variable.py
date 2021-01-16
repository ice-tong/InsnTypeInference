from insn_type import *


class InsnVariable:

    def __init__(self, offset, 
            base='rbp', var_name='_'):
        self.offset = offset
        self.base = base
        self.var_name = var_name

        self._var_type = InsnType()
        self._definite_type = False
        self._pointer = False
    
    @property
    def var_type(self):
        return self._var_type

    def set_type(self, var_type, definite_type=False):
        if self._definite_type: return
        self._var_type = var_type
        self._definite_type = definite_type
    
    def __repr__(self):
        return '<InsnVariable {} | {} {}>'.format(self.var_type, self.base, hex(self.offset))

    def __eq__(self, other):
        if not isinstance(other, InsnVariable): return False
        return self.offset == other.offset and \
            self.base == other.base


class VariableManagement:

    def __init__(self, region):
        self.region = region
        self.insn2var = {}
        self.offset2var = {}
    
    def add_isns2variable(self, insn_addr, var):
        self.insn2var[insn_addr] = var
    
    def add_offset2variable(self, offset, var):
        self.offset2var[offset] = var

    def find_variable_by_offset(self, offset):
        if offset in self.offset2var:
            return self.offset2var[offset]
        else: 
            return InsnVariable(offset)