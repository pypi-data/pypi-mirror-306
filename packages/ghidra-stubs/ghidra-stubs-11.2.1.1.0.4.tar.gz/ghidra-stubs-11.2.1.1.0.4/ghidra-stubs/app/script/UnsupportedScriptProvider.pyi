from typing import overload
import generic.jar
import ghidra.app.script
import java.io
import java.lang
import java.util.regex


class UnsupportedScriptProvider(ghidra.app.script.GhidraScriptProvider):
    """
    A stub provider for unsupported scripts. These will typically be scripts with supported
     extensions but unsupported ScriptInfo#AT_RUNTIME tags.
    """





    @overload
    def __init__(self): ...

    @overload
    def __init__(self, baseProvider: ghidra.app.script.GhidraScriptProvider):
        """
        Creates a new {@link UnsupportedScriptProvider} that is derived from the given base provider.
         The base provider is any provider with a compatible extension, but without the required
         {@link ScriptInfo#AT_RUNTIME} tag.
        @param baseProvider The base {@link GhidraScriptProvider}
        """
        ...



    @overload
    def compareTo(self, that: ghidra.app.script.GhidraScriptProvider) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def createNewScript(self, newScript: generic.jar.ResourceFile, category: unicode) -> None: ...

    def deleteScript(self, scriptSource: generic.jar.ResourceFile) -> bool:
        """
        Deletes the script file and unloads the script from the script manager.
        @param scriptSource the script source file
        @return true if the script was completely deleted and cleaned up
        """
        ...

    def equals(self, obj: object) -> bool: ...

    def getBlockCommentEnd(self) -> java.util.regex.Pattern: ...

    def getBlockCommentStart(self) -> java.util.regex.Pattern: ...

    def getClass(self) -> java.lang.Class: ...

    def getCommentCharacter(self) -> unicode: ...

    def getDescription(self) -> unicode: ...

    def getExtension(self) -> unicode: ...

    def getRuntimeEnvironmentName(self) -> unicode:
        """
        Returns an optional runtime environment name of a {@link GhidraScriptProvider} that scripts
         can specify they require to run under. Useful for when more than one
         {@link GhidraScriptProvider} uses the same file extension.
        @return an optional runtime environment name of a {@link GhidraScriptProvider} that scripts
         can specify they require to run under (could be null if there is no requirement)
        @see ScriptInfo#AT_RUNTIME
        """
        ...

    def getScriptInstance(self, sourceFile: generic.jar.ResourceFile, writer: java.io.PrintWriter) -> ghidra.app.script.GhidraScript: ...

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
    def blockCommentEnd(self) -> java.util.regex.Pattern: ...

    @property
    def blockCommentStart(self) -> java.util.regex.Pattern: ...

    @property
    def commentCharacter(self) -> unicode: ...

    @property
    def description(self) -> unicode: ...

    @property
    def extension(self) -> unicode: ...