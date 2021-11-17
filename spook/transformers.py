class Transformer(object):
    mappings = {}
    value_mappings_functions = {}

    def __init__(self, initial_data):
        self.initial_data = initial_data

    def transform_dict(self, obj: dict):
        result = {}
        for k, v in obj.items():
            if k in self.mappings.keys():
                if k in self.value_mappings_functions.keys():
                    result[self.mappings.get(k)] = self.value_mappings_functions[k](v)
                else:
                    result[self.mappings.get(k)] = v

        return result

    def transform(self):
        if type(self.initial_data) == list:
            return [
                self.transform_dict(i)
                for i in self.initial_data
            ]
        return self.transform_dict(self.initial_data)
