import os
import site
import importlib
import importlib.util

class Loader():
    def __init__(self) -> None:
        pass

    def getModuleClassFromPath(self, moduleName, modulePath):
        return self.__loadModuleFromPath(moduleName, modulePath)
    
    def getModuleClassFromSitePkgs(self, moduleName):
        pkgPaths = site.getsitepackages()
        userpkgPaths = site.getusersitepackages()
        pkgPaths.append(userpkgPaths)
        return self.__loadModuleFromSitePkgs(moduleName, pkgPaths)
    
    def __loadModuleFromPath(self, moduleName, modulePath):
        for dirPath, dirNames, fileNames in os.walk(modulePath, topdown=True):
            for fileName in fileNames:
                if(moduleName in fileName and fileName.endswith(".py")):
                    fullPath = os.path.join(dirPath, fileName)
                    moduleCls = self.__loadModuleClass(moduleName, fullPath)
                    return moduleCls
    
    def __loadModuleFromSitePkgs(self, moduleName, pkgPaths):
        for pkgPath in pkgPaths:
            for dirPath, dirNames, fileNames in os.walk(pkgPath, topdown=True):
                for fileName in fileNames:
                    if(moduleName in fileName and fileName.endswith(".py")):
                        fullPath = os.path.join(dirPath, fileName)
                        moduleCls = self.__loadModuleClass(moduleName, fullPath)
                        return moduleCls
    
    def __loadModuleClass(self, moduleName, modulePath):
        spec = importlib.util.spec_from_file_location(moduleName, modulePath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls = getattr(module, moduleName)
        return cls