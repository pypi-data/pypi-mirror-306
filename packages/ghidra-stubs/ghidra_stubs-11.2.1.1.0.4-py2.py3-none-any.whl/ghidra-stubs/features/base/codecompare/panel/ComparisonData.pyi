from typing import overload
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang


class ComparisonData(object):
    """
    ComparisonData is an abstract of items that can be compared in a CodeComparisonPanel. 
     Not all comparison panels can handle all types of comparison data. For example, the decompiler
     comparison only works when the comparison data is a function.
    """

    EMPTY: ghidra.features.base.codecompare.panel.ComparisonData
    FG_COLOR_TITLE: java.awt.Color







    def equals(self, __a0: object) -> bool: ...

    def getAddressSet(self) -> ghidra.program.model.address.AddressSetView:
        """
        Returns the set of addresses being compared. Currently, all comparisons are address based,
         so this should never be null.
        @return the set of addresses being compared
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode:
        """
        Returns a description of the data being compared.
        @return a description of the data being compared.
        """
        ...

    def getFunction(self) -> ghidra.program.model.listing.Function:
        """
        Returns the function being compared or null if this comparison data is not function based.
        @return the function being compared or null if this comparison data is not function based
        """
        ...

    def getProgram(self) -> ghidra.program.model.listing.Program:
        """
        Returns the program containing the data being compared.
        @return the program containing the data being compared.
        """
        ...

    def getShortDescription(self) -> unicode:
        """
        Returns a short description (useful for tab name)
        @return a short description
        """
        ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool:
        """
        Returns true if this comparison has no addresses to compare
        @return true if this comparison has no addresses to compare
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
    def addressSet(self) -> ghidra.program.model.address.AddressSetView: ...

    @property
    def description(self) -> unicode: ...

    @property
    def empty(self) -> bool: ...

    @property
    def function(self) -> ghidra.program.model.listing.Function: ...

    @property
    def program(self) -> ghidra.program.model.listing.Program: ...

    @property
    def shortDescription(self) -> unicode: ...