from typing import overload
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.util.datastruct.Duo
import java.lang


class ListingAddressCorrelation(object):
    """
    This is the interface for a correlator that associates addresses from one program with
     addresses from another program or it can associate addresses from one part of a program 
     with addresses from another part of the same program. Given an address from one program, it
     can provide the corresponding address for the other program. The two programs are referred to
     as the LEFT program and the RIGHT program. See ghidra.util.datastruct.Duo.Side
    """









    def equals(self, __a0: object) -> bool: ...

    def getAddress(self, side: ghidra.util.datastruct.Duo.Side, otherSideAddress: ghidra.program.model.address.Address) -> ghidra.program.model.address.Address:
        """
        Gets the address for the given side that matches the given address from the other side.
        @param side the side to get an address for
        @param otherSideAddress the address from the other side to find a match for
        @return the address for the given side that matches the given address from the other side.
        """
        ...

    def getAddresses(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.address.AddressSetView:
        """
        Gets the addresses that are part of the correlator for the given side
        @param side LEFT or RIGHT
        @return the addresses that are part of the correlator for the given side
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getFunction(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Function:
        """
        Gets the function for the given side. This will be null if the addresses are not function
         based.
        @param side LEFT or RIGHT
        @return the function for the given side or null if not function based
        """
        ...

    def getProgram(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Program:
        """
        Gets the program for the given side.
        @param side LEFT or RIGHT
        @return the program for the given side
        """
        ...

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

