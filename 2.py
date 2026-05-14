class ValidatedField:
    def __init__(self, expected_type, min_value=None, max_value=None):
        self.type, self.min, self.max = expected_type, min_value, max_value

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name) if obj else self

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Очікувався {self.type}, отримано {type(value)}")
        if (self.min and value < self.min) or (self.max and value > self.max):
            raise ValueError(f"Значення {value} поза діапазоном [{self.min}, {self.max}]")
        setattr(obj, self.private_name, value)

class ConfigSection:
    _sections = {}
    def __init_subclass__(cls, section_name, **kwargs):
        super().__init_subclass__(**kwargs)
        ConfigSection._sections[section_name] = cls

class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, 1, 65535)
    def __init__(self, host, port): self.host, self.port = host, port

def main():
    db = DatabaseConfig("localhost", 5432)
    print(f"DB Config: {db.host}:{db.port}")
    try: db.port = 70000 
    except ValueError as e: print(f"Валідація: {e}")

if __name__ == "__main__": main()
