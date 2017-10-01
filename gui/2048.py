#!/usr/bin/python3.6
__author__='ertuil'
__date__='2017.07.07'

import wx
import random


class FM(wx.Frame):
    def __init__(self):
        super(FM,self).__init__(None,title='2048',size=(350,400))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        self.data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.old_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.score =0


        self.p=wx.Panel(self)
        self.p.SetBackgroundColour((247,247,239))
        self.layout=wx.GridBagSizer(5,5)

        self.scoreLabel=wx.TextCtrl(self.p,-1,value='SCORE:\t0',style=wx.TE_READONLY)
        self.layout.Add(self.scoreLabel,pos=(0,0),span=(1,2),flag=wx.EXPAND)
        self.scoreLabel.SetForegroundColour((255,255,255))
        self.scoreLabel.SetBackgroundColour((189,174,164))

        self.bt=wx.Button(self.p,-1,label='Start!')
        self.layout.Add(self.bt,pos=(0,2),span=(1,2),flag=wx.EXPAND|wx.ALL)
        self.bt.SetForegroundColour((255,125,0))
        self.bt.SetBackgroundColour((247,247,239))
        self.bt.SetDefault()
        self.bt.Bind(wx.EVT_BUTTON,self.OnClicked)

        self.p.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        
        self.labels=[]
        font = wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD)
        for i in range(0,16):
            a=wx.TextCtrl(self.p,-1,value='',size=(80,80),style=wx.TE_READONLY|wx.TE_CENTER)
            a.SetFont(font)
            self.labels.append(a)
            self.layout.Add(self.labels[i],pos=(i//4+1,i%4),flag=wx.ALL,border=2)
        self.p.SetSizer(self.layout)

    def OnClicked(self,event):
        self.bt.SetLabel('RESTART!')
        self.data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.old_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.score =0
        self.scoreLabel.SetValue('SCORE:\t'+str(self.score))
        self.Create()
        self.Flash()
        self.SetFocus()
    
    def Create(self):
        i = random.randint(0,15)
        while self.data[i] != 0:
            i = random.randint(0,15)
        if random.randint(1,4)>3:
            self.data[i]=4
        else:
            self.data[i]=2



    def OnKeyDown(self,event):
        key=event.GetKeyCode()
        ns=[0,0,0,0]
        self.old_data=self.data[:]
        if key == wx.WXK_UP:
            for i in range(0,4):
                for j in range(0,4):
                    ns[j]=self.data[4 * j + i]
                ans=self.Sort(ns)
                for j in range(0,4):
                    self.data[4*j+i]=ans[j]

        elif key == wx.WXK_DOWN:
            for i in range (0,4):
                for j in range(0,4):
                    ns[j]=self.data[12 - 4*j +i]
                ans=self.Sort(ns)
                for j in range(0,4):
                    self.data[12-4*j+i]=ans[j]

        elif key == wx.WXK_LEFT:
            for i in range(0,4):
                for j in range(0,4):
                    ns[j]=self.data[4*i+j]
                ans=self.Sort(ns)
                for j in range(0,4):
                    self.data[4*i+j]=ans[j]

        elif key == wx.WXK_RIGHT:
            for i in range(0,4):
                for j in range(0,4):
                    ns[j]=self.data[3+4*i-j]
                ans=self.Sort(ns)
                for j in range(0,4):
                    self.data[3+4*i-j]=ans[j]
        else :
            event.Skip()
        if self.Verify() == True:
            self.Create()
        self.Flash()
        if self.Success() == True:
            dlg= wx.MessageDialog(None,"Continue?","Successed!",wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
                self.SetTitle("Successed!")
            else :
                self.Close(True)
        if self.Failed() ==True:
            dlg = wx.MessageDialog(None,"Try Again?","Failed",wx.YES_NO)
            if dlg.ShowModal() ==wx.ID_YES:
                dlg.Destroy()
                self.bt.SetLabel('RESTART!')
                self.data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                self.old_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                self.score =0
                self.scoreLabel.SetValue('SCORE:\t'+str(self.score))
                self.Create()
                self.Flash()
                self.SetFocus()
            else :
                dlg.Destroy()

    
    def Verify(self):
        ans = False
        for i in range(0,15):
            if self.old_data[i] != self.data[i]:
                ans = True
        return ans
    
    def Success(self):
        flag = False
        for i in range(0,15):
            if self.data[i] >=2048:
                flag = True
        return flag

    def Failed(self):
        flag = True
        ns=[0,0,0,0]
        for i in range(0,4):
            for j in range(0,4):
                ns[j]=self.data[4 * j + i]
            ans=self.Sort(ns,False)
            for j in range(0,4):
                if ns[j] != ans[j]:
                    flag = False
        for i in range (0,4):
            for j in range(0,4):
                ns[j]=self.data[12 - 4*j +i]
            ans=self.Sort(ns,False)
            for j in range(0,4):
                if ns[j] != ans[j]:
                    flag = False
        for i in range (0,4):
            for j in range(0,4):
                ns[j]=self.data[4*i+j]
            ans=self.Sort(ns,False)
            for j in range(0,4):
                if ns[j] != ans[j]:
                    flag = False
        for i in range (0,4):
            for j in range(0,4):
                ns[j]=self.data[3+4*i-j]
            ans=self.Sort(ns,False)
            for j in range(0,4):
                if ns[j] != ans[j]:
                    flag = False
        return flag      
        
    def Flash(self):
        for i in range(0,16):
            if self.data[i] == 0:
                self.labels[i].SetValue('')
                self.labels[i].SetBackgroundColour((204,192,178))
            else:
                self.labels[i].SetValue(str(self.data[i]))
                if self.data[i]== 2:
                    self.labels[i].SetBackgroundColour((238,228,218))
                elif self.data[i]==4:
                    self.labels[i].SetBackgroundColour((240,224,201))
                elif self.data[i]==8:
                    self.labels[i].SetBackgroundColour((242,177,121))
                elif self.data[i]== 16:
                    self.labels[i].SetBackgroundColour((246,148,99))
                elif self.data[i]==32:
                    self.labels[i].SetBackgroundColour((245,124,95))
                elif self.data[i]==64:
                    self.labels[i].SetBackgroundColour((248,94,60))
                elif self.data[i]==128:
                    self.labels[i].SetBackgroundColour((237,206,113))
                elif self.data[i]==256:
                    self.labels[i].SetBackgroundColour((238,206,99))
                elif self.data[i]==512:
                    self.labels[i].SetBackgroundColour((238,202,99))
                elif self.data[i]==1024:
                    self.labels[i].SetBackgroundColour((238,198,66))
                elif self.data[i]==2048:
                    self.labels[i].SetBackgroundColour((231,190,41))
                elif self.data[i]==4096:
                    self.labels[i].SetBackgroundColour((255,61,58))
                elif self.data[i]>4096:
                    self.labels[i].SetBackgroundColour((255,28,25))
                if self.data[i]<8:
                    self.labels[i].SetForegroundColour((123,113,107))
                else :
                    self.labels[i].SetForegroundColour((255,255,255))
        self.scoreLabel.SetValue('SCORE:\t'+str(self.score))


    def Sort(self,ns,flag=True):
        i=0
        j=0
        js=[0,0,0,0]
        tems=0
        for i in range(0,4):
            if ns[i] !=0:
                js[j]=ns[i]
                j=j+1

        i = 0
        while i < 3:
            if js[i] == js[i + 1] and js[i] != 0 :
                js[i]=js[i] * 2
                tems=tems+js[i]/2
                for j in range(i+1,3):
                    js[j]=js[j+1]
                js[3]=0
                i = - 1
            elif js[i] == js[i + 1] and js[i] == 0 :
                break
            i=i+1
        if flag == True:
            self.score += tems
        return js

if __name__=='__main__':
    app=wx.App()
    FM()
    app.MainLoop()

