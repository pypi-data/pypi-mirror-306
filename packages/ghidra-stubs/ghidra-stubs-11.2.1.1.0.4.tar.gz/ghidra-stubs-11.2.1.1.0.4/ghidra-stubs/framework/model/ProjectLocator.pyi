from typing import overload
import java.io
import java.lang
import java.net


class ProjectLocator(object):
    """
    Lightweight descriptor of a local Project storage location.
    """

    DISALLOWED_CHARS: java.util.Set
    PROJECT_DIR_SUFFIX: unicode = u'.rep'
    PROJECT_FILE_SUFFIX: unicode = u'.gpr'



    def __init__(self, path: unicode, name: unicode):
        """
        Construct a project locator object.
        @param path absolute path to parent directory (may or may not exist).  The user's temp directory
         will be used if this value is null or blank.  The use of "\" characters will always be replaced 
         with "/".
         WARNING: Use of a relative paths should be avoided (e.g., on a windows platform
         an absolute path should start with a drive letter specification such as C:\path).
         A path such as "/path" on windows will utilize the current default drive and will
         not throw an exception.  If a drive letter is specified it must specify an absolute
         path (e.g., C:\, C:\path).
        @param name name of the project (may only contain alphanumeric characters or
        @throws IllegalArgumentException if an absolute path is not specified or invalid project name
        """
        ...



    def equals(self, obj: object) -> bool: ...

    def exists(self) -> bool:
        """
        {@return true if project storage exists}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getLocation(self) -> unicode:
        """
        Get the location of the project which will contain marker file
         ({@link #getMarkerFile()}) and project directory ({@link #getProjectDir()}). 
         <p>
         Note: directory may or may not exist.
        @return project location directory
        """
        ...

    def getMarkerFile(self) -> java.io.File:
        """
        {@return the file that indicates a Ghidra project.}
        """
        ...

    def getName(self) -> unicode:
        """
        {@return the name of the project identified by this project info.}
        """
        ...

    def getProjectDir(self) -> java.io.File:
        """
        {@return the project directory}
        """
        ...

    @staticmethod
    def getProjectDirExtension() -> unicode:
        """
        {@return the project directory file extension.}
        """
        ...

    @staticmethod
    def getProjectExtension() -> unicode:
        """
        {@return the file extension suitable for creating file filters for the file chooser}
        """
        ...

    def getProjectLockFile(self) -> java.io.File:
        """
        {@return project lock file to prevent multiple accesses to the same project at once.}
        """
        ...

    def getURL(self) -> java.net.URL:
        """
        {@return the URL associated with this local project.  If using a temporary transient
         project location this URL should not be used.}
        """
        ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isProjectDir(file: java.io.File) -> bool:
        """
        {@return whether the given file is a project directory.}
        @param file file to check
        """
        ...

    def isTransient(self) -> bool:
        """
        {@return true if this project URL corresponds to a transient project
         (e.g., corresponds to remote Ghidra URL)}
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
    def URL(self) -> java.net.URL: ...

    @property
    def location(self) -> unicode: ...

    @property
    def markerFile(self) -> java.io.File: ...

    @property
    def name(self) -> unicode: ...

    @property
    def projectDir(self) -> java.io.File: ...

    @property
    def projectLockFile(self) -> java.io.File: ...

    @property
    def transient(self) -> bool: ...