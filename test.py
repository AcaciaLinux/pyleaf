from re import S
from pyleafcore import *

leafcore = Leafcore()

leafcore.setRootDir("./root")
leafcore.a_update()

packages = ["crosstools"]
leafcore.a_install(packages)
