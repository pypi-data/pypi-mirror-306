from typing import overload
import ghidra.features.base.memsearch.searcher
import ghidra.util.datastruct
import ghidra.util.task
import java.lang


class MemoryMatchTableLoader(object):
    """
    Interface for loading the memory search results table. Various implementations handle the
     different cases such as a search all, or a search next, or combining results with a previous
     search, etc.
    """









    def didTerminateEarly(self) -> bool:
        """
        Returns true if the search/loading did not fully complete. (Search limit reached, cancelled
         by user, etc.)
        @return true if the search/loading did not fully complete
        """
        ...

    def dispose(self) -> None:
        """
        Cleans up resources
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstMatch(self) -> ghidra.features.base.memsearch.searcher.MemoryMatch:
        """
        Returns the first match found. Typically used to navigate the associated navigatable.
        @return the first match found
        """
        ...

    def hasResults(self) -> bool:
        """
        Returns true if at least one match was found.
        @return true if at least one match was found
        """
        ...

    def hashCode(self) -> int: ...

    def loadResults(self, accumulator: ghidra.util.datastruct.Accumulator, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Called by the table model to initiate searching and loading using the threaded table models
         threading infrastructure.
        @param accumulator the accumulator to store results that will appear in the results table
        @param monitor the task monitor
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
    def firstMatch(self) -> ghidra.features.base.memsearch.searcher.MemoryMatch: ...