import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from voteit.exportimport import ExportImportMF as _


IMPORT_NAME_REGEXP = r"[a-z\-0-9]{2,20}"


class MemoryTmpStore(dict):
    """ Instances of this class implement the
        deform.interfaces.FileUploadTempStore interface.
        It will be shared across threads, so don't use it for anything
        important.
        It's usable as a buffer for uploaded files while validation occurs.
    """
    def preview_url(self, uid):
        return None

#Note: Don't use this instantiated version for anything else! They'll contain the same data! :)
tmpstore = MemoryTmpStore()


@schema_factory('ImportSchema')
class ImportSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(),
                               title = _(u"Name, will be part of the url"),
                               description = _(u"Lowercase, numbers or hyphen is ok."),
                               validator = colander.Regex(IMPORT_NAME_REGEXP),)
    upload = colander.SchemaNode(
        deform.FileData(),
        title = _(u"Upload ZEXP file."),
        widget=deform.widget.FileUploadWidget(tmpstore)
    )
