from typing import overload
import ghidra.program.model.listing
import ghidra.util.datastruct.Duo
import java.lang


class FunctionComparisonModelListener(object):
    """
    Allows subscribers to register for FunctionComparisonModel changes
    """









    def activeFunctionChanged(self, side: ghidra.util.datastruct.Duo.Side, function: ghidra.program.model.listing.Function) -> None:
        """
        Notification that the selected function changed on one side or the other.
        @param side the side whose selected function changed
        @param function the new selected function for the given side
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def modelDataChanged(self) -> None:
        """
        Notification that the set of functions on at least one side changed. The selected functions
         on either side may have also changed.
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

