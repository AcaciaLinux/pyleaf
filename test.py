from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setRootDir("./root")
leafcore.a_update()

packages = ["crosstools"]
res = leafcore.a_install(packages)

if (res != 0):
	print("Leafcore error code: {}".format(res))
