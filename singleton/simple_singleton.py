class Simple_Singleton:

    _instance = None

    def __new__(cls):

        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

def main():

    s1 = Simple_Singleton()
    s2 = Simple_Singleton()

    assert s1 is s2

    print("success")

if __name__=="__main__":
    main()