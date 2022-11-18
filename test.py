#!python3

from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setRootDir("./root")
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOASK, True)
leafcore.a_update()

packages = ["base"]
res = leafcore.a_install(packages)

if (res != 0):
	print("Leafcore error code: {}".format(res))
