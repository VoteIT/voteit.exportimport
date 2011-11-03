import colander
import deform
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.security import has_permission
from betahaus.pyracont.factories import createSchema
from betahaus.viewcomponent.decorators import view_action
from voteit.core.views.base_view import BaseView
from voteit.core.models.interfaces import IBaseContent
from voteit.core.security import MANAGE_SERVER

from voteit.exportimport.interfaces import IExportImport
from voteit.exportimport import ExportImportMF as _


button_cancel = deform.Button('cancel', _(u"Cancel"))
button_import = deform.Button('import', _(u"Import"))
button_export = deform.Button('export', _(u"Export and download"))


class ExportImportView(BaseView):
    """ Handle export and import of database objects. """
    
    @view_config(name = '_export', context = IBaseContent, renderer = "voteit.core:views/templates/base_edit.pt")
    def export_view(self):
        redirect_url = resource_url(self.context, self.request)
        if not has_permission(MANAGE_SERVER, self.api.root, self.request):
            raise HTTPForbidden("You're not allowed to access this view")
        export_import = self.request.registry.queryAdapter(self.api.root, IExportImport)
        if not export_import:
            msg = _(u"ExportImport component not included in VoteIT. You need to register it to use this.")
            self.api.flash_messages.add(msg, type = 'error')
            return HTTPFound(location=redirect_url)

        form = deform.Form(colander.Schema(), buttons=(button_export, button_cancel))
        self.api.register_form_resources(form)

        if 'export' in self.request.POST:
            return export_import.download_export(self.context)
        
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))
            return HTTPFound(location=redirect_url)

        #No action
        msg = _(u"Export current context")
        self.api.flash_messages.add(msg, close_button=False)
        self.response['form'] = form.render()
        return self.response

    @view_config(name = '_import', context = IBaseContent, renderer = "voteit.core:views/templates/base_edit.pt")
    def import_view(self):
        if not has_permission(MANAGE_SERVER, self.api.root, self.request):
            raise HTTPForbidden("You're not allowed to access this view")
        redirect_url = resource_url(self.context, self.request)
        export_import = self.request.registry.queryAdapter(self.api.root, IExportImport)
        if not export_import:
            msg = _(u"ExportImport component not included in VoteIT. You need to register it to use this.")
            self.api.flash_messages.add(msg, type = 'error')
            return HTTPFound(location=redirect_url)
        schema = createSchema('ImportSchema').bind(context = self.context, request = self.request)
        form = deform.Form(schema, buttons=(button_import, button_cancel))
        self.api.register_form_resources(form)

        if 'import' in self.request.POST:
            controls = self.request.params.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response

            name = appstruct['name']
            filedata = appstruct['upload']
            export_import.import_data(self.context, name, filedata['fp'])
            filedata.clear()
            self.api.flash_messages.add(_(u"Created new objects from import"))
            return HTTPFound(location=redirect_url)

        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))
            return HTTPFound(location=redirect_url)

        #No action
        msg = _(u"Import file to current context")
        self.api.flash_messages.add(msg, close_button=False)
        self.response['form'] = form.render()
        return self.response

@view_action('context_actions', 'export', title = _(u"Export this"), viewname = '_export')
@view_action('context_actions', 'import', title = _(u"Import here"), viewname = '_import')
def exportimport_context_action(context, request, va, **kw):
    api = kw['api']
    if not api.context_has_permission(MANAGE_SERVER, api.root):
        return ''
    url = "%s%s" % (api.resource_url(context, request), va.kwargs['viewname'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
