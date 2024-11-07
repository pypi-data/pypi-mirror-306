from typing import overload
import ghidra.program.util
import ghidra.util.datastruct.Duo
import java.lang


class ProgramLocationTranslator(object):
    """
    Class for converting a program location from one program to another
    """





    def __init__(self, correlator: ghidra.program.util.ListingAddressCorrelation):
        """
        Constructor given a correlator for translating addresses
        @param correlator converts address from one program to another
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getProgramLocation(self, side: ghidra.util.datastruct.Duo.Side, otherSideLocation: ghidra.program.util.ProgramLocation) -> ghidra.program.util.ProgramLocation:
        """
        Converts a program location from the other side to the given side.
        @param side the side to get a location for
        @param otherSideLocation the location from the other side
        @return a program location for the given side that matches the other given location
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

