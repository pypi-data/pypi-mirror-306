from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import java.lang


class Omf51RecordFactory(ghidra.app.util.bin.format.omf.AbstractOmfRecordFactory):
    """
    A class for reading/creating OMF-51 records
    """





    def __init__(self, provider: ghidra.app.util.bin.ByteProvider):
        """
        Creates a new {@link Omf51RecordFactory}
        @param provider The {@link ByteProvider} that contains the records
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEndRecordType(self) -> int: ...

    def getReader(self) -> ghidra.app.util.bin.BinaryReader:
        """
        {@return the reader associated with this factory}
        """
        ...

    def getStartRecordTypes(self) -> List[int]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def readNextRecord(self) -> ghidra.app.util.bin.format.omf.OmfRecord: ...

    def reset(self) -> None:
        """
        Reset this factory's reader to index 0
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def endRecordType(self) -> int: ...

    @property
    def startRecordTypes(self) -> List[object]: ...