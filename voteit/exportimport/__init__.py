from pyramid.i18n import TranslationStringFactory

ExportImportMF = TranslationStringFactory('voteit.exportimport')


def includeme(config):
    """ Include ExportImport adapter and register views."""
    config.scan('voteit.exportimport')

    from voteit.exportimport.models import ExportImport
    from voteit.core.models.interfaces import ISiteRoot
    from voteit.exportimport.interfaces import IExportImport
    config.registry.registerAdapter(ExportImport, (ISiteRoot,), IExportImport)