from typing import overload
import ghidra.pty
import ghidra.pty.ssh
import java.io
import java.lang


class SshPtyParent(ghidra.pty.ssh.SshPtyEndpoint, ghidra.pty.PtyParent):




    def __init__(self, channel: com.jcraft.jsch.ChannelExec, outputStream: java.io.OutputStream, inputStream: java.io.InputStream): ...



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

