from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.bin.format.omf.omf
import ghidra.app.util.bin.format.omf.omf.OmfLibraryRecord
import ghidra.util.task
import java.lang


class OmfLibraryRecord(object):





    class MemberHeader(object):
        machineName: unicode
        name: unicode
        payloadOffset: long
        size: long
        translator: unicode



        def __init__(self): ...



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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    @staticmethod
    def checkMagicNumber(reader: ghidra.app.util.bin.BinaryReader) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getMemberHeaders(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfLibraryRecord.MemberHeader]: ...

    def getPageSize(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def parse(factory: ghidra.app.util.bin.format.omf.AbstractOmfRecordFactory, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.omf.omf.OmfLibraryRecord: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def memberHeaders(self) -> java.util.ArrayList: ...

    @property
    def pageSize(self) -> int: ...