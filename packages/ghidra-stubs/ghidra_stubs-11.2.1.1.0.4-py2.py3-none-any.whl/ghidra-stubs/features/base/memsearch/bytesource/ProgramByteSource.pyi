from typing import List
from typing import overload
import ghidra.features.base.memsearch.bytesource
import ghidra.program.model.address
import java.lang


class ProgramByteSource(object, ghidra.features.base.memsearch.bytesource.AddressableByteSource):
    """
    AddressableByteSource implementation for a Ghidra Program
    """





    def __init__(self, program: ghidra.program.model.listing.Program): ...



    def equals(self, __a0: object) -> bool: ...

    def getBytes(self, address: ghidra.program.model.address.Address, bytes: List[int], length: int) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getSearchableRegions(self) -> List[ghidra.features.base.memsearch.bytesource.SearchRegion]: ...

    def hashCode(self) -> int: ...

    def invalidate(self) -> None: ...

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
    def searchableRegions(self) -> List[object]: ...