from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setRootDir("./root")
leafcore.a_update()
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOASK, True)

packages = ["base"]
leafcore.a_install(packages)
