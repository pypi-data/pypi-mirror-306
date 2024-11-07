from typing import List
from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.app.util.bin.format.swift.types
import ghidra.program.model.data
import java.lang


class FieldDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift FieldDescriptor structure
    """

    SIZE: int = 16



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link FieldDescriptor}
        @param reader A {@link BinaryReader} positioned at the start of the structure
        @throws IOException if there was an IO-related problem creating the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getBase(self) -> long:
        """
        Gets the base "address" of this {@link SwiftTypeMetadataStructure}
        @return The base "address" of this {@link SwiftTypeMetadataStructure}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getFieldRecordSize(self) -> int:
        """
        Gets the field record size
        @return The field record size
        """
        ...

    def getFieldRecords(self) -> List[ghidra.app.util.bin.format.swift.types.FieldRecord]:
        """
        Gets the {@link List} of {@link FieldRecord}s
        @return The {@link List} of {@link FieldRecord}s
        """
        ...

    def getKind(self) -> int:
        """
        Gets the kind
        @return The kind
        """
        ...

    def getMangledTypeName(self) -> unicode:
        """
        Gets the mangled type name
        @return The mangled type name
        """
        ...

    def getNumFields(self) -> int:
        """
        Gets the number of fields
        @return The number of fields
        """
        ...

    def getStructureName(self) -> unicode: ...

    def getSuperclass(self) -> int:
        """
        Gets the superclass
        @return The superclass
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def description(self) -> unicode: ...

    @property
    def fieldRecordSize(self) -> int: ...

    @property
    def fieldRecords(self) -> List[object]: ...

    @property
    def kind(self) -> int: ...

    @property
    def mangledTypeName(self) -> unicode: ...

    @property
    def numFields(self) -> int: ...

    @property
    def structureName(self) -> unicode: ...

    @property
    def superclass(self) -> int: ...