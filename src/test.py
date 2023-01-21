#!python3

from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setStringConfig(LeafConfig_string.CONFIG_ROOTDIR, "./root")
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOASK, True)
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOPROGRESS, True)
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_FORCE, False)
leafcore.setStringConfig(LeafConfig_string.CONFIG_PKGLISTURL, "https://api.acacialinux.org/?get=packagelist");
if (not leafcore.a_update() == 0):
	print("Failed to get package list (code {}): {}".format(leafcore.getLastErrorCode(), leafcore.getLastErrorString()))
	exit(-1)

packages = ["glibc", "readline", "ncurses"]
res = leafcore.a_install(packages)

if (res != 0):
	print("Leafcore error code: {}".format(res))
 
Upackages = []
res = leafcore.a_upgrade(Upackages)

Rpackages = ["readline"]
leafcore.a_remove(Rpackages)

if (res != 0):
	print("Leafcore error code: {}".format(res))

print("")
print("----- LEAF DEBUG LOG -----")
print(leafcore.get_log())
