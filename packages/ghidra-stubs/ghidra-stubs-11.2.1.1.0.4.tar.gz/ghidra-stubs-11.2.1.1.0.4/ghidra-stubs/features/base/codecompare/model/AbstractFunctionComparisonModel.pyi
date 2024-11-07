from typing import List
from typing import overload
import ghidra.features.base.codecompare.model
import ghidra.program.model.listing
import ghidra.util.datastruct
import ghidra.util.datastruct.Duo
import java.lang
import java.util


class AbstractFunctionComparisonModel(object, ghidra.features.base.codecompare.model.FunctionComparisonModel):
    """
    Base class for implementers of the FunctionComparisonModel. Provides listener support and
     tracking for the selected function for each side.
    """

    FUNCTION_COMPARATOR: java.util.Comparator



    def __init__(self): ...



    def addFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getActiveFunction(self, side: ghidra.util.datastruct.Duo.Side) -> ghidra.program.model.listing.Function: ...

    def getClass(self) -> java.lang.Class: ...

    def getFunctions(self, __a0: ghidra.util.datastruct.Duo.Side) -> List[object]: ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def removeFunction(self, __a0: ghidra.program.model.listing.Function) -> None: ...

    def removeFunctionComparisonModelListener(self, listener: ghidra.features.base.codecompare.model.FunctionComparisonModelListener) -> None: ...

    @overload
    def removeFunctions(self, __a0: ghidra.program.model.listing.Program) -> None: ...

    @overload
    def removeFunctions(self, __a0: java.util.Collection) -> None: ...

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