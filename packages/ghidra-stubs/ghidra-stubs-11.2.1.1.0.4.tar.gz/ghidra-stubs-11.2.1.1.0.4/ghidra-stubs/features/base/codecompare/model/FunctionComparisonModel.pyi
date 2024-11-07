from typing import List
from typing import overload
import ghidra.features.base.codecompare.model
import ghidra.program.model.listing
import ghidra.util.datastruct.Duo
import java.lang
import java.util


class FunctionComparisonModel(object):
    """
    A model for comparing one or more functions in a side by side display. The model supports the
     concept of a set of function that can be selected for each side of the comparison. It also 
     maintains the selected function for each side. The default model simply has a single set
     of functions that can be selected for either side of the comparison. The model supports the
     concept of different sets of functions for each and even the idea the the active function for
     one side can determine the set of functions for the other side. See 
     MatchedFunctionComparisonModel.
 
     This model is intended to be used by the the FunctionComparisonService to generate
     a function comparison display window. 
 
     Note: Subscribers may register to be informed of changes to this model via the
     FunctionComparisonModelListener interface.
    """









    def addFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None:
        """
        Adds the given listener to the list of those to be notified of model changes.
        @param listener the listener to add
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getActiveFunction(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Function:
        """
        Returns the active (selected) function for the given side.
        @param side the side to get the active function for
        @return the active function for the given side
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getFunctions(self, side: ghidra.util.datastruct.Duo.Side) -> List[ghidra.program.model.listing.Function]:
        """
        Returns the list of all functions on the given side that could be made active.
        @param side the side to get functions for
        @return the list of all functions on the given side that could be made active
        """
        ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool:
        """
        Returns true if the model has no function to compare.
        @return true if the model has no functions to compare
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def removeFunction(self, function: ghidra.program.model.listing.Function) -> None:
        """
        Removes the given function from both sides of the comparison.
        @param function the function to remove
        """
        ...

    def removeFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None:
        """
        Removes the given listener from the list of those to be notified of model changes.
        @param listener the listener to remove
        """
        ...

    @overload
    def removeFunctions(self, program: ghidra.program.model.listing.Program) -> None:
        """
        Removes all functions from the given program from both sides of the comparison
        @param program that program whose functions should be removed from this model
        """
        ...

    @overload
    def removeFunctions(self, functions: java.util.Collection) -> None:
        """
        Removes all the given functions from both sides of the comparison.
        @param functions the functions to remove
        """
        ...

    def setActiveFunction(self, side: ghidra.util.datastruct.Duo.Side, function: ghidra.program.model.listing.Function) -> bool:
        """
        Sets the function for the given side. The function must be one of the functions from that
         side's set of functions
        @param side the side to set the function for
        @param function the function so set for the given side
        @return true if the function was made active or false if the function does not exist for the
         given side
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def empty(self) -> bool: ...