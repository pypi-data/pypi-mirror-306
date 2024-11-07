from typing import overload
import ghidra.app.util.bin.format.elf
import ghidra.app.util.bin.format.elf.extend
import ghidra.app.util.bin.format.elf.relocation
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.reloc
import java.lang
import java.util


class ElfRelocationContext(object):
    """
    ElfRelocationContext provides a relocation handler context related
     to the processing of entries contained within a specific relocation table.
    """









    def dispose(self) -> None:
        """
        Dispose relocation context when processing of corresponding relocation table is complete.
         Instance should be disposed to allow all program changes to be flushed prior to processing
         a subsequent relocation table.
        """
        ...

    def endRelocationTableProcessing(self) -> None:
        """
        Invoked at end of relocation processing for current relocation table.
         See {@link #startRelocationTableProcessing(ElfRelocationTable)}.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def extractAddend(self) -> bool:
        """
        Determine if addend data must be extracted
        @return true if relocation does not provide addend data and it must be
         extracted from relocation target if appropriate
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getElfHeader(self) -> ghidra.app.util.bin.format.elf.ElfHeader: ...

    def getGOTValue(self) -> long:
        """
        Returns the appropriate .got section using the
         DT_PLTGOT value defined in the .dynamic section.
         If no such dynamic value defined, the symbol offset for _GLOBAL_OFFSET_TABLE_
         will be used, otherwise a NotFoundException will be thrown.
        @return the .got section address offset
        @throws NotFoundException if the dynamic DT_PLTGOT not defined and 
         _GLOBAL_OFFSET_TABLE_ symbol not defined
        """
        ...

    def getImageBaseWordAdjustmentOffset(self) -> long:
        """
        Get image base addressable word adjustment value to be applied to any pre-linked address values
         such as those contained with the dynamic table. (Applies to default address space only)
        @return image base adjustment value
        """
        ...

    def getLoadAdapter(self) -> ghidra.app.util.bin.format.elf.extend.ElfLoadAdapter: ...

    def getLoadHelper(self) -> ghidra.app.util.bin.format.elf.ElfLoadHelper: ...

    def getLog(self) -> ghidra.app.util.importer.MessageLog: ...

    def getProgram(self) -> ghidra.program.model.listing.Program: ...

    def getRelocationAddress(self, baseAddress: ghidra.program.model.address.Address, relocOffset: long) -> ghidra.program.model.address.Address:
        """
        Get relocation address
        @param baseAddress base address
        @param relocOffset relocation offset relative to baseAddress
        @return relocation address
        """
        ...

    @staticmethod
    def getRelocationContext(loadHelper: ghidra.app.util.bin.format.elf.ElfLoadHelper, symbolMap: java.util.Map) -> ghidra.app.util.bin.format.elf.relocation.ElfRelocationContext:
        """
        Get a relocation context for a specfic Elf image and relocation table
        @param loadHelper Elf load helper
        @param symbolMap Elf symbol placement map
        @return relocation context object.  A generic context will be returned if a custom one
         is not defined.
        """
        ...

    def getRelrRelocationType(self) -> int:
        """
        Get the RELR relocation type associated with the underlying
         relocation handler.
        @return RELR relocation type or 0 if not supported
        """
        ...

    def getSymbol(self, symbolIndex: int) -> ghidra.app.util.bin.format.elf.ElfSymbol:
        """
        Get the Elf symbol which corresponds to the specified index.  Each relocation table
         may correspond to a specific symbol table to which the specified symbolIndex will be
         applied.  In the absense of a corresponding symbol table index 0 will return a special 
         null symbol.
        @param symbolIndex symbol index
        @return Elf symbol which corresponds to symbol index or <B>null</B> if out of range
        """
        ...

    def getSymbolAddress(self, symbol: ghidra.app.util.bin.format.elf.ElfSymbol) -> ghidra.program.model.address.Address:
        """
        Get the program address at which the specified Elf symbol was placed.
        @param symbol Elf symbol
        @return program address
        """
        ...

    def getSymbolName(self, symbolIndex: int) -> unicode:
        """
        Get the ELF symbol name which corresponds to the specified index.
        @param symbolIndex symbol index
        @return symbol name which corresponds to symbol index or null if out of range
        """
        ...

    def getSymbolValue(self, symbol: ghidra.app.util.bin.format.elf.ElfSymbol) -> long:
        """
        Get the adjusted symbol value based upon its placement within the program.
         This value may differ from symbol.getValue() and will reflect the addressable
         unit/word offset of it program address.
        @param symbol Elf symbol
        @return adjusted Elf symbol value or 0 if symbol mapping not found
        """
        ...

    def hasRelocationHandler(self) -> bool:
        """
        @return true if a relocation handler was found
        """
        ...

    def hashCode(self) -> int: ...

    def isBigEndian(self) -> bool: ...

    def markRelocationError(self, relocationAddress: ghidra.program.model.address.Address, typeId: int, symbolIndex: int, symbolName: unicode, msg: unicode) -> None:
        """
        Generate relocation error log entry and bookmark.
        @param relocationAddress relocation address
        @param typeId relocation type ID value (will get mapped to {@link ElfRelocationType#name()}
         if possible).
        @param symbolIndex associated symbol index within symbol table (-1 to ignore)
        @param symbolName relocation symbol name or null if unknown
        @param msg error message
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def processRelocation(self, relocation: ghidra.app.util.bin.format.elf.ElfRelocation, relocationAddress: ghidra.program.model.address.Address) -> ghidra.program.model.reloc.RelocationResult:
        """
        Process a relocation from the relocation table which corresponds to this context.
         All relocation entries will be processed in the order they appear within the table.
        @param relocation relocation to be processed
        @param relocationAddress relocation address where it should be applied
        @return applied relocation result
        """
        ...

    def startRelocationTableProcessing(self, relocTable: ghidra.app.util.bin.format.elf.ElfRelocationTable) -> None:
        """
        Invoked at start of relocation processing for specified table.
         The method {@link #endRelocationTableProcessing()} will be invoked after last relocation
         is processed.
        @param relocTable relocation table
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
    def GOTValue(self) -> long: ...

    @property
    def bigEndian(self) -> bool: ...

    @property
    def elfHeader(self) -> ghidra.app.util.bin.format.elf.ElfHeader: ...

    @property
    def imageBaseWordAdjustmentOffset(self) -> long: ...

    @property
    def loadAdapter(self) -> ghidra.app.util.bin.format.elf.extend.ElfLoadAdapter: ...

    @property
    def loadHelper(self) -> ghidra.app.util.bin.format.elf.ElfLoadHelper: ...

    @property
    def log(self) -> ghidra.app.util.importer.MessageLog: ...

    @property
    def program(self) -> ghidra.program.model.listing.Program: ...

    @property
    def relrRelocationType(self) -> int: ...