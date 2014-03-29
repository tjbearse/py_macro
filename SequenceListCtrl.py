import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, TextEditMixin
from KeySequence import Parse, ParseError


""" holds text and parsed output """
class KeySequenceHolder(object):
    def __init__(self, text=""):
        self.text = text
        self.parsed = []
        
        
class SequenceListCtrl(wx.ListCtrl, TextEditMixin, ListCtrlAutoWidthMixin):
    """List style control for editing and displaying sequences of keys to run"""
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style | wx.LC_VIRTUAL)
        ListCtrlAutoWidthMixin.__init__(self)
        TextEditMixin.__init__(self) 
                
        self.sequences = []
        
        self.SetItemCount(0)
        
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnModified, self)

    def OnGetItemText(self, item, column):
        return self.sequences[item].text
    
    def SetVirtualData(self, row, col, text):
        self.sequences[row].text = text
    
    
    ''' methods '''
    def InsertNew(self, index=0):
        """Inserts a new row, initialized to repeat=1 and blank sequence.
            rows are zero indexed
        """
        print "insert, indx = ", index
        assert(0 <= index <= len(self.sequences))
        self.sequences.insert(index, KeySequenceHolder())
        self.SetItemCount(len(self.sequences))
        self.Refresh()

    def Delete(self, index):
        """Deletes the specified row (zero indexed)"""
        assert(0 <= index <= len(self.sequences))
        self.sequences.pop(index)
        self.SetItemCount(len(self.sequences))
        self.Refresh()
        

    def Move(self, index, dest):
        assert(0 <= index <= len(self.sequences))
        assert(0 <= dest <= len(self.sequences))
        item = self.sequences.pop(index)
        self.sequences.insert(dest, item)
        self.Refresh()
        
        
        
    '''Event Handlers'''
        
    def OnModified(self, event):
        # validate
        if event.GetColumn() == 1 :
            try:
                interp = Parse(event.GetText())
                event.Allow()
                event.GetItem().parsed = interp
            except ParseError:
                event.Veto()
        print "made it", event.GetIndex()
        if event.GetIndex() == len(self.sequences)-1:
            self.InsertNew(len(self.sequences)) 
                
                