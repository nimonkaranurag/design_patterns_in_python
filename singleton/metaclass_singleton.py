class SingletonMeta(type):

    _instances = {}

    def __call__(cls):

        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(cls)
        
        return cls._instances[cls]
    

class Singleton(metaclass=SingletonMeta):

    def business_logic(self):
        print("executing some business logic.")
    
def main():

    s1 = Singleton()
    s2 = Singleton()

    assert s1 is s2
    
    print("success")

if __name__=="__main__":
    main()
