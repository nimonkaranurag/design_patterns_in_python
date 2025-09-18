# Python Notes

- Python doesn’t have a single Java-style constructor. Instead it splits responsibilities into:
`__new__` = creation (the true constructor; returns the new object)
`__init__` = initialization (configures the already-created object)

- It decouples: *object creation* from *object initialization*.
- When the Python interpreter encounters a statement like: `f = Foo()` it translates it to: `type.__call__(Foo, *args, **kwargs)`.
- The `__call__()` method of the `type` metaclass looks something like this:
```python
def __call__(cls,*args,**kwargs):
    # create the class object
    obj = cls.__new__(cls,*args,**kwargs)

    # verify that the object created belongs to that class
    if isinstance(obj,cls):
        # initialize the object
        cls.__init__(obj,*args,**kwargs)
    
    return obj # return the created object
```
- However, every class in Python itself is an object and uses the `type` "metaclass" for instatiating itself.
- A `metaclass` in Python describes the rules for creating and initializing classes (as objects) and their instances.
- A metaclass controls:
  - Class creation (`metaclass.__new__ / metaclass.__init__`) — i.e., how the class object itself is built when `class Foo: ...` is executed.
  - Optionally, the instance creation pipeline via `metaclass.__call__`(which orchestrates `cls.__new__` -> `cls.__init__`).

- In layman terms, `metaclass.__new__` and `metaclass.__init__` -> how do you create a class object? and `metaclass.__call__` -> the pipeline for creating instances (objects) of that class object! 
- Then, `class.__new__` and `class.__init__` -> how do you create an instance *of a class "object"*?


## Singleton Design Pattern

- This is an **creational** design pattern dealing with how class objects are created.
