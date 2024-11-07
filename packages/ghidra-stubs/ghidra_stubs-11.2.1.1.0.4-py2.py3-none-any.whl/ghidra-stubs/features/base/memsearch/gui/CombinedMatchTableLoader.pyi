from typing import overload
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.searcher
import ghidra.util.datastruct
import ghidra.util.task
import java.lang


class CombinedMatchTableLoader(object, ghidra.features.base.memsearch.gui.MemoryMatchTableLoader):
    """
    Table loader that performs a search and then combines the new results with existing results.
    """





    def __init__(self, __a0: ghidra.features.base.memsearch.searcher.MemorySearcher, __a1: List[object], __a2: ghidra.features.base.memsearch.combiner.Combiner): ...



    def didTerminateEarly(self) -> bool: ...

    def dispose(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstMatch(self) -> ghidra.features.base.memsearch.searcher.MemoryMatch: ...

    def hasResults(self) -> bool: ...

    def hashCode(self) -> int: ...

    def loadResults(self, accumulator: ghidra.util.datastruct.Accumulator, monitor: ghidra.util.task.TaskMonitor) -> None: ...

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