'''
Created on 2 Feb 2011

@author: Francis
'''
import wx
from objecthtmlview import ObjectHtmlView

O = {'title':'same', 'text':'object!'}

class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self._init_panel()
    
    def _init_panel(self):
        main_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.ohl = ObjectHtmlView(self)
        self.ohl.SetRenderer(renderer)
        
        add_button = wx.Button(self, wx.ID_ANY, 'Add Object')
        self.Bind(wx.EVT_BUTTON, self._handle_add, id=add_button.GetId())                
        
        add_same_button = wx.Button(self, wx.ID_ANY, 'Same Object')
        self.Bind(wx.EVT_BUTTON, self._handle_add_same, id=add_same_button.GetId())  
        
        change_button = wx.Button(self, wx.ID_ANY, 'Change Object')
        self.Bind(wx.EVT_BUTTON, self._handle_change, id=change_button.GetId())      
        
        main_sizer.Add(self.ohl, proportion=1, flag=wx.GROW)
        main_sizer.Add(add_button)
        main_sizer.Add(add_same_button)
        main_sizer.Add(change_button)
        
        self.SetSizer(main_sizer)

    def _handle_add(self, event):
        self.ohl.AddObject({'title':'A title','text':'lots of text lots of text lots of text lots of text lots of text lots of text '})

    def _handle_add_same(self, event):
        self.ohl.AddObject(O)

    def _handle_change(self, event):
        o = self.ohl.GetClientData(1)
        o['text'] = 'Changed Text!'
        self.ohl.RefreshObject(o)

def renderer(obj):
    return '<b><u>%s:</u></b>%s' % (obj['title'], obj['text'])

if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = Frame(None)
    dlg.Show()
    app.MainLoop()