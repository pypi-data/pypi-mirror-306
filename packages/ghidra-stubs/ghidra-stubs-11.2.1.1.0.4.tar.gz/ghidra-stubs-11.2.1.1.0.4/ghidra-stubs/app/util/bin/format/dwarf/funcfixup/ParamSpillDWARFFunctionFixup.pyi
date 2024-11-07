from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.funcfixup
import java.lang


class ParamSpillDWARFFunctionFixup(object, ghidra.app.util.bin.format.dwarf.funcfixup.DWARFFunctionFixup):
    """
    Steal storage location from parameters that are defined in a function's local variable
     area, because the storage location isn't the parameter location during call, but its location
     after being spilled.
 
     Create a local variable at that storage location.
    """

    PRIORITY_LAST: int = 1000
    PRIORITY_NORMAL: int = 3000
    PRIORITY_NORMAL_EARLY: int = 4000
    PRIORITY_NORMAL_LATE: int = 2000



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findFixups() -> List[object]: ...

    def fixupDWARFFunction(self, dfunc: ghidra.app.util.bin.format.dwarf.DWARFFunction) -> None: ...

    def getClass(self) -> java.lang.Class: ...

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

