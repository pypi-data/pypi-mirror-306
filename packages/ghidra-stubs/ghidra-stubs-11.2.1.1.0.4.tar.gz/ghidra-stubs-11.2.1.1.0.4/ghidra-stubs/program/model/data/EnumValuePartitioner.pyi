from typing import List
from typing import overload
import ghidra.program.model.data
import java.lang


class EnumValuePartitioner(object):
    """
    This is a static utility class used to partition a set of long values into as many
     non-intersecting BitGroups as possible.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def partition(values: List[long], size: int) -> List[ghidra.program.model.data.BitGroup]:
        """
        Partition the given values into a list of non-intersecting BitGroups.
        @param values the values to be partitioned.
        @param size size of enum value in bytes
        @return a list of BitGroups with non-intersecting bits.
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

