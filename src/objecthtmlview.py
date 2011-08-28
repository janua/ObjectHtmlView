'''
Created on 1 Feb 2011

@author: Francis
'''
import wx
from reportlab.lib.validators import isCallable

class ObjectHtmlView(wx.SimpleHtmlListBox):    
    
    def __init__(self, parent, *args, **kwargs):
        self.object_list = []
        self.renderer = lambda x: str(x)
        wx.SimpleHtmlListBox.__init__(self, parent, *args, **kwargs)
    
    def AddObject(self, obj):
        #self.object_list.append(obj)
        if not self.HasObject(obj):
            self.Insert(self.renderer(obj), self.Count, obj)
    
    def AddObjects(self, obj_list):
        for obj in obj_list:
            self.AddObject(obj)
    
    def RemoveObject(self, obj):
        for index in range(self.Count):
            if self.GetClientData(index) == obj:
                self.Delete(index)
                return
        raise ValueError('This object does not exist')

    def GetObjectCount(self):
        return self.Count
    
    def GetObjectAt(self, index):
        if index < self.Count:
            return self.GetClientData(index)
        raise IndexError('That index does not exist.')
    
    def GetObjects(self):
        for index in range(self.Count):
            yield self.GetClientData(index)
                
    def SetRenderer(self, renderer):
        if not isCallable(renderer):
            raise TypeError('This object is not callable.')
        else:
            self.renderer = renderer
    
    def GetRenderer(self):
        return self.renderer
    
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

    def RefreshObject(self, obj):
        for index in range(self.Count):
            if self.GetClientData(index) is obj:
                self.SetString(index, self.renderer(obj))
        self.Refresh()
    
    def HasObject(self, obj):
        for index in range(self.Count):
            if self.GetClientData(index) is obj:
                return True
        return False

    def GetIndexOf(self, obj):
        for index in range(self.Count):
            if self.GetClientData(index) is obj:
                return index
        raise ValueError('This object does not exist')

    def MoveUp(self, obj):
        obj_index = self.GetIndexOf(obj)
        if obj_index:
            before = self.GetClientData(obj_index-1)
            self.SetClientData(obj_index-1, obj)
            self.SetClientData(obj_index, before)
            self.RefreshObject(obj)
            self.RefreshObject(before)
    
    def MoveDown(self, obj):
        obj_index = self.GetIndexOf(obj)
        if obj_index < self.Count-1:
            after = self.GetClientData(obj_index+1)
            self.SetClientData(obj_index+1, obj)
            self.SetClientData(obj_index, after)
            self.RefreshObject(obj)
            self.RefreshObject(after)
        
        