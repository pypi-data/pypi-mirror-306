from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.golang
import ghidra.app.util.bin.format.golang.rtti
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class GoPcHeader(object):
    """
    A low-level structure embedded in golang binaries that contains useful bootstrapping
     information.
 
     Introduced in golang 1.16
    """

    GOPCLNTAB_SECTION_NAME: unicode = u'gopclntab'
    GO_1_16_MAGIC: int = -6
    GO_1_18_MAGIC: int = -16
    GO_1_2_MAGIC: int = -5
    GO_STRUCTURE_NAME: unicode = u'runtime.pcHeader'



    def __init__(self): ...



    @staticmethod
    def createArtificialGoPcHeaderStructure(cp: ghidra.program.model.data.CategoryPath, dtm: ghidra.program.model.data.DataTypeManager) -> ghidra.program.model.data.Structure: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findPcHeaderAddress(programContext: ghidra.app.util.bin.format.golang.rtti.GoRttiMapper, range: ghidra.program.model.address.AddressRange, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.model.address.Address:
        """
        Searches (possibly slowly) for a pclntab/pcHeader structure in the specified memory range,
         which is typically necessary in stripped PE binaries.
        @param programContext {@link GoRttiMapper}
        @param range memory range to search (typically .rdata or .noptrdata sections)
        @param monitor {@link TaskMonitor} that will let the user cancel
        @return {@link Address} of the found pcHeader structure, or null if not found
        @throws IOException if error reading
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCuAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns address of the cu tab slice, used by the cuOffset field's markup annotation.
        @return address of the cu tab slice
        """
        ...

    def getFiletabAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the address of the filetab slice, used by the filetabOffset field's markup annotation
        @return address of the filetab slice
        """
        ...

    def getFuncnameAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns address of the func name slice
        @return address of func name slice
        """
        ...

    def getGoVersion(self) -> ghidra.app.util.bin.format.golang.GoVer: ...

    def getMinLC(self) -> int:
        """
        Returns the min lc, used as the GoPcValueEvaluator's pcquantum
        @return minLc
        """
        ...

    @staticmethod
    def getPcHeaderAddress(program: ghidra.program.model.listing.Program) -> ghidra.program.model.address.Address:
        """
        Returns the {@link Address} (if present) of the go pclntab section or symbol.
        @param program {@link Program}
        @return {@link Address} of go pclntab, or null if not present
        """
        ...

    def getPclnAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the address of the pcln slice, used by the pclnOffset field's markup annotation
        @return address of the pcln slice
        """
        ...

    def getPctabAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the address of the pctab slice, used by the pctabOffset field's markup annotation
        @return address of the pctab slice
        """
        ...

    def getPtrSize(self) -> int:
        """
        Returns the pointer size
        @return pointer size
        """
        ...

    def getTextStart(self) -> ghidra.program.model.address.Address:
        """
        Returns the address of where the text area starts.
        @return address of text starts
        """
        ...

    @staticmethod
    def hasPcHeader(program: ghidra.program.model.listing.Program) -> bool:
        """
        Returns true if the specified program has an easily found pclntab w/pcHeader
        @param program {@link Program}
        @return boolean true if program has a pclntab, false otherwise
        """
        ...

    def hasTextStart(self) -> bool:
        """
        Returns true if this pcln structure contains a textStart value (only present >= 1.18)
        @return 
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isPcHeader(provider: ghidra.app.util.bin.ByteProvider) -> bool:
        """
        Returns true if there is a pclntab at the current position of the specified ByteProvider.
        @param provider {@link ByteProvider}
        @return boolean true if the byte provider has the magic signature of a pclntab
        @throws IOException if error reading
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def cuAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def filetabAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def funcnameAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def goVersion(self) -> ghidra.app.util.bin.format.golang.GoVer: ...

    @property
    def minLC(self) -> int: ...

    @property
    def pclnAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def pctabAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def ptrSize(self) -> int: ...

    @property
    def textStart(self) -> ghidra.program.model.address.Address: ...