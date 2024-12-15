class Test():
    def __init__(self):
        self.child =  None

    def update(self):
        if self.child is None:
            print("\tUpdating node...")
            print(f"\tOld object: {self}")
            self = Test() # new test object
            print(f"\tNew object: {self}")
        else:
            self.child.update()


test_parent = Test()
test_parent.child = Test()
print(f"Parent obj: {test_parent} || child obj: {test_parent.child}")
test_parent.update()
print(f"Parent obj: {test_parent} || child obj: {test_parent.child}")