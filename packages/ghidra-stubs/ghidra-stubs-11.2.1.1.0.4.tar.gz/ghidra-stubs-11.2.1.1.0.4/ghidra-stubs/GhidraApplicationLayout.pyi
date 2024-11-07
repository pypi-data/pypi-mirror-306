from typing import List
from typing import overload
import generic.jar
import ghidra.framework
import java.io
import java.lang
import java.util
import utility.application


class GhidraApplicationLayout(utility.application.ApplicationLayout):
    """
    The Ghidra application layout defines the customizable elements of the Ghidra
     application's directory structure.
    """





    @overload
    def __init__(self):
        """
        Constructs a new Ghidra application layout object.
        @throws IOException if there was a problem getting a user directory or the application 
           properties or modules.
        """
        ...

    @overload
    def __init__(self, applicationInstallationDir: java.io.File):
        """
        Constructs a new Ghidra application layout object using a provided
         application installation directory instead of this layout's default.
         <p>
         This is used when something external to Ghidra needs Ghidra's layout
         (like the Eclipse GhidraDevPlugin).
        @param applicationInstallationDir The application installation directory.
        @throws IOException if there was a problem getting a user directory or the application
           properties.
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getApplicationInstallationDir(self) -> generic.jar.ResourceFile:
        """
        Gets the application installation directory from the application layout.
        @return The application installation directory (or null if not set).
        """
        ...

    def getApplicationProperties(self) -> ghidra.framework.ApplicationProperties:
        """
        Gets the application properties from the application layout
        @return The application properties.  Should never be null.
        """
        ...

    def getApplicationRootDirs(self) -> java.util.Collection:
        """
        Gets the application root directories from the application layout.
        @return A collection of application root directories (or null if not set).
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getExtensionArchiveDir(self) -> generic.jar.ResourceFile:
        """
        Returns the directory where archived application Extensions are stored.  This directory may
         contain both zip files and subdirectories.   This directory is only used inside of an
         installation; development mode does not use this directory.   This directory is used to ship 
         pre-built Ghidra extensions as part of a distribution.
         <P>
         This should be at the following location:<br>
         <ul>
         <li><code>{install dir}/Extensions/Ghidra</code></li>
         </ul>
        @return the application Extensions archive directory.  Could be null if the
           {@link ApplicationLayout} does not support application Extensions.
        """
        ...

    def getExtensionInstallationDirs(self) -> List[generic.jar.ResourceFile]:
        """
        Returns a prioritized {@link List ordered list} of the application Extensions installation 
         directories.   Typically, the values may be any of the following locations:<br>
         <ul>
         <li><code>[user settings dir]/Extensions</code></li>
         <li><code>[application install dir]/Ghidra/Extensions</code> (Release Mode)</li>
         <li><code>ghidra/Ghidra/Extensions</code> (Development Mode)</li>
         </ul>
        @return an {@link List ordered list} of the application Extensions installation directories.
           Could be empty if the {@link ApplicationLayout} does not support application Extensions.
        """
        ...

    def getModules(self) -> java.util.Map:
        """
        Gets the application's modules from the application layout.
        @return The application's modules as a map (mapping module name to module for convenience).
        """
        ...

    def getPatchDir(self) -> generic.jar.ResourceFile:
        """
        Returns the location of the application patch directory.  The patch directory can be
         used to modify existing code within a distribution.
        @return the patch directory; may be null
        """
        ...

    def getUserCacheDir(self) -> java.io.File:
        """
        Gets the user cache directory from the application layout.
        @return The user cache directory (or null if not set).
        """
        ...

    def getUserSettingsDir(self) -> java.io.File:
        """
        Gets the user settings directory from the application layout.
        @return The user settings directory (or null if not set).
        """
        ...

    def getUserTempDir(self) -> java.io.File:
        """
        Gets the user temp directory from the application layout.
        @return The user temp directory (or null if not set).
        """
        ...

    def hashCode(self) -> int: ...

    def inSingleJarMode(self) -> bool:
        """
        Checks whether or not the application is using a "single jar" layout.  Custom application
         layouts that extend this class can override this method once they determine they are in
         single jar mode.
        @return true if the application is using a "single jar" layout; otherwise, false.
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

