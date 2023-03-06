from ctypes import *
from enum import Enum

cleaf_loaded = False
cleaf = None

class LeafConfig_redownload(Enum):
    REDOWNLOAD_NONE = 0
    REDOWNLOAD_SPECIFIED = 1
    REDOWNLOAD_ALL = 2

class LeafConfig_bool(Enum):
    CONFIG_NOASK = 0
    CONFIG_NOCLEAN = 1
    CONFIG_NOPROGRESS = 2
    CONFIG_FORCE = 3
    CONFIG_FORCEOVERWRITE = 4
    CONFIG_RUNPREINSTALL = 5
    CONFIG_RUNPOSTINSTALL = 6
    CONFIG_INSTALLDEPS = 7
    CONFIG_CHECKREMOTEHASHUPGRADE = 8

class LeafConfig_string(Enum):
    CONFIG_ROOTDIR = 0
    CONFIG_PKGLISTURL = 1
    CONFIG_CACHEDIR = 2
    CONFIG_DOWNLOADDIR = 3
    CONFIG_PACKAGESDIR = 4
    CONFIG_CONFIGDIR = 5
    CONFIG_INSTALLEDDIR = 6
    CONFIG_HOOKSDIR = 7
    CONFIG_PKGLISTPATH = 8
    CONFIG_CHROOTCMD = 9
    CONFIG_RUNSCRIPTSDIR = 10
    CONFIG_DOWNLOADCACHE = 11

class Leafcore():
    def __init__(self):
        self.check_cleaf()

        # Create a new Leafcore instance
        cleaf.cleafcore_new.restype = c_void_p
        self.leafcore = cleaf.cleafcore_new()

    def setVerbosity(self, verbosity):
        # Verbosity from 0 (normal) - 3 (ultraverbose)
        cleaf.cleaf_setLogLevel(verbosity)

    def __del__(self):
        if(not cleaf is None):
            cleaf.cleafcore_delete.argtypes = [c_void_p]
            cleaf.cleafcore_delete(self.leafcore)

    def abort(self):
        cleaf.cleaf_abort()

    def setRedownload(self, redownload: LeafConfig_redownload):
        cleaf.cleafconfig_setRedownload.argtypes = [c_void_p, c_uint]
        cleaf.cleafconfig_setRedownload(self.leafcore, redownload)

    def setBoolConfig(self, config: LeafConfig_bool, value: bool):
        val = 0
        if value:
            val = 1

        cleaf.cleafconfig_setBoolConfig.argtypes = [c_void_p, c_uint, c_int]
        cleaf.cleafconfig_setBoolConfig(self.leafcore, config.value, val)

    def getBoolConfig(self, config: LeafConfig_bool):
        cleaf.cleafconfig_getBoolConfig.restype = c_int
        cleaf.cleafconfig_getBoolConfig.argtypes = [c_void_p, c_uint]
        return cleaf.cleafconfig_getBoolConfig(self.leafcore, config.value)

    def setStringConfig(self, config: LeafConfig_string, option: str):
        cleaf.cleafconfig_setStringConfig.restype = c_int
        cleaf.cleafconfig_setStringConfig.argtypes = [c_void_p, c_uint, c_char_p]
        cleaf.cleafconfig_setStringConfig(self.leafcore, config.value, bytes(option, encoding='utf-8'))

    def getStringConfig(self, config: LeafConfig_string):
        cleaf.cleaf_getStringConfig.restype = c_void_p
        resP = cleaf.cleaf_getString()
        log = c_char_p(resP)

        if (resP == 0):
            return "[pyleaf] FAILED TO RETRIEVE LOG"

        string = str(log.value.decode('utf-8'))

        cleaf.cleaf_delete_log.argtypes = [c_void_p]
        cleaf.cleaf_delete_log(resP)

        return string

    def a_update(self):
        cleaf.cleafcore_a_update.restype = c_int
        cleaf.cleafcore_a_update.argtypes = [c_void_p]
        return cleaf.cleafcore_a_update(self.leafcore)

    def a_install(self, packages):
        arr = (c_char_p * len(packages))()

        for i in range(0, len(packages)):
            c_str = (packages[i]).encode('utf-8')
            arr[i] = create_string_buffer(c_str).raw

        cleaf.cleafcore_a_install.restype = c_int
        cleaf.cleafcore_a_install.argtypes = [c_void_p, c_uint, (c_char_p * len(packages))]
        return cleaf.cleafcore_a_install(self.leafcore, len(packages), arr)

    def a_installLocal(self, packages):
        arr = (c_char_p * len(packages))()

        for i in range(0, len(packages)):
            c_str = (packages[i]).encode('utf-8')
            arr[i] = create_string_buffer(c_str).raw

        cleaf.cleafcore_a_installLocal.restype = c_int
        cleaf.cleafcore_a_installLocal.argtypes = [c_void_p, c_uint, (c_char_p * len(packages))]
        return cleaf.cleafcore_a_installLocal(self.leafcore, len(packages), arr)
    
    def a_upgrade(self, packages):
        arr = (c_char_p * len(packages))()

        for i in range(0, len(packages)):
            print("Adding argument " + str(i) + ": " + packages[i])
            c_str = (packages[i]).encode('utf-8')
            arr[i] = c_char_p(c_str)

        cleaf.cleafcore_a_upgrade.restype = c_int
        cleaf.cleafcore_a_upgrade.argtypes = [c_void_p, c_int, (c_char_p * len(packages))]
        return cleaf.cleafcore_a_upgrade(self.leafcore, len(packages), arr)

    def a_remove(self, packages):
        arr = (c_char_p * len(packages))()

        for i in range(0, len(packages)):
            c_str = (packages[i]).encode('utf-8')
            arr[i] = create_string_buffer(c_str).raw

        cleaf.cleafcore_a_remove.restype = c_int
        cleaf.cleafcore_a_remove.argtypes = [c_void_p, c_uint, (c_char_p * len(packages))]
        return cleaf.cleafcore_a_remove(self.leafcore, len(packages), arr)

    def check_cleaf(self):
        global cleaf_loaded
        global cleaf

        if (not cleaf_loaded):
            cleaf = cdll.LoadLibrary("libcleaf.so")
            cleaf_loaded = True
            # Initialize the cleaf api, only do this once
            # because it allocates a new Log module instance
            # Set the loglevel to LOGLEVEL_U
            cleaf.cleaf_init.argtypes = [c_uint]
            cleaf.cleaf_init(3)

    def getLastErrorCode(self):
        cleaf.cleafcore_getError.restype = c_uint16
        cleaf.cleafcore_getError.argtypes = [c_void_p]
        return cleaf.cleafcore_getError(self.leafcore)

    def getLastErrorString(self):
        cleaf.cleafcore_getErrorString.restype = c_void_p
        cleaf.cleafcore_getErrorString.argtypes = [c_void_p]
        resP = cleaf.cleafcore_getErrorString(self.leafcore)
        log = c_char_p(resP)

        if (resP == 0):
            return "[pyleaf] FAILED TO RETRIEVE ERROR STRING"

        string = str(log.value.decode('utf-8'))

        #TODO: free memory

        return string

    def get_log(self):
        cleaf.cleaf_get_log.restype = c_void_p
        resP = cleaf.cleaf_get_log()
        log = c_char_p(resP)

        if (resP == 0):
            return "[pyleaf] FAILED TO RETRIEVE LOG"

        string = str(log.value.decode('utf-8'))

        #TODO: free memory

        return string

    def clear_log(self):
        cleaf.cleaf_clear_log()
