
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    """ ZenPacks.community.WMIPerf_MSSQL loader
    """

    packZProperties = [
            ('zSQLInstance', 'SQLSERVER', 'string'),
        ]