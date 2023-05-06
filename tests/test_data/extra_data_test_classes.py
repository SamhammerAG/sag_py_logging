from attrs import define


class NotSerializableClass:
    def __init__(self, testtext: str) -> None:
        self.testtext: str = testtext


@define
class ClassWithoutDict:
    x: int
    y: int
