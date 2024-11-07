from typing import Iterator
from typing import overload
import ghidra.program.model.address
import ghidra.program.util
import java.lang
import java.util
import java.util.function


class ProgramSelection(object, ghidra.program.model.address.AddressSetView):
    """
    Class to define a selection for a program.
    """





    @overload
    def __init__(self):
        """
        Construct a new empty ProgramSelection.
        """
        ...

    @overload
    def __init__(self, addressFactory: ghidra.program.model.address.AddressFactory):
        """
        Construct a new empty ProgramSelection.
        @param addressFactory NOT USED
        @deprecated use {@link #ProgramSelection()}
        """
        ...

    @overload
    def __init__(self, setView: ghidra.program.model.address.AddressSetView):
        """
        Construct a new ProgramSelection
        @param setView address set for the selection
        """
        ...

    @overload
    def __init__(self, sel: ghidra.program.util.InteriorSelection):
        """
        Construct a new ProgramSelection from the indicated interior selection.
        @param sel the interior selection
        """
        ...

    @overload
    def __init__(self, from_: ghidra.program.model.address.Address, to: ghidra.program.model.address.Address):
        """
        Constructor.
        @param from the start of the selection
        @param to the end of the selection
        """
        ...

    @overload
    def __init__(self, addressFactory: ghidra.program.model.address.AddressFactory, setView: ghidra.program.model.address.AddressSetView):
        """
        Construct a new ProgramSelection
        @param addressFactory NOT USED
        @param setView address set for the selection
        @deprecated use {@link #ProgramSelection(AddressSetView)}
        """
        ...

    @overload
    def __init__(self, addressFactory: ghidra.program.model.address.AddressFactory, sel: ghidra.program.util.InteriorSelection):
        """
        Construct a new ProgramSelection from the indicated interior selection.
        @param addressFactory NOT USED
        @param sel the interior selection
        @deprecated use {@link #ProgramSelection(InteriorSelection)}s
        """
        ...

    @overload
    def __init__(self, addressFactory: ghidra.program.model.address.AddressFactory, from_: ghidra.program.model.address.Address, to: ghidra.program.model.address.Address):
        """
        Constructor.
        @param addressFactory NOT USED
        @param from the start of the selection
        @param to the end of the selection
        """
        ...

    def __iter__(self): ...

    @overload
    def contains(self, addr: ghidra.program.model.address.Address) -> bool: ...

    @overload
    def contains(self, rangeSet: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def contains(self, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> bool: ...

    def equals(self, obj: object) -> bool: ...

    def findFirstAddressInCommon(self, set: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.Address: ...

    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    def getAddressCountBefore(self, __a0: ghidra.program.model.address.Address) -> long: ...

    @overload
    def getAddressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, atStart: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, start: ghidra.program.model.address.Address, forward: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddresses(self, forward: bool) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getAddresses(self, start: ghidra.program.model.address.Address, forward: bool) -> ghidra.program.model.address.AddressIterator: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getInteriorSelection(self) -> ghidra.program.util.InteriorSelection:
        """
        Get the interior selection.
        @return null if there is no interior selection
        """
        ...

    def getLastRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getNumAddressRanges(self) -> int: ...

    def getNumAddresses(self) -> long: ...

    def getRangeContaining(self, address: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressRange: ...

    def hasSameAddresses(self, asv: ghidra.program.model.address.AddressSetView) -> bool:
        """
        Returns true if and only if this set and the given
         address set contains exactly the same addresses.
        @param asv the address set to compare with this one.
        @return true if the specified set has the same addresses.
        """
        ...

    def hashCode(self) -> int: ...

    def intersect(self, view: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

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

    def spliterator(self) -> java.util.Spliterator: ...

    def subtract(self, view: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    def toString(self) -> unicode: ...

    @staticmethod
    def trimEnd(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    @staticmethod
    def trimStart(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    def union(self, view: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def xor(self, view: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @property
    def addressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @property
    def empty(self) -> bool: ...

    @property
    def firstRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def interiorSelection(self) -> ghidra.program.util.InteriorSelection: ...

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