from typing import overload
import ghidra.app.util.bin.format.golang
import ghidra.framework.options
import ghidra.program.model.listing
import java.lang


class GoVer(object, java.lang.Comparable):
    """
    Golang version numbers
    """

    ANY: ghidra.app.util.bin.format.golang.GoVer
    GOLANG_VERSION_PROPERTY_NAME: unicode = u'Golang go version'
    INVALID: ghidra.app.util.bin.format.golang.GoVer
    V1_16: ghidra.app.util.bin.format.golang.GoVer
    V1_17: ghidra.app.util.bin.format.golang.GoVer
    V1_18: ghidra.app.util.bin.format.golang.GoVer
    V1_2: ghidra.app.util.bin.format.golang.GoVer



    def __init__(self, major: int, minor: int): ...



    @overload
    def compareTo(self, o: ghidra.app.util.bin.format.golang.GoVer) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, obj: object) -> bool: ...

    @staticmethod
    def fromProgramProperties(program: ghidra.program.model.listing.Program) -> ghidra.app.util.bin.format.golang.GoVer: ...

    def getClass(self) -> java.lang.Class: ...

    def getMajor(self) -> int:
        """
        Major value
        @return major
        """
        ...

    def getMinor(self) -> int:
        """
        Minor value
        @return minor
        """
        ...

    def hashCode(self) -> int: ...

    def inRange(self, min: ghidra.app.util.bin.format.golang.GoVer, max: ghidra.app.util.bin.format.golang.GoVer) -> bool:
        """
        Returns true if this version is between the specified min and max versions (inclusive).
        @param min minimum version to allow (inclusive)
        @param max maximum version to allow (inclusive)
        @return boolean true if this version is between the specified min and max versions
        """
        ...

    def isAtLeast(self, otherVersion: ghidra.app.util.bin.format.golang.GoVer) -> bool:
        """
        Compares this version to the specified other version and returns true if this version
         is greater than or equal to the other version.
        @param otherVersion version info to compare
        @return true if this version is gte other version
        """
        ...

    def isInvalid(self) -> bool: ...

    def isWildcard(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def parse(s: unicode) -> ghidra.app.util.bin.format.golang.GoVer:
        """
        Parses a version string ("1.2") and returns a GoVer instance, or
         INVALID if no matching version or bad data.
        @param s string to parse
        @return GoVer instance, or INVALID
        """
        ...

    @staticmethod
    def setProgramPropertiesWithOriginalVersionString(props: ghidra.framework.options.Options, s: unicode) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def invalid(self) -> bool: ...

    @property
    def major(self) -> int: ...

    @property
    def minor(self) -> int: ...

    @property
    def wildcard(self) -> bool: ...