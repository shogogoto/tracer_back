
class VarGenerator:
    __count:int = 0

    @classmethod
    def generate(cls)->str:
        var = f"gen_var_{cls.__count}"
        cls.__count += 1
        return var
