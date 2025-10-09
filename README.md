# Python Notes

## Class Objects 

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


## The `super()` keyword

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


## Factory Method Pattern

- Suppose you have a collection of bullets you ship with your game:
  ```python
  fast_bullet = FastBullet()
  slow_bullet = SlowBullet()
  splash_bullet = SplashBullet()
  ```
  - Now, a customer request comes in for you to add a new bullet to the game, given the current design - the only way to do so would be:
    ```python
    (...)
    splash_bullet = SplashBullet()
    xxxx_bullet = xxxxBullet() # a new type of bullet
    ```
  - The obvious problem with this design is:
    - your code is *too aware* of the bullet types and is tightly coupled to it.
    - the solution is implementing a **Factory Method Pattern**.

- This is also a **creational** design pattern which abstracts the instance creation logic from the client.
- It provides a mechanism to create instances without exposing the actual logic.
- **Objects are created by calling a factory method instead of a constructor.**

## Builder Design Pattern

- Another **creational** design pattern, it encapsulates the logic for building complex objects; making it reusable.
- **What is a "complex object"?**
  - An object which has many distinct "parts" is called complex.
  - There exists well defined relationships between these parts.

- The principles behind this pattern are:
  - isolate/decouple the construction of a "complex" object.
  - design the construction process in a manner that enables creation of different representations of that object.

- Consider the following scenario: *You want to build a house for a video game.*
  - The house will have several different "parts"/components: a swimming pool, windows, roof, etc.
  - One option is to define a single class `House` which offers a constructor to set configurations for all of these parts:
    ```python
    my_house = House(
      walls = {
        "count": 2,
        "colour": "bold cyan",
      },
      (...)
    )
    # this is unreadable and difficult to maintain.
    # the crux of the problem is: `House` has the responsibility of creating itself through its constructor.
    ```
    - We want to decouple the creation of a new `House` instance from the `House` type itself -> provide an abstract respresentation of the **creation process**.
    - We do not want to let the object create itself.
  - Enter: **the builder pattern**!
    - a **builder** is an object that constructs other objects.
    - it assembles object "parts" to yield a final object representation.
    - For example, you can break down construction of `my_house` into a series of method calls:
      ```pseudo
      Step 1: build_walls()
      Step 2: build_pool()
      (...)
      ```
      - Now, you can "build" the `House` by calling *only the methods that you need*, getting a specific configuration of `House`.
      - `my_house_1` for example, could choose to have a pool, then it would call: `build_pool()` at some step. However, `my_house_2` may choose to build a `House` without a pool and it would simply skip the call to `build_pool()`.

## Adapter Design Pattern

- **Suppose the following situation:** you have a system component which generates data in an XML format which needs to be consumed by some other component; however, the second component only accepts serialized JSON => these formats are incompatible with each other!
  - One possible solution is rewriting one of the two components to enable data compatibility. However, this is not maintainable and violates the SOLID principles.
- **Scenario 2:** Suppose you have migrated a class `Rectangle`:
  *from*
    ```python
    Rectangle(x,y,width,height)
    ```
  *to*
    ```python
    Rectangle(x1,y1,x2,y2)
    ```
  - For backwards compatibility with legacy code an unelegant solution would be to re-write all of it so that it is compatible with the new constructor for `Rectangle`.

- To address these incompatibilities, we can use the **adapter design pattern!**
  - It is a design pattern used to **convert the interface contract of one class to be compatible with another class' interface contract.**
  - An **adapter** can convert source data into a format the client can understand.
    - In the first scenario, the adapter would convert XML -> JSON for consumption by the second component (the **adaptee**). This would be a *data adapter*.
    - In the second scenario, the adapter would similarly translate the new constructor interface for compatibility with legacy code. This would be an *interface adapter*.
  - An adapter thus enables two classes to work together which otherwise could not have because of differences in their expectations (incompatible interfaces).
  - It is a **structural pattern**.
  - Essentially we define a "wrapper" on the adaptee/incompatible object. So, you no longer nead to modify the internals of two incompatible interfaces.

## Strategy Pattern

- **Suppose:** You are designing a web scraper which should be agnostic to the data format it is scraping, that is, it should be able to scrape: JSON, XML, CSV - all popular data formats.
  - If you expand a single `Scraper` to accommodate all these formats using a switch case then: it will be difficult to maintain and will make this class over-bloated.
  - It will also violate the **Open/Closed principle** (open for extension and closed for modification) in case of future data sources that the `Scraper` should accommodate.
  - One other solution is: migrate all the extraction logic for each data type to a separate class and have the `Scraper` use their implementations as needed.
    - You could define a common `Handler` interface.
    - Each data type: CSV, XML, JSON, etc. will have a concrete implementation of the `Handler`.
    - The `Scraper` will use the corresponding concrete implementation when it encounters the respective type (e.g., a `JSONHandler` for JSON, an `SQLHandler` for SQL, etc.).
    - In this way, the exact implementation for extracting each data type is abstracted from the `Scraper`.

- The **Strategy pattern** is exactly this: "extract related algorithms into separate classes and define a common interface for them".
- **When to apply this approach?**
  - Your class <ins>has branching statements for different variants of the same algorithm</ins> (in the above scenario: the "data extraction algorithm").
  - You want to isolate the business logic of the class from implementations.
  - Use it within an object when you want the ability to <ins>switch between algorithms at runtime</ins> (it is not elegant if you have a big block of `if-else` statements, toggling variants of the algorithm).
- This is an example of a **behavioural design pattern**.

## Observer Pattern

- This is a **behavioural design pattern.**
- A simple publisher/subscriber model (or, "subject"/"observer(s)" model) where the publisher/"subject" notifies all subscribers/"observers" of any changes in its state.

## State Pattern

- An object has a <ins>finite number</ins> of "states".
- Each state is accompanied by a finite number of "actions" that can be performed on the object in that state.
- Each action results in a change in the object's state. So, performing an action causes a "transition" from one state to another.
- The "behaviour" of an object in any state encapsulates the "actions" it can perform in that state (these terms are used interchangeably in this context).
- The **state pattern** is a **behavioural design pattern** which allows an object to alter its behaviour *when its internal state changes* (when it transitions from one state to another because of some action).