from typing import overload
import generic.jar
import ghidra.app.script
import ghidra.util.classfinder
import java.io
import java.lang
import java.util.regex


class GhidraScriptProvider(object, ghidra.util.classfinder.ExtensionPoint, java.lang.Comparable):
    """
    A provider that can compile, interpret, load, etc., Ghidra Scripts from a given language.
 
 
     NOTE: ALL GhidraScriptProvider CLASSES MUST END IN "ScriptProvider". If not, the
     ClassSearcher will not find them.
    """





    def __init__(self): ...



    @overload
    def compareTo(self, that: ghidra.app.script.GhidraScriptProvider) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def createNewScript(self, newScript: generic.jar.ResourceFile, category: unicode) -> None:
        """
        Creates a new script using the specified file.
        @param newScript the new script file
        @param category the script category
        @throws IOException if an error occurs writing the file
        """
        ...

    def deleteScript(self, scriptSource: generic.jar.ResourceFile) -> bool:
        """
        Deletes the script file and unloads the script from the script manager.
        @param scriptSource the script source file
        @return true if the script was completely deleted and cleaned up
        """
        ...

    def equals(self, obj: object) -> bool: ...

    def getBlockCommentEnd(self) -> java.util.regex.Pattern:
        """
        Returns a Pattern that matches block comment closings.
 
         <p>
         If block comments are not supported by this provider, then this returns null.
        @return the Pattern for block comment closings, null if block comments are not supported
        """
        ...

    def getBlockCommentStart(self) -> java.util.regex.Pattern:
        """
        Returns a Pattern that matches block comment openings.
 
         <p>
         If block comments are not supported by this provider, then this returns null.
        @return the Pattern for block comment openings, null if block comments are not supported
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCommentCharacter(self) -> unicode:
        """
        Returns the comment character.
 
         <p>
         For example, "//" or "#".
        @return the comment character
        """
        ...

    def getDescription(self) -> unicode:
        """
        Returns a description for this type of script.
        @return a description for this type of script
        """
        ...

    def getExtension(self) -> unicode:
        """
        Returns the file extension for this type of script.
 
         <p>
         For example, ".java" or ".py".
        @return the file extension for this type of script
        """
        ...

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

    def getScriptInstance(self, sourceFile: generic.jar.ResourceFile, writer: java.io.PrintWriter) -> ghidra.app.script.GhidraScript:
        """
        Returns a GhidraScript instance for the specified source file.
        @param sourceFile the source file
        @param writer the print writer to write warning/error messages. If the error prevents
                    success, throw an exception instead. The caller will print the error.
        @return a GhidraScript instance for the specified source file
        @throws GhidraScriptLoadException when the script instance cannot be created
        """
        ...

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

    @property
    def runtimeEnvironmentName(self) -> unicode: ...