from typing import overload
import ghidra.pty
import ghidra.pty.windows
import java.io
import java.lang


class ConPtyParent(ghidra.pty.windows.ConPtyEndpoint, ghidra.pty.PtyParent):




    def __init__(self, writeHandle: ghidra.pty.windows.Handle, readHandle: ghidra.pty.windows.Handle, pseudoConsoleHandle: ghidra.pty.windows.PseudoConsoleHandle): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getInputStream(self) -> java.io.InputStream: ...

    def getOutputStream(self) -> java.io.OutputStream: ...

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

