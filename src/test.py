#!python3

from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setStringConfig(LeafConfig_string.CONFIG_ROOTDIR, "./root")
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOASK, True)
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOPROGRESS, True)
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_FORCE, False)
leafcore.setStringConfig(LeafConfig_string.CONFIG_PKGLISTURL, "https://api.acacialinux.org/?get=packagelist")
leafcore.setStringConfig(LeafConfig_string.CONFIG_DOWNLOADCACHE, "./leafcache/")
leafcore.a_update()

packages = ["glibc", "readline", "ncurses"]
leafcore.a_install(packages)
 
Upackages = []
leafcore.a_upgrade(Upackages)

Rpackages = ["readline"]
leafcore.a_remove(Rpackages)

print("")
print("----- LEAF DEBUG LOG -----")
print(leafcore.get_log())
