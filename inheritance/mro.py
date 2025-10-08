class GrandParent:
  def get_age():
    return 100

class Parent(GrandParent):
  pass

class Child(Parent):
  pass

print(Child.__mro__)
print(
  super(Parent, Child).get_age()
)
