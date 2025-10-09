# Python Notes

### Class Objects 

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
- **In summary:**
  - `class.__new__` -> how to create the class object
  - `class.__init__` -> how to initialize class object(s) (how to instantiate a class?)
  - `class.__call__` -> the full pipeline of class object creation + initialization.


### The `super()` keyword

- The `super()` keyword returns a *proxy object* which *delegates method calls* to the next class in the **MRO(method resolution order)**.
- Python maintains an *ordered `tuple` of class objects* representing the "MRO" which the interpreter searches when it is looking for an executor of a method/function.
- For example:
```python
class Grandfather:
  pass

class Parent(Grandfather):
  pass

class Child(Parent):
  pass

print(Child.__mro__)
# Output:
# (<class '__main__.Child'>, <class '__main__.Parent'>, <class '__main__.Grandfather'>, <class 'object'>)
```
  - the MRO of a class includes the class itself.

- The `super()` keyword accepts two arguments:
  - `super(X,...)`: means "skip X and everything before it in the MRO"
  - `super(...,Y)`: means "use Y's MRO"
  - the important constraint here is: **Y must be a subclass of X or X itself** -> the second argument to `super(X,Y)` must be a subclass of the first or the class itself.
  - a valid interpretation of this is:
    - The Python interpreter first looks at the *second argument* passed using `super(...,Y)` and says: "okay, I need to use this object's MRO".
    - **Then**, the Python interpreter applies the "constraint" offered by the *first argument* to `super(X,...)` and says: "okay, now let me skip `X` and everything before it in the MRO of `Y`".
  - Another important note is `X` <ins>must be a class object</ins> of type `type`. `Y` can be: 
    - either `X` itself or a sub-class of `X` OR
    - an instance of `X` (or an instance of a sub-class of `X`).
    the idea is: `X` must appear in:
      - `Y.__mro__` if `Y` is a sub-class of `X`
      - `type(Y).__mro__` if `Y` is an instance of `X` or one of `X`'s subclasses.
  - Instances do not have MROs.
    For example:
      ```python
      class Dog:
        pass

      dog1=Dog()
      dog2=Dog()
      # doesn't make sense for dog1's MRO to be different from dog2's MRO.
      # instances do not have MROs -> it is a class object attribute.
      
      assert type(dog1).__mro__ == dog2.__class__.__mro__ # two ways of accessing an instance's MRO!
      assert type(dog1).__mro__ == Dog.__mro__ # Dog is a class and has an MRO
      ```
  - Instances and classes are different.

    For example:
      ```python
      class Animal:
        pass

      class Dog(Animal):
        pass

      dog = Dog()

      # these are instances
      assert isinstance(dog, Dog) # True
      assert isinstance(dog, Animal) # True

      # these are classes
      assert isinstance(Dog, type) # True
      assert not isinstance(Dog, Animal) # True

      # the MRO is strictly an inheritance chain
      assert issubclass(Dog, Animal) # True
      assert type(Dog) is type # True

      dog.__class__.__mro__ # this the Dog's MRO
      Dog.__class__.__mro__ # this is type's MRO
      ```

- In any class' MRO, the last item is **always:**
  ```python
  <class 'object'>
  ```
  - The root of ANY Python class' hierarchy is `object`.
  - Every Python class inherits from it.

- The MRO applies to both methods and class variables.
  - If Python does not hit a method or variable in the immediately next class object in the MRO, it searches the next one in the hierarchy till it is found.

- The MRO **is strictly an inheritance chain**, NOT an instantiation chain.
  - Metaclasses define rules for *instantiating* class objects. This is decoupled from inheritance.

## Singleton Design Pattern

- This is an **creational** design pattern dealing with how class objects are created.
- There are many ways to architecturally implement a Singleton design, however: the most efficient way to do so is by using a thread-safe metaclass implementation.


