from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.util.search.memory
import java.lang


class MemSearchResult(object, java.lang.Comparable):
    """
    A class that represents a memory search hit at an address.
    """





    @overload
    def __init__(self, address: ghidra.program.model.address.Address, length: int): ...

    @overload
    def __init__(self, address: ghidra.program.model.address.Address, bytes: List[int]): ...



    def addressEquals(self, a: ghidra.program.model.address.Address) -> bool:
        """
        Returns true if the given address equals the address of this search result
        @param a the other address
        @return true if the given address equals the address of this search result
        """
        ...

    @overload
    def compareTo(self, o: ghidra.util.search.memory.MemSearchResult) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def getAddress(self) -> ghidra.program.model.address.Address: ...

    def getBytes(self) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def address(self) -> ghidra.program.model.address.Address: ...

    @property
    def bytes(self) -> List[int]: ...

    @property
    def length(self) -> int: ...