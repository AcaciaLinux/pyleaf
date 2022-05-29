from ctypes import *

class Leafcore():

	def __init__(self):
        self.cleaf = cdll.LoadLibrary("libcleaf.so")
        self.cleaf.cleaf_setLogLevel(0)
        self.obj = self.cleaf.cleafcore_new()
        
    def setVerbosity(self, verbosity):
        # Verbosity from 0 (normal) - 3 (ultraverbose)
        self.cleaf.cleaf_setLogLevel(verbosity)

	def __del__(self):
		self.cleaf.cleafcore_delete(self.obj)

	def setRootDir(self, rootDir):
		self.cleaf.cleafconfig_setRootDir(bytes(rootDir, encoding='utf-8'))

	def a_update(self):
		self.cleaf.cleafcore_a_update(self.obj)

	def a_install(self, packages):
		arr = (c_char_p * len(packages))()

		for i in range(0, len(packages)):
			print("Adding argument " + str(i) + ": " + packages[i])
			c_str = (packages[i]).encode('utf-8')
			arr[i] = c_char_p(c_str)

		self.cleaf.cleafcore_readDefaultPackageList(self.obj)
		self.cleaf.cleafcore_a_install(self.obj, len(packages), arr)


