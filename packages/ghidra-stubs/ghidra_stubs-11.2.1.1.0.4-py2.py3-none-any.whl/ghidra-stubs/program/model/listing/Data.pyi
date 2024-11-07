from typing import List
from typing import overload
import ghidra.docking.settings
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.listing
import ghidra.program.model.mem
import ghidra.program.model.scalar
import ghidra.program.model.symbol
import ghidra.util
import java.io
import java.lang
import java.util


class Data(ghidra.program.model.listing.CodeUnit, ghidra.docking.settings.Settings, object):
    """
    Interface for interacting with data at an address in a program.
    """

    COMMENT_PROPERTY: unicode = u'COMMENT__GHIDRA_'
    DEFINED_DATA_PROPERTY: unicode = u'DEFINED_DATA__GHIDRA_'
    EMPTY_STRING_ARRAY: List[unicode]
    EOL_COMMENT: int = 0
    INSTRUCTION_PROPERTY: unicode = u'INSTRUCTION__GHIDRA_'
    MNEMONIC: int = -1
    NO_COMMENT: int = -1
    PLATE_COMMENT: int = 3
    POST_COMMENT: int = 2
    PRE_COMMENT: int = 1
    REPEATABLE_COMMENT: int = 4
    SPACE_PROPERTY: unicode = u'Space'







    def addMnemonicReference(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.symbol.RefType, __a2: ghidra.program.model.symbol.SourceType) -> None: ...

    def addOperandReference(self, __a0: int, __a1: ghidra.program.model.address.Address, __a2: ghidra.program.model.symbol.RefType, __a3: ghidra.program.model.symbol.SourceType) -> None: ...

    def addValueReference(self, refAddr: ghidra.program.model.address.Address, type: ghidra.program.model.symbol.RefType) -> None:
        """
        Add a memory reference to the value.
        @param refAddr address referenced.
        @param type the type of reference to be added.
        """
        ...

    def clearAllSettings(self) -> None: ...

    def clearSetting(self, __a0: unicode) -> None: ...

    def compareTo(self, __a0: ghidra.program.model.address.Address) -> int: ...

    def contains(self, __a0: ghidra.program.model.address.Address) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    @overload
    def getAddress(self) -> ghidra.program.model.address.Address: ...

    @overload
    def getAddress(self, __a0: int) -> ghidra.program.model.address.Address: ...

    def getAddressString(self, __a0: bool, __a1: bool) -> unicode: ...

    def getBaseDataType(self) -> ghidra.program.model.data.DataType:
        """
        If the dataType is a typeDef, then the typeDef's base type is returned, otherwise, the
         datatType is returned.
        @return the data type
        """
        ...

    def getBigInteger(self, __a0: int, __a1: int, __a2: bool) -> long: ...

    def getByte(self, __a0: int) -> int: ...

    @overload
    def getBytes(self) -> List[int]: ...

    @overload
    def getBytes(self, __a0: List[int], __a1: int) -> int: ...

    def getBytesInCodeUnit(self, __a0: List[int], __a1: int) -> None: ...

    def getClass(self) -> java.lang.Class: ...

    def getComment(self, __a0: int) -> unicode: ...

    def getCommentAsArray(self, __a0: int) -> List[unicode]: ...

    @overload
    def getComponent(self, index: int) -> ghidra.program.model.listing.Data:
        """
        Returns the immediate n'th component or null if none exists.
        @param index the index of the component to get.
        @return the component
        """
        ...

    @overload
    def getComponent(self, componentPath: List[int]) -> ghidra.program.model.listing.Data:
        """
        Get a data item given  the index path. Each integer in the array represents an index into
         the data item at that level.
        @param componentPath the array of indexes to use to find the requested data item.
        @return the component
        """
        ...

    def getComponentAt(self, offset: int) -> ghidra.program.model.listing.Data:
        """
        Return the first immediate child component that contains the byte at the given offset.  It
         is important to note that with certain datatypes there may be more than one component
         containing the specified offset (see {@link #getComponentsContaining(int)}).
        @param offset the amount to add to this data items address to get the address of the
         requested data item.
        @return first data component containing offset or null
        @deprecated method name has been changed to better reflect behavior.  The method
         {@link #getComponentContaining(int)} should be used instead.
        """
        ...

    def getComponentContaining(self, offset: int) -> ghidra.program.model.listing.Data:
        """
        Return the first immediate child component that contains the byte at the given offset.  It
         is important to note that with certain datatypes there may be more than one component
         containing the specified offset (see {@link #getComponentsContaining(int)}).
        @param offset the amount to add to this data items address to get the
        @return first data component containing offset or null address of the requested data item.
        """
        ...

    def getComponentIndex(self) -> int:
        """
        Get the index of this component in its parent
        @return -1 if this data item is not a component of another data item.
        """
        ...

    def getComponentLevel(self) -> int:
        """
        Get this data's component level in its hierarchy of components.
        @return the level of this data item with 0 being the level of top data items.
        """
        ...

    def getComponentPath(self) -> List[int]:
        """
        Get the component path if this is a component. The component path is an array of integers
         that represent each index in the tree of data items. Top level data items have an empty
         array for their component path.
        @return the path
        """
        ...

    def getComponentPathName(self) -> unicode:
        """
        Returns the component path name (dot notation) for this field
        @return the component path name
        """
        ...

    def getComponentsContaining(self, offset: int) -> List[ghidra.program.model.listing.Data]:
        """
        Returns a list of all the immediate child components that contain the byte at the
         given offset.
         <P>
         For a union, this will return all the components (if the offset is 0).  The presence of bit-fields
         or zero-length components may cause multiple components to be returned.
        @param offset the amount to add to this data items address to get the
         address of the requested data item.
        @return a list of all the immediate child components that contain the byte at the
         given offset or null if offset is out of bounds.
        """
        ...

    def getDataType(self) -> ghidra.program.model.data.DataType:
        """
        Get the Data type for the data.
        @return the data type
        """
        ...

    def getDefaultLabelPrefix(self, options: ghidra.program.model.data.DataTypeDisplayOptions) -> unicode:
        """
        Returns the appropriate string to use as the default label prefix or null if it has no
         preferred default label prefix;
        @param options the options
        @return the prefix
        """
        ...

    def getDefaultSettings(self) -> ghidra.docking.settings.Settings: ...

    def getDefaultValueRepresentation(self) -> unicode:
        """
        Returns a string that represents the data value without markup.
        @return the string
        """
        ...

    def getExternalReference(self, __a0: int) -> ghidra.program.model.symbol.ExternalReference: ...

    def getFieldName(self) -> unicode:
        """
        Get the field name of this data item if it is "inside" another data item, otherwise return
         null.
        @return the name of this data as known from some parent data item or
                 null if this data item is not a component of another data item.
        """
        ...

    @overload
    def getInputStream(self) -> java.io.InputStream: ...

    @overload
    def getInputStream(self, __a0: int, __a1: int) -> java.io.InputStream: ...

    def getInt(self, __a0: int) -> int: ...

    def getIntProperty(self, __a0: unicode) -> int: ...

    def getLabel(self) -> unicode: ...

    def getLength(self) -> int: ...

    @overload
    def getLong(self, __a0: int) -> long: ...

    @overload
    def getLong(self, __a0: unicode) -> long: ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMemory(self) -> ghidra.program.model.mem.Memory: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getMnemonicReferences(self) -> List[ghidra.program.model.symbol.Reference]: ...

    def getMnemonicString(self) -> unicode: ...

    def getNames(self) -> List[unicode]: ...

    def getNumComponents(self) -> int:
        """
        Return the number of components that make up this data item.
         if this is an Array, return the number of elements in the array.
        @return the number of components
        """
        ...

    def getNumOperands(self) -> int: ...

    def getObjectProperty(self, __a0: unicode) -> ghidra.util.Saveable: ...

    def getOperandReferences(self, __a0: int) -> List[ghidra.program.model.symbol.Reference]: ...

    def getParent(self) -> ghidra.program.model.listing.Data:
        """
        Get the immediate parent data item of this data item or null if this data item is not
         contained in another data item.
        @return the data
        """
        ...

    def getParentOffset(self) -> int:
        """
        Get the offset of this Data item from the start of its immediate parent.
        @return the offset
        """
        ...

    def getPathName(self) -> unicode:
        """
        Returns the full path name (dot notation) for this field.  This includes the symbol name at
         this address.
        @return the path name
        """
        ...

    def getPrimaryReference(self, __a0: int) -> ghidra.program.model.symbol.Reference: ...

    def getPrimarySymbol(self) -> ghidra.program.model.symbol.Symbol: ...

    def getPrimitiveAt(self, offset: int) -> ghidra.program.model.listing.Data:
        """
        Returns the primitive component containing this offset (i.e., one that does not
         have sub-components).  This is useful for data items which are made up of multiple
         layers of other data items. This method immediately goes to the lowest level data item.
         If the minimum offset of a component is specified, the only first component containing
         the offset will be considered (e.g., 0-element array).
        @param offset the offset
        @return primitive component containing this offset
        """
        ...

    def getProgram(self) -> ghidra.program.model.listing.Program: ...

    def getReferenceIteratorTo(self) -> ghidra.program.model.symbol.ReferenceIterator: ...

    def getReferencesFrom(self) -> List[ghidra.program.model.symbol.Reference]: ...

    def getRoot(self) -> ghidra.program.model.listing.Data:
        """
        Get the highest level Data item in a hierarchy of structures containing this component.
        @return the data
        """
        ...

    def getRootOffset(self) -> int:
        """
        Get the offset of this Data item from the start of the root data item of some hierarchy of
         structures.
        @return the offset
        """
        ...

    def getScalar(self, __a0: int) -> ghidra.program.model.scalar.Scalar: ...

    def getShort(self, __a0: int) -> int: ...

    def getString(self, __a0: unicode) -> unicode: ...

    def getStringProperty(self, __a0: unicode) -> unicode: ...

    def getSuggestedValues(self, __a0: ghidra.docking.settings.StringSettingsDefinition) -> List[unicode]: ...

    def getSymbols(self) -> List[ghidra.program.model.symbol.Symbol]: ...

    def getUnsignedByte(self, __a0: int) -> int: ...

    def getUnsignedInt(self, __a0: int) -> long: ...

    def getUnsignedShort(self, __a0: int) -> int: ...

    @overload
    def getValue(self) -> object:
        """
        Returns the value of the data item.  The value may be an address, a scalar,
         register or null if no value.
        @return the value
        """
        ...

    @overload
    def getValue(self, __a0: unicode) -> object: ...

    def getValueClass(self) -> java.lang.Class:
        """
        Get the class used to express the value of this data.

         <p>NOTE: This determination is made based upon data type and settings only and does not
         examine memory bytes which are used to construct the data value object.
        @return value class or null if a consistent class is not utilized.
        """
        ...

    def getValueReferences(self) -> List[ghidra.program.model.symbol.Reference]:
        """
        Get the references for the value.
        @return the references
        """
        ...

    def getVarLengthInt(self, __a0: int, __a1: int) -> int: ...

    def getVarLengthUnsignedInt(self, __a0: int, __a1: int) -> long: ...

    def getVoidProperty(self, __a0: unicode) -> bool: ...

    def hasProperty(self, __a0: unicode) -> bool: ...

    def hasStringValue(self) -> bool:
        """
        Returns true if this data corresponds to string data.  This is determined
         by the corresponding data type producing a String value.
        @return true if this data returns a String value and can be treated as string data.
        """
        ...

    def hashCode(self) -> int: ...

    def isArray(self) -> bool:
        """
        Returns true if this data item is an Array of DataTypes
        @return true if an array
        """
        ...

    def isBigEndian(self) -> bool: ...

    def isChangeAllowed(self, __a0: ghidra.docking.settings.SettingsDefinition) -> bool: ...

    def isConstant(self) -> bool:
        """
        Determine if this data has explicitly been marked as constant.
         NOTE: This is based upon explicit {@link Data} and {@link DataType} mutability settings
         and does not reflect independent memory block or processor specification settings.
        @return true if data is constant, else false.
        """
        ...

    def isDefined(self) -> bool:
        """
        Returns true if the data type is defined.  Any address that has not been defined to be code
         or data is treated as undefined data.
        @return true if is defined
        """
        ...

    def isDynamic(self) -> bool:
        """
        Returns true if this data item is a dynamic DataType.
        @return true if is dynamic
        """
        ...

    def isEmpty(self) -> bool: ...

    def isInitializedMemory(self) -> bool: ...

    def isPointer(self) -> bool:
        """
        Returns true if this is a pointer, implies getValue() will will return an Object that is an
         Address.
        @return true if a pointer
        """
        ...

    def isStructure(self) -> bool:
        """
        Returns true if this data item is a Structure.
        @return true if a structure
        """
        ...

    def isUnion(self) -> bool:
        """
        Returns true if this data item is a Union.
        @return true if a union
        """
        ...

    def isVolatile(self) -> bool:
        """
        Determine if this data has explicitly been marked as volatile.
         NOTE: This is based upon explicit {@link Data} and {@link DataType} mutability settings
         and does not reflect independent memory block or processor specification settings.
        @return true if data is volatile, else false.
        """
        ...

    def isWritable(self) -> bool:
        """
        Determine if this data has explicitly been marked as writable.
         NOTE: This is based upon explicit {@link Data} and {@link DataType} mutability settings
         and does not reflect independent memory block or processor specification settings.
        @return true if data is writable, else false.
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def propertyNames(self) -> java.util.Iterator: ...

    def removeExternalReference(self, __a0: int) -> None: ...

    def removeMnemonicReference(self, __a0: ghidra.program.model.address.Address) -> None: ...

    def removeOperandReference(self, __a0: int, __a1: ghidra.program.model.address.Address) -> None: ...

    def removeProperty(self, __a0: unicode) -> None: ...

    def removeValueReference(self, refAddr: ghidra.program.model.address.Address) -> None:
        """
        Remove a reference to the value.
        @param refAddr address of reference to be removed.
        """
        ...

    def setComment(self, __a0: int, __a1: unicode) -> None: ...

    def setCommentAsArray(self, __a0: int, __a1: List[unicode]) -> None: ...

    def setLong(self, __a0: unicode, __a1: long) -> None: ...

    def setPrimaryMemoryReference(self, __a0: ghidra.program.model.symbol.Reference) -> None: ...

    @overload
    def setProperty(self, __a0: unicode) -> None: ...

    @overload
    def setProperty(self, __a0: unicode, __a1: int) -> None: ...

    @overload
    def setProperty(self, __a0: unicode, __a1: unicode) -> None: ...

    @overload
    def setProperty(self, __a0: unicode, __a1: ghidra.util.Saveable) -> None: ...

    def setRegisterReference(self, __a0: int, __a1: ghidra.program.model.lang.Register, __a2: ghidra.program.model.symbol.SourceType, __a3: ghidra.program.model.symbol.RefType) -> None: ...

    def setStackReference(self, __a0: int, __a1: int, __a2: ghidra.program.model.symbol.SourceType, __a3: ghidra.program.model.symbol.RefType) -> None: ...

    def setString(self, __a0: unicode, __a1: unicode) -> None: ...

    def setValue(self, __a0: unicode, __a1: object) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def address(self) -> ghidra.program.model.address.Address: ...

    @property
    def array(self) -> bool: ...

    @property
    def baseDataType(self) -> ghidra.program.model.data.DataType: ...

    @property
    def bigEndian(self) -> bool: ...

    @property
    def bytes(self) -> List[int]: ...

    @property
    def componentIndex(self) -> int: ...

    @property
    def componentLevel(self) -> int: ...

    @property
    def componentPath(self) -> List[int]: ...

    @property
    def componentPathName(self) -> unicode: ...

    @property
    def constant(self) -> bool: ...

    @property
    def dataType(self) -> ghidra.program.model.data.DataType: ...

    @property
    def defaultSettings(self) -> ghidra.docking.settings.Settings: ...

    @property
    def defaultValueRepresentation(self) -> unicode: ...

    @property
    def defined(self) -> bool: ...

    @property
    def dynamic(self) -> bool: ...

    @property
    def empty(self) -> bool: ...

    @property
    def fieldName(self) -> unicode: ...

    @property
    def initializedMemory(self) -> bool: ...

    @property
    def inputStream(self) -> java.io.InputStream: ...

    @property
    def label(self) -> unicode: ...

    @property
    def length(self) -> int: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def memory(self) -> ghidra.program.model.mem.Memory: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def mnemonicReferences(self) -> List[ghidra.program.model.symbol.Reference]: ...

    @property
    def mnemonicString(self) -> unicode: ...

    @property
    def names(self) -> List[unicode]: ...

    @property
    def numComponents(self) -> int: ...

    @property
    def numOperands(self) -> int: ...

    @property
    def parent(self) -> ghidra.program.model.listing.Data: ...

    @property
    def parentOffset(self) -> int: ...

    @property
    def pathName(self) -> unicode: ...

    @property
    def pointer(self) -> bool: ...

    @property
    def primaryMemoryReference(self) -> None: ...  # No getter available.

    @primaryMemoryReference.setter
    def primaryMemoryReference(self, value: ghidra.program.model.symbol.Reference) -> None: ...

    @property
    def primarySymbol(self) -> ghidra.program.model.symbol.Symbol: ...

    @property
    def program(self) -> ghidra.program.model.listing.Program: ...

    @property
    def property(self) -> None: ...  # No getter available.

    @property.setter
    def property(self, value: unicode) -> None: ...

    @property
    def referenceIteratorTo(self) -> ghidra.program.model.symbol.ReferenceIterator: ...

    @property
    def referencesFrom(self) -> List[ghidra.program.model.symbol.Reference]: ...

    @property
    def root(self) -> ghidra.program.model.listing.Data: ...

    @property
    def rootOffset(self) -> int: ...

    @property
    def structure(self) -> bool: ...

    @property
    def symbols(self) -> List[ghidra.program.model.symbol.Symbol]: ...

    @property
    def union(self) -> bool: ...

    @property
    def value(self) -> object: ...

    @property
    def valueClass(self) -> java.lang.Class: ...

    @property
    def valueReferences(self) -> List[ghidra.program.model.symbol.Reference]: ...

    @property
    def volatile(self) -> bool: ...

    @property
    def writable(self) -> bool: ...