class Item:
    def __init__(self, use_function=None, power=0, **kwargs):
        self.use_function = use_function
        self.power = power
        self.function_kwargs = kwargs
