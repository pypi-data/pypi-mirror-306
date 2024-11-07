from typing import List
from typing import overload
import ghidra.features.base.memsearch.bytesource
import ghidra.program.model.address
import java.lang


class AddressableByteSource(object):
    """
    Interface for reading bytes from a program. This provides a level of indirection for reading the
     bytes of a program so that the provider of the bytes can possibly do more than just reading the
     bytes from the static program. For example, a debugger would have the opportunity to refresh the
     bytes first.
 
     This interface also provides methods for determining what regions of memory can be queried and
     what addresses sets are associated with those regions. This would allow client to present choices
     about what areas of memory they are interested in AND are valid to be examined.
    """









    def equals(self, __a0: object) -> bool: ...

    def getBytes(self, address: ghidra.program.model.address.Address, bytes: List[int], length: int) -> int:
        """
        Retrieves the byte values for an address range.
        @param address The address of the first byte in the range
        @param bytes the byte array to store the retrieved byte values
        @param length the number of bytes to retrieve
        @return the number of bytes actually retrieved
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getSearchableRegions(self) -> List[ghidra.features.base.memsearch.bytesource.SearchRegion]:
        """
        Returns a list of memory regions where each region has an associated address set of valid
         addresses that can be read.
        @return a list of readable regions
        """
        ...

    def hashCode(self) -> int: ...

    def invalidate(self) -> None:
        """
        Invalidates any caching of byte values. This intended to provide a hint in debugging scenario
         that we are about to issue a sequence of byte value requests where we are re-acquiring
         previous requested byte values to look for changes.
        """
        ...

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