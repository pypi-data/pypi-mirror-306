from typing import overload
import ghidra.app.decompiler
import ghidra.program.model.pcode
import java.lang


class ClangMarkup(object):




    def __init__(self): ...



    @staticmethod
    def buildClangTree(decoder: ghidra.program.model.pcode.Decoder, hfunc: ghidra.program.model.pcode.HighFunction) -> ghidra.app.decompiler.ClangTokenGroup: ...

    def equals(self, __a0: object) -> bool: ...

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

