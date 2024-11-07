from typing import List
from typing import overload
import docking.widgets.fieldpanel.field
import ghidra.app.nav
import ghidra.app.util.viewer.field
import ghidra.framework.plugintool
import ghidra.program.model.listing
import java.lang


class GhidraLocalURLAnnotatedStringHandler(ghidra.app.util.viewer.field.URLAnnotatedStringHandler):
    """
    This implementation expands URLAnnotatedStringHandler providing an example form
     of a local project Ghidra URL.
    """





    def __init__(self): ...



    def createAnnotatedString(self, prototypeString: docking.widgets.fieldpanel.field.AttributedString, text: List[unicode], program: ghidra.program.model.listing.Program) -> docking.widgets.fieldpanel.field.AttributedString: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def escapeAnnotationPart(__a0: unicode) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getDisplayString(self) -> unicode: ...

    @overload
    def getPrototypeString(self) -> unicode: ...

    @overload
    def getPrototypeString(self, dislplayText: unicode) -> unicode: ...

    def getSupportedAnnotations(self) -> List[unicode]: ...

    def handleMouseClick(self, annotationParts: List[unicode], navigatable: ghidra.app.nav.Navigatable, serviceProvider: ghidra.framework.plugintool.ServiceProvider) -> bool: ...

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

    @property
    def displayString(self) -> unicode: ...

    @property
    def prototypeString(self) -> unicode: ...