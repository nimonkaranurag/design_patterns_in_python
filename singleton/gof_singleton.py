class GangOfFour_Singleton:
    
    _instance = None

    def __init__(self):
        raise RuntimeError("Use the `get_instance` method for initializing instances.")
    
    @classmethod
    def get_instance(cls):
        
        if not cls._instance:
            cls._instance=cls.__new__(cls)
        
        return cls._instance

def main():

    obj_1 = GangOfFour_Singleton.get_instance()
    obj_2 = GangOfFour_Singleton.get_instance()

    assert obj_1 is obj_2

    print("success")

if __name__ == "__main__":
    main()
