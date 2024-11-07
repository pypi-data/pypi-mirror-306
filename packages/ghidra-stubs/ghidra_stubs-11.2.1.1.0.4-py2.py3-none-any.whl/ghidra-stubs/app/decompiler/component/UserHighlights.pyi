from typing import overload
import java.lang


class UserHighlights(object):
    """
    A class to manage and track Decompiler highlights created by the user via the UI or from a 
     script.  This class manages secondary and global highlights.  For a description of these terms, 
     see ClangHighlightController.
 
     These highlights will remain until cleared explicitly by the user or a client API call.  
     Contrastingly, context highlights are cleared as the user moves the cursor around the Decompiler 
     display.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

