from ctypes import *

cleaf = cdll.LoadLibrary("libcleaf.so")

cleaf.cleaf_init(17)

class Leafcore():

	def __init__(self):
		self.obj = cleaf.cleafcore_new()

	def __del__(self):
		cleaf.cleafcore_delete(self.obj)

	def setRootDir(self, rootDir):
		cleaf.cleafconfig_setRootDir(bytes(rootDir, encoding='utf-8'))

	def a_update(self):
		cleaf.cleafcore_a_update(self.obj)

	def a_install(self, packages):
		arr = (c_char_p * len(packages))()

		for i in range(0, len(packages)):
			print("Adding argument " + str(i) + ": " + packages[i])
			c_str = (packages[i]).encode('utf-8')
			arr[i] = c_char_p(c_str)

		cleaf.cleafcore_readDefaultPackageList(self.obj)
		cleaf.cleafcore_a_install(self.obj, len(packages), arr)


