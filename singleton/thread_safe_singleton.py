import threading

class ThreadSafeSingleton:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        with cls._lock:

            if not cls._instance:
                cls._instance = super().__new__(cls)
            
        return cls._instance

def main():

    s1 = ThreadSafeSingleton()
    s2 = ThreadSafeSingleton()

    assert s1 is s2

    print("success")

if __name__=="__main__":
    main()