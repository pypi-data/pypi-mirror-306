from typing import List
from typing import overload
import generic.jar
import java.lang
import java.util


class GModule(object):
    """
    Represents a module in universe of repos.   This class has the notion of 'shadow' modules, which
     are those modules that live under a repo other than the module root directory, but in the same
     path structure.  This allows for optional repos to be used, adding content to the module when 
     that repo is present.
    """





    def __init__(self, appRoots: java.util.Collection, moduleRoot: generic.jar.ResourceFile): ...



    def accumulateDataFilesByExtension(self, __a0: List[object], __a1: unicode) -> None: ...

    def collectExistingModuleDirs(self, __a0: List[object], __a1: unicode) -> None: ...

    def equals(self, obj: object) -> bool: ...

    def findModuleFile(self, relativeDataFilePath: unicode) -> generic.jar.ResourceFile: ...

    def getClass(self) -> java.lang.Class: ...

    def getFatJars(self) -> java.util.Set: ...

    def getModuleRoot(self) -> generic.jar.ResourceFile: ...

    def getName(self) -> unicode: ...

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
    def fatJars(self) -> java.util.Set: ...

    @property
    def moduleRoot(self) -> generic.jar.ResourceFile: ...

    @property
    def name(self) -> unicode: ...