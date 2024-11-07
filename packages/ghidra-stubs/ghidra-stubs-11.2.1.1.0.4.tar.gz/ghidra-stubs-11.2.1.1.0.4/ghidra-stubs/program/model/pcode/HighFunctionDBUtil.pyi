from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.program.model.pcode.HighFunctionDBUtil
import ghidra.program.model.symbol
import java.lang
import java.util


class HighFunctionDBUtil(object):
    """
    HighFunctionDBUtil provides various methods for updating the state of a
     function contained within a program database.  It is important to note that the decompiler
     result state (e.g., HighFunction, HighParam, HighLocal, etc.) is not altered by any of
     these methods.  A new decompiler result will need to be generated to reflect any
     changes made to the database.  Care must be taken when making incremental changes
     to multiple elements (e.g., Variables)
    """

    AUTO_CAT: unicode = u'/auto_proto'




    class ReturnCommitOption(java.lang.Enum):
        COMMIT: ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption
        COMMIT_NO_VOID: ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption
        NO_COMMIT: ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self): ...



    @staticmethod
    def commitLocalNamesToDatabase(highFunction: ghidra.program.model.pcode.HighFunction, source: ghidra.program.model.symbol.SourceType) -> None:
        """
        Commit local variables from the decompiler's model of the function to the database.
         This does NOT include formal function parameters.
        @param highFunction is the decompiler's model of the function
        @param source is the desired SourceType for the commit
        """
        ...

    @staticmethod
    def commitParamsToDatabase(highFunction: ghidra.program.model.pcode.HighFunction, useDataTypes: bool, returnCommit: ghidra.program.model.pcode.HighFunctionDBUtil.ReturnCommitOption, source: ghidra.program.model.symbol.SourceType) -> None:
        """
        Commit all parameters, including optional return, associated with HighFunction to the 
         underlying database.
        @param highFunction is the associated HighFunction
        @param useDataTypes is true if the HighFunction's parameter data-types should be committed
        @param returnCommit controls optional commit of return parameter
        @param source is the signature source type to set
        @throws DuplicateNameException if commit of parameters caused conflict with other
         local variable/label.
        @throws InvalidInputException if specified storage is invalid
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getSpacebaseReferenceAddress(addrFactory: ghidra.program.model.address.AddressFactory, op: ghidra.program.model.pcode.PcodeOp) -> ghidra.program.model.address.Address:
        """
        Get the Address referred to by a spacebase reference. Address-of references are encoded in
         the p-code syntax tree as: {@code vn = PTRSUB(<spacebase>, #const)}.  This decodes the reference and
         returns the Address
        @param addrFactory is the factory used to construct the Address
        @param op is the PTRSUB op encoding the reference
        @return the recovered Address (or null if not correct form)
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readOverride(sym: ghidra.program.model.symbol.Symbol) -> ghidra.program.model.pcode.DataTypeSymbol:
        """
        Read a call prototype override which corresponds to the specified override code symbol
        @param sym special call override code symbol whose address corresponds to a call site
        @return call prototype override DataTypeSymbol or null if associated function signature
         data-type could not be found
        """
        ...

    def toString(self) -> unicode: ...

    @staticmethod
    def updateDBVariable(highSymbol: ghidra.program.model.pcode.HighSymbol, name: unicode, dataType: ghidra.program.model.data.DataType, source: ghidra.program.model.symbol.SourceType) -> None:
        """
        Rename and/or retype the specified variable in the database.  All parameters may be flushed
         to the database if typed parameter inconsistency detected.
        @param highSymbol is the symbol being updated
        @param name new variable name or null to use retain current variable name
        @param dataType newly assigned data type or null to retain current variable datatype.
         Only a fixed-length data type may be specified.  If size varies from the current size,
         an attempt will be made to grow/shrink the storage.
        @param source source type
        @throws InvalidInputException if suitable data type was not specified, or unable to
         resize storage, or invalid name specified
        @throws DuplicateNameException if name was specified and conflicts with another
         variable/label within the function's namespace
        @throws UnsupportedOperationException if unsupported variable type is specified
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @staticmethod
    def writeOverride(function: ghidra.program.model.listing.Function, callsite: ghidra.program.model.address.Address, sig: ghidra.program.model.listing.FunctionSignature) -> None:
        """
        Commit an overriding prototype for a particular call site to the database. The override
         only applies to the function(s) containing the actual call site. Calls to the same function from
         other sites are unaffected.  This is used typically either for indirect calls are for calls to
         a function with a variable number of parameters.
        @param function is the Function whose call site is being overridden
        @param callsite is the address of the calling instruction (the call site)
        @param sig is the overriding function signature
        @throws InvalidInputException if there are problems committing the override symbol
        """
        ...

    @staticmethod
    def writeUnionFacet(function: ghidra.program.model.listing.Function, dt: ghidra.program.model.data.DataType, fieldNum: int, addr: ghidra.program.model.address.Address, hash: long, source: ghidra.program.model.symbol.SourceType) -> None:
        """
        Write a union facet to the database (UnionFacetSymbol).  Parameters provide the
         pieces for building the dynamic LocalVariable.  This method clears out any preexisting
         union facet with the same dynamic hash and firstUseOffset.
        @param function is the function affected by the union facet
        @param dt is the parent data-type; a union, a pointer to a union, or a partial union
        @param fieldNum is the ordinal of the desired union field
        @param addr is the first use address of the facet
        @param hash is the dynamic hash
        @param source is the SourceType for the LocalVariable
        @throws InvalidInputException if the LocalVariable cannot be created
        @throws DuplicateNameException if the (auto-generated) name is used elsewhere
        """
        ...

