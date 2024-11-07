from typing import List
from typing import overload
import java.awt.datatransfer
import java.lang


class ToolButtonTransferable(object, java.awt.datatransfer.Transferable, java.awt.datatransfer.ClipboardOwner):
    """
    Defines data that is available for drag/drop and clipboard transfers.
     The data is a ToolButton object.
    """

    localToolButtonFlavor: java.awt.datatransfer.DataFlavor







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getTransferData(self, f: java.awt.datatransfer.DataFlavor) -> object: ...

    def getTransferDataFlavors(self) -> List[java.awt.datatransfer.DataFlavor]: ...

    def hashCode(self) -> int: ...

    def isDataFlavorSupported(self, f: java.awt.datatransfer.DataFlavor) -> bool: ...

    def lostOwnership(self, clipboard: java.awt.datatransfer.Clipboard, contents: java.awt.datatransfer.Transferable) -> None: ...

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
    def transferDataFlavors(self) -> List[java.awt.datatransfer.DataFlavor]: ...