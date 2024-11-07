from typing import overload
import java.lang
import java.util.stream


class AddressCollectors(object):
    """
    Utilities for using addresses and ranges in streams
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def toAddressSet() -> java.util.stream.Collector:
        """
        Union a stream of address ranges into a single mutable address set
        @return the address set
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

