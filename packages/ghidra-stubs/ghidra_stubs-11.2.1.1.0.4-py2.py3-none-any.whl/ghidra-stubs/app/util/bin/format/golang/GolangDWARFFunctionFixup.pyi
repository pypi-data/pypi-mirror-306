from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.funcfixup
import java.lang


class GolangDWARFFunctionFixup(object, ghidra.app.util.bin.format.dwarf.funcfixup.DWARFFunctionFixup):
    """
    Fixups for golang functions found during DWARF processing.
 
     Fixes storage of parameters to match the go callspec and modifies parameter lists to match
     Ghidra's capabilities.
 
     Special characters used by golang in symbol names (middle dot ·, weird slash ∕) are 
     fixed up in DWARFProgram.getDWARFNameInfo() by calling 
     GoSymbolName.fixGolangSpecialSymbolnameChars().
 
     Go's 'unique' usage of DW_TAG_subroutine_type to define its ptr-to-ptr-to-func is handled in
     DWARFDataTypeImporter.makeDataTypeForFunctionDefinition().
 
    """

    GOLANG_API_EXPORT: ghidra.program.model.data.CategoryPath
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

    @staticmethod
    def isGolangFunction(dfunc: ghidra.app.util.bin.format.dwarf.DWARFFunction) -> bool:
        """
        Returns true if the specified {@link DWARFFunction} wrapper refers to a function in a golang
         compile unit.
        @param dfunc {@link DWARFFunction}
        @return boolean true or false
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

