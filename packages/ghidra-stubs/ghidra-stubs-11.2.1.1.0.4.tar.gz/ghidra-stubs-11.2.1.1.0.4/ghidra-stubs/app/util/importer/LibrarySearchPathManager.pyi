from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.importer
import ghidra.formats.gfilesystem
import ghidra.util.task
import java.lang


class LibrarySearchPathManager(object):
    """
    A simple class for managing the library search path and avoiding duplicate directories.
    """









    @staticmethod
    def addPath(path: unicode) -> bool:
        """
        Adds the specified library search path path to the end of the path search list
        @param path the library search path to add
        @return true if the path was appended, false if the path was a duplicate
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getLibraryFsrlList(provider: ghidra.app.util.bin.ByteProvider, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> List[ghidra.formats.gfilesystem.FSRL]:
        """
        Returns a {@link List} of {@link FSRL}s to search for libraries
        @param provider The {@link ByteProvider} of the program being loaded
        @param log The log
        @param monitor A cancellable monitor
        @return a {@link List} of {@link FSRL}s to search for libraries
        @throws CancelledException if the user cancelled the operation
        """
        ...

    @staticmethod
    def getLibraryPaths() -> List[unicode]:
        """
        Returns an array of library search paths
        @return an array of library search paths
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def reset() -> None:
        """
        Resets the library search path to the default values
        """
        ...

    @staticmethod
    def setLibraryPaths(paths: List[unicode]) -> None:
        """
        Sets the library search paths to the given array
        @param paths the new library search paths
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

