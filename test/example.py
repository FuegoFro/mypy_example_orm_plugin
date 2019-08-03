from typing import Type, ClassVar, List


class MyClass:
    pass


class BaseField:
    instance_type: ClassVar[Type[object]]


class IntType(BaseField):
    instance_type = int


class StringType(BaseField):
    instance_type = str


class MyClassType(BaseField):
    instance_type = MyClass


class ListIntType(BaseField):
    instance_type = List[int]


class BaseModel:
    pass


class Model(BaseModel):
    foo = ListIntType()
    bar = StringType()
    baz = MyClassType()


reveal_type(Model.foo)
reveal_type(Model.bar)
reveal_type(Model.baz)


m: Model = Model()
x = "a"
x = m.foo
x = m.bar
reveal_type(m.foo)
reveal_type(m.bar)
reveal_type(m.baz)
