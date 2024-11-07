from typing import overload
import ghidra.pcode.struct
import java.lang


class StringTree(object):




    def __init__(self): ...



    @overload
    def append(self, tree: ghidra.pcode.struct.StringTree) -> None: ...

    @overload
    def append(self, seq: java.lang.CharSequence) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def single(seq: java.lang.CharSequence) -> ghidra.pcode.struct.StringTree: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

