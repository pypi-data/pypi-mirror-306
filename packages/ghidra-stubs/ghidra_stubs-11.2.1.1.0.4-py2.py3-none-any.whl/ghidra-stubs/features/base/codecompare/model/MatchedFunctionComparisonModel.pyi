from typing import List
from typing import overload
import ghidra.features.base.codecompare.model
import ghidra.program.model.listing
import ghidra.util.datastruct.Duo
import java.lang
import java.util


class MatchedFunctionComparisonModel(ghidra.features.base.codecompare.model.AbstractFunctionComparisonModel):
    """
    A FunctionComparisonModel comprised of matched pairs of source and target functions. Each
     source function has its own set of target functions that it can be compared with.
    """





    def __init__(self): ...



    def addFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None: ...

    def addMatch(self, sourceFunction: ghidra.program.model.listing.Function, targetFunction: ghidra.program.model.listing.Function) -> None:
        """
        Adds a new comparison to the model. If the sourceFunction already exists on the left side,
         then the target function will be added to that specific function's right side functions. 
         Otherwise, the source function will be added to the left side the given target as its only
         right side function.
        @param sourceFunction the left side function to add
        @param targetFunction the right side function to add for that source function
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getActiveFunction(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Function: ...

    def getClass(self) -> java.lang.Class: ...

    def getFunctions(self, side: ghidra.util.datastruct.Duo.Side) -> List[ghidra.program.model.listing.Function]: ...

    def getSourceFunctions(self) -> List[ghidra.program.model.listing.Function]: ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def removeFunction(self, function: ghidra.program.model.listing.Function) -> None:
        """
        Removes the given function from all comparisons in the model, whether
         stored as a source or target
        @param function the function to remove
        """
        ...

    def removeFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None: ...

    @overload
    def removeFunctions(self, program: ghidra.program.model.listing.Program) -> None:
        """
        Removes all functions in the model that come from the given
         program
        @param program the program to remove functions from
        """
        ...

    @overload
    def removeFunctions(self, functions: java.util.Collection) -> None:
        """
        Removes all the given functions from all comparisons in the model
        @param functions the functions to remove
        """
        ...

    def setActiveFunction(self, side: ghidra.util.datastruct.Duo.Side, function: ghidra.program.model.listing.Function) -> bool: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def empty(self) -> bool: ...

    @property
    def sourceFunctions(self) -> List[object]: ...