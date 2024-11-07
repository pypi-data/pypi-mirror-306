from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.lang
import java.lang


class PcodeFormatter(object):








    def equals(self, __a0: object) -> bool: ...

    @overload
    def formatOps(self, __a0: ghidra.program.model.lang.Language, __a1: List[object]) -> object: ...

    @overload
    def formatOps(self, __a0: ghidra.program.model.lang.Language, __a1: ghidra.program.model.address.AddressFactory, __a2: List[object]) -> object: ...

    def formatTemplates(self, __a0: ghidra.program.model.lang.Language, __a1: List[object]) -> object: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getPcodeOpTemplates(__a0: ghidra.program.model.address.AddressFactory, __a1: List[object]) -> List[object]: ...

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

