'''
Created on 1 Feb 2011

@author: Francis
'''
import unittest
from objecthtmlview import ObjectHtmlView
import wx

OBJECTS = ({1:2}, {3:4})

class TestObjectHtmlViewAddRemove(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
            
    def test_empty(self):
        self.assertEqual(0, self.ohl.GetObjectCount())
    
    def test_add_object(self):
        self.ohl.AddObject({'an':'object'})
        self.assertEqual(1, self.ohl.GetObjectCount())
    
    def test_add_objects(self):
        self.ohl.AddObjects(OBJECTS)
        self.assertEqual(len(OBJECTS), self.ohl.GetObjectCount())
    
    def test_remove_object(self):
        o = {'an':'object'}
        self.ohl.AddObject(o)
        self.assertEqual(1, self.ohl.GetObjectCount())
        self.ohl.RemoveObject(o)
        self.assertEqual(0, self.ohl.GetObjectCount())
        
    def test_remove_non_existing_object(self):
        self.assertRaises(ValueError, self.ohl.RemoveObject, {})
        
    def test_add_same_object(self):
        o = {'an':'object'}
        self.ohl.AddObject(o)
        self.ohl.AddObject(o)
        self.assertEqual(1, self.ohl.GetObjectCount())

class TestObjectHtmlViewOrder(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
    
    def test_first_position(self):
        o = {'an':'object'}
        self.ohl.AddObject(o)
        self.assertEqual(o, self.ohl.GetObjectAt(0))
    
    def test_second_position(self):
        o, o2 = {'object':'1'}, {'object':'2'}
        self.ohl.AddObjects((o, o2))
        self.assertEqual(o2, self.ohl.GetObjectAt(1))
    
    def test_wrong_index(self):
        self.assertRaises(IndexError, self.ohl.GetObjectAt, 0)

    def test_get_objects(self):
        o, o2 = {'object':'1'}, {'object':'2'}
        self.ohl.AddObjects((o, o2))
        self.assertTrue(o in self.ohl.GetObjects())
        self.assertTrue(o2 in self.ohl.GetObjects())
    
    def test_get_index(self):
        o = {'index':'object'}
        self.ohl.AddObject(o)
        self.assertEqual(0, self.ohl.GetIndexOf(o))

    def test_get_index_two_object(self):
        o, o2 = {'index':'object'}, {'index':'object 2'}
        self.ohl.AddObjects((o, o2))
        self.assertEqual(1, self.ohl.GetIndexOf(o2))
    
    def test_get_index_non_exist(self):
        self.assertRaises(ValueError, self.ohl.GetIndexOf, {'non':'existant'})
        

class TestObjectHtmlViewRendering(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
        
    def test_set_non_callable(self):
        self.assertRaises(TypeError, self.ohl.SetRenderer, {})
        
    def test_set_callable(self):
        def callable(args):
            pass
        self.ohl.SetRenderer(callable)
        self.assertEqual(self.ohl.GetRenderer(), callable)
        
class TestObjectHtmlViewSelection(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
        
        def render(obj):
            return '%s' % obj
        
        self.ohl.SetRenderer(render)
    
    def test_no_selection(self):
        self.assertEqual(None, self.ohl.GetSelectedObject())
        
    def test_select_non_existant_object(self):
        self.assertRaises(ValueError, self.ohl.SelectObject, {})
    
    def test_select_object_one(self):
        o = {'an':'object'}
        self.ohl.AddObject(o)
        self.ohl.SelectObject(o)
        self.assertEqual(o, self.ohl.GetSelectedObject())
    
    def test_select_object_two(self):
        o, o2 = {'an':'object'}, {'object':'2'}
        self.ohl.AddObjects((o, o2))
        self.ohl.SelectObject(o)
        self.assertEqual(o, self.ohl.GetSelectedObject())
        self.ohl.SelectObject(o2)
        self.assertEqual(o2, self.ohl.GetSelectedObject())
    
    def test_select_object_three(self):
        o, o2, o3 = {'an':'object'}, {'object':'2'}, {'o':'2'}
        self.ohl.AddObjects((o, o2, o3))
        self.ohl.SelectObject(o)
        self.assertEqual(o, self.ohl.GetSelectedObject())
        self.ohl.SelectObject(o2)
        self.assertEqual(o2, self.ohl.GetSelectedObject())
        self.ohl.SelectObject(o3)
        self.assertEqual(o3, self.ohl.GetSelectedObject())

class TestObjectHtmlViewRefresh(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
    
    def test_refresh_object(self):
        o = {'text':'lots of text'}
        self.ohl.AddObject(o)
        o['random'] = 'new random string'
        self.ohl.RefreshObject(o)
        self.assertEqual(self.ohl.GetObjectAt(0)['random'], o['random'])
        self.assertEqual(self.ohl.GetString(0), self.ohl.renderer(o))

class TestObjectHtmlViewExistance(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
        
    def test_has_object(self):
        o = {'an':'object'}
        self.ohl.AddObject(o)
        self.assertTrue(self.ohl.HasObject(o))
        
    def test_not_have_object(self):
        self.assertFalse(self.ohl.HasObject({'non':'existant'}))

class TestObjectHtmlViewMovement(unittest.TestCase):
    
    def setUp(self):
        app = wx.PySimpleApp()
        frame = wx.Frame(None)
        self.ohl = ObjectHtmlView(frame)
        frame.Show()
        
    def test_move_up(self):
        o, o2 = {'top':'object'}, {'bottom':'object'}
        self.ohl.AddObjects((o,o2))
        self.ohl.MoveUp(o2)
        self.assertEqual(o2, self.ohl.GetObjectAt(0))
    
    def test_move_down(self):
        o, o2 = {'top':'object'}, {'bottom':'object'}
        self.ohl.AddObjects((o,o2))
        self.ohl.MoveDown(o)
        self.assertEqual(o, self.ohl.GetObjectAt(1))
    
    def test_move_up_top(self):
        o = {'top':'object'}
        self.ohl.AddObject(o)
        self.ohl.MoveUp(o)
        self.assertEqual(0, self.ohl.GetIndexOf(o))
    
    def test_move_bottom(self):
        o = {'top':'object'}
        self.ohl.AddObject(o)
        self.ohl.MoveDown(o)
        self.assertEqual(0, self.ohl.GetIndexOf(o))
    
        
    
if __name__ == '__main__':
    
    unittest.main()
        