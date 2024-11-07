from typing import overload
import ghidra.program.model.address
import ghidra.program.model.symbol
import java.lang


class OffsetReference(ghidra.program.model.symbol.Reference, object):
    """
    OffsetReference is a memory reference whose "to" address is
     computed from a base address plus an offset.
 
     NOTE: References into the reserved EXTERNAL block must report #getToAddress()
     the same as #getBaseAddress() regardless of offset value due to symbol
     spacing limitations within the EXTERNAL block.  See MemoryBlock#EXTERNAL_BLOCK_NAME.
    """

    MNEMONIC: int = -1
    OTHER: int = -2







    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def getBaseAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the base address.
        @return the address
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getFromAddress(self) -> ghidra.program.model.address.Address: ...

    def getOffset(self) -> long:
        """
        Returns the offset.
        @return the offset
        """
        ...

    def getOperandIndex(self) -> int: ...

    def getReferenceType(self) -> ghidra.program.model.symbol.RefType: ...

    def getSource(self) -> ghidra.program.model.symbol.SourceType: ...

    def getSymbolID(self) -> long: ...

    def getToAddress(self) -> ghidra.program.model.address.Address:
        """
        Return the base address plus the offset.  The exception to this is the
         EXTERNAL block case where this method returns the base address regardless
         of the offset value.
        @return reference "to" address
        """
        ...

    def hashCode(self) -> int: ...

    def isEntryPointReference(self) -> bool: ...

    def isExternalReference(self) -> bool: ...

    def isMemoryReference(self) -> bool: ...

    def isMnemonicReference(self) -> bool: ...

    def isOffsetReference(self) -> bool: ...

    def isOperandReference(self) -> bool: ...

    def isPrimary(self) -> bool: ...

    def isRegisterReference(self) -> bool: ...

    def isShiftedReference(self) -> bool: ...

    def isStackReference(self) -> bool: ...

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
    def baseAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def entryPointReference(self) -> bool: ...

    @property
    def externalReference(self) -> bool: ...

    @property
    def fromAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def memoryReference(self) -> bool: ...

    @property
    def mnemonicReference(self) -> bool: ...

    @property
    def offset(self) -> long: ...

    @property
    def offsetReference(self) -> bool: ...

    @property
    def operandIndex(self) -> int: ...

    @property
    def operandReference(self) -> bool: ...

    @property
    def primary(self) -> bool: ...

    @property
    def referenceType(self) -> ghidra.program.model.symbol.RefType: ...

    @property
    def registerReference(self) -> bool: ...

    @property
    def shiftedReference(self) -> bool: ...

    @property
    def source(self) -> ghidra.program.model.symbol.SourceType: ...

    @property
    def stackReference(self) -> bool: ...

    @property
    def symbolID(self) -> long: ...

    @property
    def toAddress(self) -> ghidra.program.model.address.Address: ...