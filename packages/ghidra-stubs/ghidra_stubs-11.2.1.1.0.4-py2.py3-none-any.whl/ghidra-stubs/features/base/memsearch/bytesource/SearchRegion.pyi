from typing import overload
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang


class SearchRegion(object):
    """
    Interface to specify a named region within a byte source (Program) that users can select to
     specify AddressSetViews that can be searched.
    """









    def equals(self, __a0: object) -> bool: ...

    def getAddresses(self, program: ghidra.program.model.listing.Program) -> ghidra.program.model.address.AddressSetView:
        """
        Returns the set of addresses from a specific program that is associated with this region.
        @param program the program that determines the specific addresses for a named region
        @return the set of addresses for this region as applied to the given program
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode:
        """
        Returns a description of the region.
        @return a description of the region
        """
        ...

    def getName(self) -> unicode:
        """
        The name of the region.
        @return the name of the region
        """
        ...

    def hashCode(self) -> int: ...

    def isDefault(self) -> bool:
        """
        Returns true if this region should be included in the default selection of which regions to
         search.
        @return true if this region should be selected by default
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
    def default(self) -> bool: ...

    @property
    def description(self) -> unicode: ...

    @property
    def name(self) -> unicode: ...