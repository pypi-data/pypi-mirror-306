from inspect import stack


class Flags:
    def __init__(self, *flags):
        self.flags = flags
        for i, f in enumerate(self.flags):
            setattr(self, f, 2**i)

    def expose(self):
        stack()[1].frame.f_globals.update(self)

    def __iter__(self):
        return ((k, getattr(self, k)) for k in self.flags)

    def __str__(self):
        return 'Flags :\n\t'+'\n\t'.join(f'{k} = {v}' for k, v in self)

