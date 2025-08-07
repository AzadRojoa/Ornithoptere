class Gamepad:
    def __init__(self, inputs: dict) -> None:
        self.inputs = inputs

    def read(self) -> dict:
        values = {}
        for name, component in self.inputs.items():
            if hasattr(component, "read"):
                values[name] = component.read()
            elif hasattr(component, "value"):
                values[name] = component.value
            else:
                values[name] = str(component)
        return values
