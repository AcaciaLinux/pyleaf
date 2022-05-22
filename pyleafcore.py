from ctypes import cdll

cleaf = cdll.LoadLibrary("libcleaf.so")

cleaf.cleaf_init(17)

class Leafcore():

	def __init__(self):
		self.obj = cleaf.cleaf_new()

	def __del__(self):
		cleaf.cleaf_delete(self.obj)
