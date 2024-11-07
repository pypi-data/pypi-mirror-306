from typing import List
from typing import overload
import ghidra.plugins.fsbrowser
import java.lang
import javax.swing


class FSBIcons(object):
    """
    Static list of Icons for the file system browser plugin and its child windows.
 
     The #getInstance() provides Icons that represent the type 
     and status of a file, based on a filename mapping and caller specified status overlays.
 
     Thread safe
    """

    CLOSE: javax.swing.Icon
    COLLAPSE_ALL: javax.swing.Icon
    COMPRESS: javax.swing.Icon
    COPY: javax.swing.Icon
    CREATE_FIRMWARE: javax.swing.Icon
    CUT: javax.swing.Icon
    DEFAULT_ICON: javax.swing.Icon
    DELETE: javax.swing.Icon
    ECLIPSE: javax.swing.Icon
    EXPAND_ALL: javax.swing.Icon
    EXTRACT: javax.swing.Icon
    FILESYSTEM_OVERLAY_ICON: javax.swing.Icon
    FONT: javax.swing.Icon
    IMPORT: javax.swing.Icon
    IMPORTED_OVERLAY_ICON: javax.swing.Icon
    INFO: javax.swing.Icon
    JAR: javax.swing.Icon
    LIBRARY: javax.swing.Icon
    LINK_OVERLAY_ICON: javax.swing.Icon
    LIST_MOUNTED: javax.swing.Icon
    LOCKED: javax.swing.Icon
    MISSING_PASSWORD_OVERLAY_ICON: javax.swing.Icon
    NEW: javax.swing.Icon
    OPEN: javax.swing.Icon
    OPEN_ALL: javax.swing.Icon
    OPEN_AS_BINARY: javax.swing.Icon
    OPEN_FILE_SYSTEM: javax.swing.Icon
    OPEN_IN_LISTING: javax.swing.Icon
    PASTE: javax.swing.Icon
    PHOTO: javax.swing.Icon
    REDO: javax.swing.Icon
    REFRESH: javax.swing.Icon
    RENAME: javax.swing.Icon
    SAVE: javax.swing.Icon
    SAVE_AS: javax.swing.Icon
    UNDO: javax.swing.Icon
    UNLOCKED: javax.swing.Icon
    VIEW_AS_IMAGE: javax.swing.Icon
    VIEW_AS_TEXT: javax.swing.Icon
    iOS: javax.swing.Icon







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getIcon(self, __a0: unicode, __a1: List[object]) -> javax.swing.Icon: ...

    @staticmethod
    def getInstance() -> ghidra.plugins.fsbrowser.FSBIcons: ...

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

