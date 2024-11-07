from typing import overload
import ghidra.docking.settings
import ghidra.program.model.data
import java.io
import java.lang


class DataTypeComponentImpl(object, ghidra.program.model.data.InternalDataTypeComponent, java.io.Serializable):
    """
    Basic implementation of a DataTypeComponent
    """

    DEFAULT_FIELD_NAME_PREFIX: unicode = u'field'



    @overload
    def __init__(self, dataType: ghidra.program.model.data.DataType, parent: ghidra.program.model.data.CompositeDataTypeImpl, length: int, ordinal: int, offset: int):
        """
        Create a new DataTypeComponent
        @param dataType the dataType for this component
        @param parent the dataType that this component belongs to
        @param length the length of the dataType in this component.
        @param ordinal the index of this component within its parent.
        @param offset the byte offset within the parent
        """
        ...

    @overload
    def __init__(self, dataType: ghidra.program.model.data.DataType, parent: ghidra.program.model.data.CompositeDataTypeImpl, length: int, ordinal: int, offset: int, fieldName: unicode, comment: unicode):
        """
        Create a new DataTypeComponent
        @param dataType the dataType for this component
        @param parent the dataType that this component belongs to
        @param length the length of the dataType in this component.
        @param ordinal the index within its parent.
        @param offset the byte offset within the parent
        @param fieldName the name associated with this component
        @param comment the comment associated with this component
        """
        ...



    @staticmethod
    def checkDefaultFieldName(fieldName: unicode) -> None: ...

    def equals(self, obj: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getComment(self) -> unicode: ...

    def getDataType(self) -> ghidra.program.model.data.DataType: ...

    def getDefaultFieldName(self) -> unicode: ...

    def getDefaultSettings(self) -> ghidra.docking.settings.Settings: ...

    def getEndOffset(self) -> int: ...

    def getFieldName(self) -> unicode: ...

    def getLength(self) -> int: ...

    def getOffset(self) -> int: ...

    def getOrdinal(self) -> int: ...

    def getParent(self) -> ghidra.program.model.data.DataType: ...

    @staticmethod
    def getPreferredComponentLength(dataType: ghidra.program.model.data.DataType, length: int) -> int:
        """
        Get the preferred length for a new component. The length returned will be no
         larger than the specified length.
        @param dataType new component datatype
        @param length constrained length or -1 to force use of dataType size.
                         Dynamic types such as string must have a positive length
                         specified.
        @return preferred component length
        @throws IllegalArgumentException if length not specified for a {@link Dynamic} dataType.
        """
        ...

    def hashCode(self) -> int: ...

    def isBitFieldComponent(self) -> bool: ...

    def isEquivalent(self, dtc: ghidra.program.model.data.DataTypeComponent) -> bool: ...

    def isZeroBitFieldComponent(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setComment(self, comment: unicode) -> None: ...

    def setDataType(self, dt: ghidra.program.model.data.DataType) -> None: ...

    def setFieldName(self, name: unicode) -> None: ...

    def toString(self) -> unicode: ...

    def update(self, ordinal: int, offset: int, length: int) -> None: ...

    @staticmethod
    def usesZeroLengthComponent(__a0: ghidra.program.model.data.DataType) -> bool: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def bitFieldComponent(self) -> bool: ...

    @property
    def comment(self) -> unicode: ...

    @comment.setter
    def comment(self, value: unicode) -> None: ...

    @property
    def dataType(self) -> ghidra.program.model.data.DataType: ...

    @dataType.setter
    def dataType(self, value: ghidra.program.model.data.DataType) -> None: ...

    @property
    def defaultFieldName(self) -> unicode: ...

    @property
    def defaultSettings(self) -> ghidra.docking.settings.Settings: ...

    @property
    def endOffset(self) -> int: ...

    @property
    def fieldName(self) -> unicode: ...

    @fieldName.setter
    def fieldName(self, value: unicode) -> None: ...

    @property
    def length(self) -> int: ...

    @property
    def offset(self) -> int: ...

    @property
    def ordinal(self) -> int: ...

    @property
    def parent(self) -> ghidra.program.model.data.DataType: ...

    @property
    def zeroBitFieldComponent(self) -> bool: ...