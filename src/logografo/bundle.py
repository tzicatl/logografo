import grok

from zope import interface, schema
from zope.container.contained import NameChooser

from logografo import LogografoMessageFactory as _
from logografo import resource
from logografo.app import Logografo

class IEventBundle(interface.Interface):    
    """
    Event Bundle only has 
    """
    title = schema.TextLine(title = _(u'Title'),
                            description= _(u'Give a title to this Bundle, for example: "Scientific discoveries"'),
                            required = True)

    description = schema.Text(title = _(u'Just a brief description of this bundle'),
                              required= False)
    
    def listEvents():
        """
        Returns a list of all events contained in this bundle
        """
        

class EventBundle(grok.Container):
    """
    This is an Event bundle that will group HistoryEvents
    """
    grok.implements(IEventBundle)
    
    title = None
    description = None
    
    def listEvents(self):
        return []
    
    def addHistoryEvent(self, hevent):
        """
        Adds a HistoryEvent to this container.
        """
        name = NameChooser(self.context).chooseName(hevent.title, hevent)
        self[name] = hevent
        
class Edit (grok.EditForm):
    """
    En EditForm for a HistoryEvent. 
    Implicit context is EventBundle
    """
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    form_fields = grok.AutoFields(EventBundle)
    
class Add(grok.AddForm):
    """
    An AddForm for a EventBundle
    """
    grok.context(Logografo)
    form_fields = grok.AutoFields(IEventBundle)
    template = grok.PageTemplateFile('bundle_templates/add.pt')
    label = _(u'Add a bundle of events')
    
    def update(self):
        resource.style.need()
        super(Add, self).update()
    
    @grok.action(_(u'Add Bundle'))
    def add (self, **data):
        bundle = EventBundle()
        self.applyData(bundle, **data)
        self.context.addBundle(bundle)
        return self.redirect(self.url(self.context))
