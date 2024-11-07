from typing import List
from typing import overload
import ghidra.program.model.data
import java.lang


class SourceArchiveUpgradeMap(object):




    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getMappedSourceArchive(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> ghidra.program.model.data.SourceArchive: ...

    @staticmethod
    def getTypedefReplacements() -> List[unicode]: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isReplacedSourceArchive(id: long) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

