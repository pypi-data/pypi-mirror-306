from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.funcfixup
import ghidra.util.classfinder
import java.lang


class DWARFFunctionFixup(ghidra.util.classfinder.ExtensionPoint, object):
    """
    Interface for add-in logic to fix/modify/tweak DWARF functions before they are written 
     to the Ghidra program.
 
     Use  to
     control the order of evaluation (higher numbers are run earlier).
 
     Fixups are found using ClassSearcher, and their class names must end
     in "DWARFFunctionFixup" (see ExtensionPoint.manifest). 
 
     Instance lifetime:
 
     New instances are not shared between programs or analysis sessions, but will be re-used to
     handle the various functions found in a single binary.
  
     If the implementation also implements Closeable, it will be called when the fixup
     is no longer needed.
    """

    PRIORITY_LAST: int = 1000
    PRIORITY_NORMAL: int = 3000
    PRIORITY_NORMAL_EARLY: int = 4000
    PRIORITY_NORMAL_LATE: int = 2000







    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findFixups() -> List[ghidra.app.util.bin.format.dwarf.funcfixup.DWARFFunctionFixup]:
        """
        Return a list of all current {@link DWARFFunctionFixup fixups} found in the classpath
         by ClassSearcher.
        @return list of all current fixups found in the classpath
        """
        ...

    def fixupDWARFFunction(self, dfunc: ghidra.app.util.bin.format.dwarf.DWARFFunction) -> None:
        """
        Called before a {@link DWARFFunction} is used to create a Ghidra Function.
         <p>
         If processing of the function should terminate (and the function be skipped), throw
         a {@link DWARFException}.
        @param dfunc {@link DWARFFunction} info read from DWARF about the function
        """
        ...

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

