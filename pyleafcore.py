from ctypes import *

cleaf_loaded = False
cleaf = None

class Leafcore():
    def __init__(self):
        self.check_cleaf()

        # Create a new Leafcore instance
        self.leafcore = cleaf.cleafcore_new()

    def setVerbosity(self, verbosity):
        # Verbosity from 0 (normal) - 3 (ultraverbose)
        cleaf.cleaf_setLogLevel(verbosity)

    def __del__(self):
	    cleaf.cleafcore_delete(self.leafcore)

    def setRootDir(self, rootDir):
        cleaf.cleafconfig_setRootDir(bytes(rootDir, encoding='utf-8'))

    def a_update(self):
	    cleaf.cleafcore_a_update(self.leafcore)

    def a_install(self, packages):
        arr = (c_char_p * len(packages))()

        for i in range(0, len(packages)):
            print("Adding argument " + str(i) + ": " + packages[i])
            c_str = (packages[i]).encode('utf-8')
            arr[i] = c_char_p(c_str)

        cleaf.cleafcore_readDefaultPackageList(self.leafcore)
        cleaf.cleafcore_parseInstalled(self.leafcore)
        cleaf.cleafcore_a_install(self.leafcore, len(packages), arr)

    def check_cleaf(self):
        global cleaf_loaded
        global cleaf
        
        if (not cleaf_loaded):
            cleaf = cdll.LoadLibrary("libcleaf.so")
            cleaf_loaded = True
            # Initialize the cleaf api, only do this once
            # because it allocates a new Log module instance
            # Set the loglevel to LOGLEVEL_U
            cleaf.cleaf_init(2)
