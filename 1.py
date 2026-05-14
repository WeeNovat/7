import hashlib

class PluginMeta(type):
    _registry = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if bases:  
            for attr in mcs.REQUIRED_ATTRS:
                if attr not in attrs:
                    raise TypeError(f"Плагін {name} має містити атрибут '{attr}'")
            mcs._registry[attrs["name"]] = cls
        return cls

    @classmethod
    def get_registry(mcs): return mcs._registry.copy()

    @classmethod
    def create_plugin(mcs, name):
        if name not in mcs._registry: raise ValueError(f"Плагін {name} не знайдено")
        return mcs._registry[name]()

class BasePlugin(metaclass=PluginMeta): pass

class UpperPlugin(BasePlugin):
    name, version = "upper", "1.0"
    def execute(self, data): return data.upper()


HashPlugin = type("HashPlugin", (BasePlugin,), {
    "name": "hash", "version": "2.0",
    "execute": lambda self, data: hashlib.md5(data.encode()).hexdigest()
})

def main():
    print("Зареєстровані плагіни:")
    for name, cls in PluginMeta.get_registry().items():
        print(f"  {name} (v{cls.version})")
    
    test_str = "Привіт Світ"
    p = PluginMeta.create_plugin("hash")
    print(f"Hash '{test_str}': {p.execute(test_str)}")

if __name__ == "__main__": main()
