class Scope:
    def __init__(self, parent_scope = None):
        self.variables = {}
        self.parent_scope = parent_scope

    def get(self, name):
        if type(name) != str:
            return name
        if name in self.variables:
            return self.variables[name]
        elif self.parent_scope:
            return self.parent_scope.get(name)
        return None

    def set(self, name, value):
        if name in self.variables:
            # throw an err
            raise Exception(f"Variable `{name}` already exists in scope")
        self.variables[name] = value