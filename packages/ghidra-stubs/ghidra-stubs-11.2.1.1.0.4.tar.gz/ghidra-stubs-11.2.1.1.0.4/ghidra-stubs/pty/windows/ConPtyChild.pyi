from typing import List
from typing import overload
import ghidra.pty
import ghidra.pty.local
import ghidra.pty.windows
import java.io
import java.lang
import java.util


class ConPtyChild(ghidra.pty.windows.ConPtyEndpoint, ghidra.pty.PtyChild):




    def __init__(self, writeHandle: ghidra.pty.windows.Handle, readHandle: ghidra.pty.windows.Handle, pseudoConsoleHandle: ghidra.pty.windows.PseudoConsoleHandle): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getInputStream(self) -> java.io.InputStream: ...

    def getOutputStream(self) -> java.io.OutputStream: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def nullSession(self, __a0: List[ghidra.pty.PtyChild.TermMode]) -> unicode: ...

    @overload
    def nullSession(self, mode: java.util.Collection) -> unicode: ...

    @overload
    def session(self, __a0: List[unicode], __a1: java.util.Map, __a2: List[ghidra.pty.PtyChild.TermMode]) -> ghidra.pty.PtySession: ...

    @overload
    def session(self, __a0: List[unicode], __a1: java.util.Map, __a2: java.io.File, __a3: List[ghidra.pty.PtyChild.TermMode]) -> ghidra.pty.PtySession: ...

    @overload
    def session(self, args: List[unicode], env: java.util.Map, workingDirectory: java.io.File, mode: java.util.Collection) -> ghidra.pty.local.LocalWindowsNativeProcessPtySession: ...

    def setWindowSize(self, cols: int, rows: int) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

