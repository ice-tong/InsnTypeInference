

class InsnType:

    _fields = ('size')

    def __init__(self, size=None, label=None):
        """
        :param size:        byte size of the type
        :param label:       label for the type
        """
        self._size = size
        self._label = label
    
    @property
    def size(self):
        return self._size
    
    @property
    def label(self):
        return self._label
    
    # def __str__(self):
    #     return '{}'.format(self.label)
    
    def __repr__(self):
        return '{}'.format(self.label)


class InsnTypeChar(InsnType):

    def __init__(self, size=1, label='char'):
        super(InsnTypeChar, self).__init__(size, label)
    
    def extract(self, state, addr):
        out = state.memory.load(addr, 1, endness=state.arch.memory_endness)
        n = state.solver.eval(out)
        return chr(n)


class InsnTypeInt(InsnType):

    _fields = InsnType._fields + ('signed')

    def __init__(self, size=None, label=None, signed=False):
        super(InsnTypeInt, self).__init__(size, label)
        self._signed = signed
    
    @property
    def signed(self):
        return self._signed

    def extract(self, state, addr):
        out = state.memory.load(addr, self.size, endness=state.arch.memory_endness)
        n = state.solver.eval(out)
        if self.signed:
            n -= 1 << (self.size * state.arch.byte_width)
        elif n >= 1 << (self.size * state.arch.byte_width - 1):
            n -= 1 << (self.size * state.arch.byte_width)
        else: ...
        return n


class InsnTypeFloat(InsnType):

    _exponent = 8
    _fraction = 23

    def __init__(self, size=4, label='float'):
        super(InsnTypeFloat, self).__init__(size, label)
    
    def extract(self, state, addr):
        raise NotImplemented()


class InsnTypeDouble(InsnType):

    _exponent = 11
    _fraction = 52

    def __init__(self, size=8, label='double'):
        super(InsnTypeDouble, self).__init__(size, label)
    
    def extract(self, state, addr):
        raise NotImplemented()


class InsnTypePoniter(InsnType):

    def __init__(self, pt_type=None, size=None, label=None):
        super(InsnTypePoniter, self).__init__(size, label)
        if pt_type:
            self._pt_type = pt_type
        else:
            self._pt_type = InsnType()
    
    @property
    def pt_type(self):
        if not isinstance(self._pt_type, InsnType):
            return self._pt_type.var_type
        else:
            return self._pt_type
    
    def set_ptType(slef, pt_type):
        self.pt_type = pt_type
    
    def extract(self, state, addr):
        raise NotImplemented()
    
    def __repr__(self):
        return '{}*'.format(self.pt_type)


class InsnTypeArray(InsnType):

    def __init__(self, elem_type=None, length=None, size=None, label=None,):
        super(InsnTypeArray, self).__init__(size, label)
        if elem_type:
            self.elem_type = elem_type
        else:
            self.elem_type = InsnType()
        self.length = length
    
    def set_elemType(slef, elem_type):
        self.elem_type = elem_type

    def extract(self, state, addr):
        raise NotImplemented()

    def __repr__(self):
        return '{}[]'.format(self.elem_type)


class InsnTypeStruct(InsnType):

    def __init__(self, size=None, label=None):
        super(InsnTypeStruct, self).__init__(size, label)
        self.fields = {}

    def add_fields(self, number_offset, number_size, number_type=None):
        if number_offset in self.fields: return
        if number_type == None: number_type = InsnType()
        self.fields[number_offset] = (number_size, number_type)
    
    def extract(self, state, addr):
        raise NotImplemented()

    def __repr__(self):
        if len(self.fields) == 1 and 0 in self.fields:
            return '{}'.format(self.fields[0][1])
        else:
            return 'Struct: {}'.format(self.fields)