from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pe
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.util
import ghidra.util.task
import java.io
import java.lang


class SecurityDataDirectory(ghidra.app.util.bin.format.pe.DataDirectory, ghidra.app.util.bin.ByteArrayConverter):








    def equals(self, __a0: object) -> bool: ...

    def getCertificate(self) -> List[ghidra.app.util.bin.format.pe.SecurityCertificate]:
        """
        Returns an array of security certificates.
        @return an array of security certificates
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDirectoryName(self) -> unicode: ...

    def getMarkupAddress(self, program: ghidra.program.model.listing.Program, isBinary: bool) -> ghidra.program.model.address.Address: ...

    def getPointer(self) -> int: ...

    def getSize(self) -> int:
        """
        Returns the size of this data directory.
        @return the size of this data directory
        """
        ...

    def getVirtualAddress(self) -> int:
        """
        Returns the relative virtual address of this data directory.
        @return the relative virtual address of this data directory
        """
        ...

    def hasParsedCorrectly(self) -> bool: ...

    def hashCode(self) -> int: ...

    def markup(self, program: ghidra.program.model.listing.Program, isBinary: bool, monitor: ghidra.util.task.TaskMonitor, log: ghidra.app.util.importer.MessageLog, nt: ghidra.app.util.bin.format.pe.NTHeader) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parse(self) -> bool: ...

    def setSize(self, size: int) -> None:
        """
        Sets the size of this data directory.
        @param size the new size of this data directory
        """
        ...

    def setVirtualAddress(self, addr: int) -> None:
        """
        Sets the relative virtual address of this data directory.
        @param addr the new relative virtual address
        """
        ...

    def toBytes(self, dc: ghidra.util.DataConverter) -> List[int]: ...

    def toString(self) -> unicode:
        """
        @see java.lang.Object#toString()
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def writeBytes(self, raf: java.io.RandomAccessFile, dc: ghidra.util.DataConverter, template: ghidra.app.util.bin.format.pe.PortableExecutable) -> None: ...

    @property
    def certificate(self) -> List[ghidra.app.util.bin.format.pe.SecurityCertificate]: ...

    @property
    def directoryName(self) -> unicode: ...