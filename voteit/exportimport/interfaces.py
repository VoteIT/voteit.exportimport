from zope.interface import Attribute
from zope.interface import Interface


class IExportImport(Interface):
    """ Adapter to export or import content.
        It adapts the site root.
    """
    def __init__(context):
        """ Object to adapt """
    def export_buffer(obj):
        """ Returns filebuffer created from object to export.
        """

    def download_export(obj):
        """ Returns a Response object with an export file.
            It's ment to be passed to the client as a response, and will initiate download.
            The Response.body attr should contain everything from export_buffer method.
        """

    def import_data(parent, name, filedata):
        """ Import data into site, and index the new objects in the catalog.
            parent
                Object where the new data will be stored
            name
                Which key the new data will be stored under, ie parent[name]
            filedata
                Contains a filebuffer, like an open file stream.
        """
