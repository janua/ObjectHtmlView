'''
Created on 1 Feb 2011

@author: Francis
'''
import wx
from reportlab.lib.validators import isCallable

class ObjectHtmlView(wx.SimpleHtmlListBox):    
    
    def __init__(self, parent, *args, **kwargs):
        self.object_list = []
        self.renderer = None
        wx.SimpleHtmlListBox.__init__(self, parent, *args, **kwargs)
    
    def AddObject(self, obj):
        self.object_list.append(obj)
    
    def AddObjects(self, obj_list):
        for obj in obj_list:
            self.AddObject(obj)
    
    def RemoveObject(self, obj):
        self.object_list.remove(obj)

    def GetObjectCount(self):
        return len(self.object_list)
    
    def GetObjectAt(self, index):
        try:
            return self.object_list[index]
        except IndexError:
            raise IndexError('That index does not exist.')
    
    def GetObjects(self):
        return self.object_list

    def SetRenderer(self, renderer):
        if not isCallable(renderer):
            raise TypeError('This object is not callable.')
        else:
            self.renderer = renderer
    
    def GetRenderer(self):
        return self.renderer
    
    def RefreshObjects(self):
        self.Clear()
        for obj in self.object_list:
            rendered = self.renderer(obj)
            self.Insert(rendered, self.Count, obj)
            
    def SelectObject(self, obj):
        for number in range(self.Count):
            if self.GetClientData(number) is obj:
                self.SetSelection(number)
                return True
        raise ValueError('This object does not exist')
    
    def GetSelectedObject(self):
        selection = self.Selection
        if selection > -1:
            return self.GetClientData(selection)
        return None
        