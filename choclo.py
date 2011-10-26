#! /usr/bin/env python
# -.- coding: utf-8 -.-

# sennon
# singnote
# full
#http://code.activestate.com/recipes/180670-generate-thumbnail-image/
#http://www.daniweb.com/software-development/python/code/216466
import os, os.path, sys
from PIL import Image
import wx

class Application(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Chocle - Image Thumbnails', size=(320, 200))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        #btn_src = wx.Button(self, -1, "選擇原圖目錄", (30,30))
        #self.Bind(wx.EVT_BUTTON, self.OnButtonSource, btn_src)

        #btn_tgt = wx.Button(self, -1, "換縮圖目錄", (80,30))
        #self.Bind(wx.EVT_BUTTON, self.OnButtonSource, btn_src)

        #txt = wx.StaticText(panel, -1, 'Hello World!')
        #sizer.Add(txt, 0, wx.TOP|wx.LEFT, 20)


        resolution_options = ['640x480', '800x600', '1024x768', 'custom']

        sizer = wx.BoxSizer(wx.VERTICAL)

        radio_resol = wx.RadioBox(
            panel, -1, "Resolution", (10,70), wx.DefaultSize,
            resolution_options, 1, wx.RA_SPECIFY_COLS
            )


        txt_src = wx.TextCtrl(panel, -1, "", (100, 10), (200, 30))
        btn_src = wx.Button(panel, -1, "Browse...", (10, 10))
        txt_resol = wx.TextCtrl(panel, -1, "", (100, 100), (50, 30))
        btn_make = wx.Button(panel, -1, "Make Thumb", (10, 140) )
        #sizer.Add(src_btn, 0 , wx.LEFT, 20)
        #sizer.Add(src_btn, 10 , wx.LEFT, 120)
        #sizer.Add(resol_radio, 20 , wx.RIGHT|wx.TOP, 220)

        self.source_tc = txt_src
        self.resol_tc = txt_resol
        self.resol_rd = radio_resol
        self.source_dir = ''
        self.source_files = []

        self.Bind(wx.EVT_BUTTON, self.OnButtonSource, btn_src)
        self.Bind(wx.EVT_BUTTON, self.OnButtonMake, btn_make)

        self.Centre()
        self.Show(True)

    def OnButtonSource(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            get_path = dlg.GetPath()
            self.source_tc.WriteText(get_path)
            self.source_dir = get_path

            # find all image files and add to self.source_files
            for path, dirs, files in os.walk(get_path, topdown=False):
                total_files = len(files)        
                for name in files: 
                    source = os.path.join(path, name)
                    self.source_files.append(source)


    def OnButtonMake(self, evt):
        get_resol = self.resol_rd.GetSelection()
        if get_resol == 0:
            resol = 800
        elif get_resol == 1:
            resol = 600
        elif get_resol == 2:
            resol = self.resol_tc.GetValue()

        target_dir = os.path.join(self.source_dir, "thumbs")
        if os.path.exists(target_dir) == 0:
            os.mkdir(target_dir)

        for f in self.source_files:
            target_f = os.path.join(target_dir, os.path.basename(f))
            #print 'make thumb of %s to %s' % (f, target_f)
            im = Image.open(f)     
            im.thumbnail((resol, resol), Image.ANTIALIAS)
            im.save(target_f, "JPEG")
            print 'done!'
"""
  #print results
                fsize = round(os.path.getsize(target) / 100) / 10
                print target + " - " + str(fsize) + " kB"
"""

if __name__ == '__main__':
    app = wx.App(0)
    Application(None)
    app.MainLoop()

