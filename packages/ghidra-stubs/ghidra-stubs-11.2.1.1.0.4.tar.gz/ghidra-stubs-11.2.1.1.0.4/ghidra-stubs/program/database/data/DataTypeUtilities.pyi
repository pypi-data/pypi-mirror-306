from typing import overload
import ghidra.docking.settings
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.program.model.symbol
import java.lang
import java.util


class DataTypeUtilities(object):




    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def equalsIgnoreConflict(name1: unicode, name2: unicode) -> bool:
        """
        Compares two data type name strings to determine if they are equivalent names, ignoring
         conflict patterns present.
        @param name1 the first name
        @param name2 the second name
        @return true if the names are equivalent when conflict suffixes are ignored.
        """
        ...

    @staticmethod
    def findDataType(dataTypeManager: ghidra.program.model.data.DataTypeManager, namespace: ghidra.program.model.symbol.Namespace, dtName: unicode, classConstraint: java.lang.Class) -> object:
        """
        Attempt to find the data type whose dtName and specified namespace match a stored data type
         within the specified dataTypeManager. The first match which satisfies the category path 
         requirement will be returned.  If a non-root namespace is specified the datatype's trailing 
         category path must match the specified namespace path.
        @param dataTypeManager data type manager
        @param namespace namespace associated with dtName (null indicates no namespace constraint)
        @param dtName name of data type
        @param classConstraint optional data type interface constraint (e.g., Structure), or null
        @return best matching data type
        """
        ...

    @staticmethod
    def findExistingClassStruct(dataTypeManager: ghidra.program.model.data.DataTypeManager, classNamespace: ghidra.program.model.listing.GhidraClass) -> ghidra.program.model.data.Structure:
        """
        Find the structure data type which corresponds to the specified class namespace
         within the specified data type manager.
         The structure must utilize a namespace-based category path, however,
         the match criteria can be fuzzy and relies primarily on the full class namespace.  
         A properly named class structure must reside within a category whose trailing 
         path either matches the class namespace or the class-parent's namespace.  
         Preference is given to it residing within the class-parent's namespace.
        @param dataTypeManager data type manager which should be searched.
        @param classNamespace class namespace
        @return existing structure which resides within matching category.
        """
        ...

    @staticmethod
    def findNamespaceQualifiedDataType(dataTypeManager: ghidra.program.model.data.DataTypeManager, dtNameWithNamespace: unicode, classConstraint: java.lang.Class) -> object:
        """
        Attempt to find the data type whose dtNameWithNamespace match a stored data type within the
         specified dataTypeManager. The namespace will be used in checking data type parent categories.  
         NOTE: name parsing assumes :: namespace delimiter which can be thrown off if name includes 
         template information which could contain namespaces (see {@link SymbolPathParser#parse(String)}).
        @param dataTypeManager data type manager
        @param dtNameWithNamespace name of data type qualified with namespace (e.g.,
                    ns1::ns2::dtname)
        @param classConstraint optional data type interface constraint (e.g., Structure), or null
        @return best matching data type
        """
        ...

    @staticmethod
    def getArrayBaseDataType(arrayDt: ghidra.program.model.data.Array) -> ghidra.program.model.data.DataType: ...

    @staticmethod
    def getBaseDataType(dt: ghidra.program.model.data.DataType) -> ghidra.program.model.data.DataType:
        """
        Get the base data type for the specified data type stripping away pointers and arrays only. A
         null will be returned for a default pointer.
        @param dt the data type whose base data type is to be determined.
        @return the base data type (may be null for default pointer).
        """
        ...

    @staticmethod
    def getCPrimitiveDataType(dataTypeName: unicode) -> ghidra.program.model.data.DataType:
        """
        Return the appropriate datatype for a given C primitive datatype name.
        @param dataTypeName the datatype name (e.g. "unsigned int", "long long")
        @return the appropriate datatype for a given C primitive datatype name.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    @staticmethod
    def getConflictValue(dataTypeName: unicode) -> int:
        """
        Get the conflict value associated with a conflict datatype name.
        @param dataTypeName datatype name to be checked
        @return conflict value:
         <ol>
         <li>-1: when name is not have a conflict name,</li>
         <li>0: when conflict name does not have a number (i.e., {@code .conflict}), or</li>
         <li>a positive value which corresponds to the conflict number in the name 
             (e.g., returns 2 for {@code .conflict2}).</li>
         </ol>
        """
        ...

    @overload
    @staticmethod
    def getConflictValue(dataType: ghidra.program.model.data.DataType) -> int:
        """
        Get the conflict value string associated with a conflict datatype name.
        @param dataType datatype to be checked
        @return conflict value:
         <ol>
         <li>-1: when type does not have a conflict name,</li>
         <li>0: when conflict name does not have a number (i.e., {@code .conflict}), or</li>
         <li>a positive value which corresponds to the conflict number in the name 
             (e.g., returns 2 for {@code .conflict2}).</li>
         </ol>
        """
        ...

    @staticmethod
    def getContainedDataTypes(rootDataType: ghidra.program.model.data.DataType) -> java.util.Collection: ...

    @staticmethod
    def getDataTypeCategoryPath(baseCategory: ghidra.program.model.data.CategoryPath, namespace: ghidra.program.model.symbol.Namespace) -> ghidra.program.model.data.CategoryPath:
        """
        Create a data type category path derived from the specified namespace and rooted from the
         specified baseCategory
        @param baseCategory category path from which to root the namespace-base path
        @param namespace the namespace
        @return namespace derived category path
        """
        ...

    @staticmethod
    def getDisplayName(arrayDt: ghidra.program.model.data.Array, showBaseSizeForDynamics: bool) -> unicode: ...

    @staticmethod
    def getMnemonic(arrayDt: ghidra.program.model.data.Array, showBaseSizeForDynamics: bool, settings: ghidra.docking.settings.Settings) -> unicode: ...

    @staticmethod
    def getName(arrayDt: ghidra.program.model.data.Array, showBaseSizeForDynamics: bool) -> unicode: ...

    @overload
    @staticmethod
    def getNameWithoutConflict(dataTypeName: unicode) -> unicode:
        """
        Get the name of a data type with all conflict naming patterns removed.
        @param dataTypeName data type name with optional category path included
        @return name with optional category path included
        """
        ...

    @overload
    @staticmethod
    def getNameWithoutConflict(dt: ghidra.program.model.data.DataType) -> unicode:
        """
        Get a datatype's name without conflict suffix.
        @param dt datatype (pointer and array permitted)
        @return datatype's name without conflict suffix
        """
        ...

    @overload
    @staticmethod
    def getNameWithoutConflict(dataType: ghidra.program.model.data.DataType, includeCategoryPath: bool) -> unicode:
        """
        Get the name of a data type with all conflict naming patterns removed.
        @param dataType data type
        @param includeCategoryPath if true, the category path will be included with the
         returned name (e.g., /mypath/mydt) and any occurance of a forward slash within individual 
         path components, including the data type name, will be escaped (e.g., {@code "\/"}).
        @return name with optional category path included
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isConflictDataType(dt: ghidra.program.model.data.DataType) -> bool:
        """
        Determine if the specified data type has a conflict name.
        @param dt datatype (pointer and array permitted)
        @return true if data type has a conflict name.
        """
        ...

    @staticmethod
    def isConflictDataTypeName(dataTypeName: unicode) -> bool:
        """
        Determine if the specified data type name is a conflict name.
        @param dataTypeName datatype name
        @return true if data type name is a conflict name.
        """
        ...

    @staticmethod
    def isSameDataType(dataType1: ghidra.program.model.data.DataType, dataType2: ghidra.program.model.data.DataType) -> bool:
        """
        Returns true if the two dataTypes have the same sourceArchive and the same UniversalID
        @param dataType1 first data type
        @param dataType2 second data type
        @return true if types correspond to the same type from a source archive
        """
        ...

    @staticmethod
    def isSameKindDataType(dataType1: ghidra.program.model.data.DataType, dataType2: ghidra.program.model.data.DataType) -> bool:
        """
        Determine if two dataTypes are the same kind of datatype without considering naming or
         component makeup.  The use of Typedefs is ignored and stripped away for comparison.
         This method also ignores details about most built-in types, pointers and arrays 
         (e.g., number of elements or size).  Implementations of the following abstract classes
         will be treated as the same kind as another datatype which extends the same abstract
         class:
         <ul>
         <li>{@link AbstractIntegerDataType}</li> 
         <li>{@link AbstractFloatDataType}</li>
         <li>{@link AbstractStringDataType}</li>
         </ul>
          Other uses of {@link BuiltInDataType} must match the specific implementation class.
        @param dataType1 first data type
        @param dataType2 second data type
        @return true if the two dataTypes are the same basic kind else false
        """
        ...

    @staticmethod
    def isSameOrEquivalentDataType(dataType1: ghidra.program.model.data.DataType, dataType2: ghidra.program.model.data.DataType) -> bool:
        """
        Returns true if two dataTypes have the same sourceArchive and the same UniversalID OR are
         equivalent
        @param dataType1 first data type (if invoked by DB object or manager, this argument must
                    correspond to the DataTypeDB).
        @param dataType2 second data type
        @return true if types correspond to the same type from a source archive or they are
                 equivelent, otherwise false
        """
        ...

    @staticmethod
    def isSecondPartOfFirst(firstDataType: ghidra.program.model.data.DataType, secondDataType: ghidra.program.model.data.DataType) -> bool:
        """
        Check to see if the second data type is the same as the first data type or is part of it.
         <br>
         Note: pointers to the second data type are references and therefore are not considered to be
         part of the first and won't cause true to be returned. If you pass a pointer to this method
         for the first or second parameter, it will return false.
        @param firstDataType the data type whose components or base type should be checked to see if
                    the second data type is part of it.
        @param secondDataType the data type to be checked for in the first data type.
        @return true if the second data type is the first data type or is part of it.
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

