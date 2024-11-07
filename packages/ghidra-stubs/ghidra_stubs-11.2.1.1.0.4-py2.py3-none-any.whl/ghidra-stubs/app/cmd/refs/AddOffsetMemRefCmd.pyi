from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class AddOffsetMemRefCmd(object, ghidra.framework.cmd.Command):
    """
    Command class to add an offset memory reference to the program.
    """





    def __init__(self, fromAddr: ghidra.program.model.address.Address, toAddr: ghidra.program.model.address.Address, toAddrIsBase: bool, refType: ghidra.program.model.symbol.RefType, source: ghidra.program.model.symbol.SourceType, opIndex: int, offset: long):
        """
        Command constructor for adding an offset memory reference. The first memory reference placed on
         an operand will be made primary by default.  All non-memory references 
         will be removed from the specified operand.  If toAddr corresponds to
         the EXTERNAL memory block (see {@link MemoryBlock#EXTERNAL_BLOCK_NAME}) the
         resulting offset reference will report to/base address as the same
         regardless of specified offset.
        @param fromAddr address of the codeunit where the reference occurs
        @param toAddr address of the location being referenced.
        @param toAddrIsBase if true toAddr is treated as base address, else treated as (base+offet).
         It is generally preferred to specify as a base address to ensure proper handling of
         EXTERNAL block case.
        @param refType reference type - how the location is being referenced.
        @param source the source of the reference
        @param opIndex the operand index in the code unit where the reference occurs
        @param offset value added to a base address to get the toAddr
        """
        ...



    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program) -> bool: ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getStatusMsg(self) -> unicode: ...

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

    @property
    def name(self) -> unicode: ...

    @property
    def statusMsg(self) -> unicode: ...