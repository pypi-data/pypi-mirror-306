from typing import List
from typing import overload
import ghidra.pcode.emu
import ghidra.pcode.emu.unix
import ghidra.program.model.lang
import java.lang


class IOStreamEmuUnixFileHandle(ghidra.pcode.emu.unix.AbstractStreamEmuUnixFileHandle):
    """
    A simulated file descriptor that proxies a host resource, typically a console/terminal
    """





    def __init__(self, __a0: ghidra.pcode.emu.PcodeMachine, __a1: ghidra.program.model.lang.CompilerSpec, __a2: java.io.InputStream, __a3: java.io.OutputStream): ...



    def close(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOffset(self) -> object: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def read(self, buf: List[int]) -> List[int]: ...

    @overload
    def read(self, __a0: object) -> object: ...

    def seek(self, offset: object) -> None: ...

    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...

    @staticmethod
    def stderr(__a0: ghidra.pcode.emu.PcodeMachine, __a1: ghidra.program.model.lang.CompilerSpec) -> ghidra.pcode.emu.unix.IOStreamEmuUnixFileHandle: ...

    @staticmethod
    def stdin(__a0: ghidra.pcode.emu.PcodeMachine, __a1: ghidra.program.model.lang.CompilerSpec) -> ghidra.pcode.emu.unix.IOStreamEmuUnixFileHandle: ...

    @staticmethod
    def stdout(__a0: ghidra.pcode.emu.PcodeMachine, __a1: ghidra.program.model.lang.CompilerSpec) -> ghidra.pcode.emu.unix.IOStreamEmuUnixFileHandle: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    def write(self, buf: List[int]) -> List[int]: ...

    @overload
    def write(self, __a0: object) -> object: ...

