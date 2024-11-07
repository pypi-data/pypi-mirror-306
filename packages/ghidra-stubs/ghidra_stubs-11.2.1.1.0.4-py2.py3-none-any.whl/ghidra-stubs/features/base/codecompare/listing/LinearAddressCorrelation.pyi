from typing import overload
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.util
import ghidra.util.datastruct.Duo
import java.lang


class LinearAddressCorrelation(object, ghidra.program.util.ListingAddressCorrelation):
    """
    Creates an address correlation with a simplistic correlation where each address correlates based
     on an offset from the address set's minimum address.
    """





    def __init__(self, comparisonData: ghidra.util.datastruct.Duo): ...



    def equals(self, __a0: object) -> bool: ...

    def getAddress(self, side: ghidra.util.datastruct.Duo.Side, otherAddress: ghidra.program.model.address.Address) -> ghidra.program.model.address.Address: ...

    def getAddresses(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.address.AddressSetView: ...

    def getClass(self) -> java.lang.Class: ...

    def getFunction(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Function: ...

    def getProgram(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Program: ...

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

