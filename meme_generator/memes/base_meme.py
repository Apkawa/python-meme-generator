

class BaseMeme:
    name: str

    def render(self, *args, **kwargs):
        raise NotImplementedError()