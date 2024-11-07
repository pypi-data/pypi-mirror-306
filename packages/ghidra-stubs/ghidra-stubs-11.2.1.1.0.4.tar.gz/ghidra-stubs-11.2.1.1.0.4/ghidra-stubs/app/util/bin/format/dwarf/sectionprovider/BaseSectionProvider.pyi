from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf.sectionprovider
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class BaseSectionProvider(object, ghidra.app.util.bin.format.dwarf.sectionprovider.DWARFSectionProvider):
    """
    Fetches DWARF sections from a normal program using simple Ghidra memory blocks.
    """





    def __init__(self, program: ghidra.program.model.listing.Program): ...



    def close(self) -> None: ...

    @staticmethod
    def createSectionProviderFor(program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.sectionprovider.BaseSectionProvider: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getSectionAsByteProvider(self, sectionName: unicode, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.ByteProvider: ...

    def hasSection(self, sectionNames: List[unicode]) -> bool: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    def updateProgramInfo(self, __a0: ghidra.program.model.listing.Program) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

