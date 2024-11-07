from typing import Iterator
from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang
import java.util
import java.util.function


class AddressSet(object, ghidra.program.model.address.AddressSetView):
    """
    Class for storing sets of addresses.  This implementation uses a red-black tree where each
     entry node in the tree stores an address range.  The key for an entry node is the minimum address
     of the range and the value is the maximum address of the range.
    """





    @overload
    def __init__(self):
        """
        Create a new empty Address Set.
        """
        ...

    @overload
    def __init__(self, addr: ghidra.program.model.address.Address):
        """
        Create a new Address containing a single address.
        @param addr the address to be included in this address set.
        """
        ...

    @overload
    def __init__(self, range: ghidra.program.model.address.AddressRange):
        """
        Create a new Address Set from an address range.
        @param range the range of addresses to include in this set.
        """
        ...

    @overload
    def __init__(self, set: ghidra.program.model.address.AddressSetView):
        """
        Create a new Address Set from an existing Address Set.
        @param set Existing Address Set to clone.
        """
        ...

    @overload
    def __init__(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address):
        """
        Creates a new Address set containing a single range
         The specified start and end addresses must form a valid range within
         a single {@link AddressSpace}.
        @param start the start address of the range
        @param end the end address of the range
        @throws IllegalArgumentException if the start and end addresses are in different spaces.  To
         avoid this, use the constructor  {@link #AddressSet(Program, Address, Address)}
        """
        ...

    @overload
    def __init__(self, program: ghidra.program.model.listing.Program, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address):
        """
        Creates a new Address set containing a single range.
         Use of this method is generally discouraged since the set of addresses between a start and
         end address not contained within the same {@link AddressSpace} may be contain unexpected 
         memory regions.
        @param start the start address of the range
        @param end the end address of the range
        @param program the program whose AddressFactory is used to resolve address ranges where the
         start and end are in different address spaces. If you use the constructor with just the
         start and end address and the addresses are in different spaces, you would get an
         IllegalArgumentException.
        """
        ...

    def __iter__(self): ...

    @overload
    def add(self, address: ghidra.program.model.address.Address) -> None:
        """
        Adds the given address to this set.
        @param address the address to add
        """
        ...

    @overload
    def add(self, range: ghidra.program.model.address.AddressRange) -> None:
        """
        Add an address range to this set.
        @param range the range to add.
        """
        ...

    @overload
    def add(self, addressSet: ghidra.program.model.address.AddressSetView) -> None:
        """
        Add all addresses of the given AddressSet to this set.
        @param addressSet set of addresses to add.
        """
        ...

    @overload
    def add(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None:
        """
        Adds the range to this set
        @param start the start address of the range to add
        @param end the end address of the range to add
        """
        ...

    @overload
    def addRange(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None:
        """
        Adds the range to this set
        @param start the start address of the range to add
        @param end the end address of the range to add
        @throws IllegalArgumentException if the start and end addresses are in different spaces.  To
         avoid this, use the constructor  {@link #addRange(Program, Address, Address)}
        """
        ...

    @overload
    def addRange(self, program: ghidra.program.model.listing.Program, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None:
        """
        Adds a range of addresses to this set.
        @param program program whose AddressFactory is used to resolve address ranges that span
         multiple address spaces.
        @param start the start address of the range to add
        @param end the end address of the range to add
        """
        ...

    def clear(self) -> None:
        """
        Removes all addresses from the set.
        """
        ...

    @overload
    def contains(self, address: ghidra.program.model.address.Address) -> bool: ...

    @overload
    def contains(self, addrSet: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def contains(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> bool: ...

    @overload
    def delete(self, range: ghidra.program.model.address.AddressRange) -> None:
        """
        Deletes an address range from this set.
        @param range AddressRange to remove from this set
        """
        ...

    @overload
    def delete(self, addressSet: ghidra.program.model.address.AddressSetView) -> None:
        """
        Delete all addresses in the given AddressSet from this set.
        @param addressSet set of addresses to remove from this set.
        """
        ...

    @overload
    def delete(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None:
        """
        Deletes a range of addresses from this set
        @param start the starting address of the range to be removed
        @param end the ending address of the range to be removed (inclusive)
        """
        ...

    def deleteFromMin(self, toAddr: ghidra.program.model.address.Address) -> None:
        """
        Delete all addresses from the minimum address in the set up to and including toAddr.
         Addresses less-than-or-equal to specified 
         address based upon {@link Address} comparison.
        @param toAddr only addresses greater than toAddr will be left in the set.
        """
        ...

    def deleteRange(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None:
        """
        Deletes a range of addresses from this set
        @param start the starting address of the range to be removed
        @param end the ending address of the range to be removed
        """
        ...

    def deleteToMax(self, fromAddr: ghidra.program.model.address.Address) -> None:
        """
        Delete all addresses starting at the fromAddr to the maximum address in the set.
         Addresses greater-than-or-equal to specified 
         address based upon {@link Address} comparison.
        @param fromAddr only addresses less than fromAddr will be left in the set.
        """
        ...

    def equals(self, obj: object) -> bool: ...

    def findFirstAddressInCommon(self, set: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.Address: ...

    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    def getAddressCountBefore(self, __a0: ghidra.program.model.address.Address) -> long: ...

    @overload
    def getAddressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, forward: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, start: ghidra.program.model.address.Address, forward: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddresses(self, forward: bool) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getAddresses(self, start: ghidra.program.model.address.Address, forward: bool) -> ghidra.program.model.address.AddressIterator: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getLastRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getNumAddressRanges(self) -> int: ...

    def getNumAddresses(self) -> long: ...

    def getRangeContaining(self, address: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressRange: ...

    def hasSameAddresses(self, addrSet: ghidra.program.model.address.AddressSetView) -> bool: ...

    def hashCode(self) -> int: ...

    def intersect(self, addrSet: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    def intersectRange(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSet: ...

    @overload
    def intersects(self, addrSet: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def intersects(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> bool: ...

    def isEmpty(self) -> bool: ...

    @overload
    def iterator(self) -> Iterator[ghidra.program.model.address.AddressRange]: ...

    @overload
    def iterator(self, forward: bool) -> Iterator[ghidra.program.model.address.AddressRange]: ...

    @overload
    def iterator(self, start: ghidra.program.model.address.Address, forward: bool) -> Iterator[ghidra.program.model.address.AddressRange]: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def printRanges(self) -> unicode:
        """
        Returns a string displaying the ranges in this set.
        @return a string displaying the ranges in this set.
        """
        ...

    def spliterator(self) -> java.util.Spliterator: ...

    def subtract(self, addrSet: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    def toList(self) -> List[ghidra.program.model.address.AddressRange]:
        """
        Returns a list of the AddressRanges in this set.
        @return a list of the AddressRanges in this set.
        """
        ...

    def toString(self) -> unicode: ...

    @staticmethod
    def trimEnd(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    @staticmethod
    def trimStart(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    def union(self, addrSet: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def xor(self, addrSet: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @property
    def addressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @property
    def empty(self) -> bool: ...

    @property
    def firstRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def lastRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def numAddressRanges(self) -> int: ...

    @property
    def numAddresses(self) -> long: ...