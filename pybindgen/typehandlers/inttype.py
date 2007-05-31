# docstrings not neede here (the type handler interfaces are fully
# documented in base.py) pylint: disable-msg=C0111

from base import ReturnValue, Parameter,\
     ReverseWrapperBase, ForwardWrapperBase


class IntParam(Parameter):

    DIRECTIONS = [Parameter.DIRECTION_IN]
    CTYPES = ['int']

    def convert_c_to_python(self, wrapper):
        assert isinstance(wrapper, ReverseWrapperBase)
        wrapper.build_params.add_parameter('i', [self.name])

    def convert_python_to_c(self, wrapper):
        assert isinstance(wrapper, ForwardWrapperBase)
        name = wrapper.declarations.declare_variable(self.ctype, self.name)
        wrapper.parse_params.add_parameter('i', ['&'+name], self.name)
        wrapper.call_params.append(name)


class IntReturn(ReturnValue):

    CTYPES = ['int']

    def get_c_error_return(self):
        return "return INT_MIN;"
    
    def convert_python_to_c(self, wrapper):
        wrapper.parse_params.add_parameter("i", ["&retval"], prepend=True)

    def convert_c_to_python(self, wrapper):
        wrapper.build_params.add_parameter("i", ["retval"], prepend=True)


class IntPtrParam(Parameter):

    DIRECTIONS = [Parameter.DIRECTION_IN, Parameter.DIRECTION_OUT,
                  Parameter.DIRECTION_IN|Parameter.DIRECTION_OUT]
    CTYPES = ['int*']
    
    def convert_c_to_python(self, wrapper):
        if self.direction & self.DIRECTION_IN:
            wrapper.build_params.add_parameter('i', ['*'+self.name])
        if self.direction & self.DIRECTION_OUT:
            wrapper.parse_params.add_parameter("i", [self.name], self.name)

    def convert_python_to_c(self, wrapper):
        assert self.ctype == 'int*'
        name = wrapper.declarations.declare_variable(self.ctype[:-1], self.name)
        wrapper.call_params.append('&'+name)
        if self.direction & self.DIRECTION_IN:
            wrapper.parse_params.add_parameter('i', ['&'+name], self.name)
        if self.direction & self.DIRECTION_OUT:
            wrapper.build_params.add_parameter("i", [name])
        


class IntRefParam(Parameter):

    DIRECTIONS = [Parameter.DIRECTION_IN, Parameter.DIRECTION_OUT,
                  Parameter.DIRECTION_IN|Parameter.DIRECTION_OUT]
    CTYPES = ['int&']
    
    def convert_c_to_python(self, wrapper):
        if self.direction & self.DIRECTION_IN:
            wrapper.build_params.add_parameter('i', [self.name])
        if self.direction & self.DIRECTION_OUT:
            wrapper.parse_params.add_parameter("i", [self.name], self.name)

    def convert_python_to_c(self, wrapper):
        assert self.ctype == 'int&'
        name = wrapper.declarations.declare_variable(self.ctype[:-1], self.name)
        wrapper.call_params.append(name)
        if self.direction & self.DIRECTION_IN:
            wrapper.parse_params.add_parameter('i', ['&'+name], self.name)
        if self.direction & self.DIRECTION_OUT:
            wrapper.build_params.add_parameter("i", [name])