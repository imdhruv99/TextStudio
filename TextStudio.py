import wx

import wx.lib.dialogs

import wx.stc as stc

import os

faces = {

    'times': 'Times new Roman',

    'mono': 'Courier New',

    'helve': 'Arial',

    'other': 'Comic Sans MS',

    'size': 10,

    'size2': 8,

}


class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        # Hold Current Directory

        self.dirName = ''

        # Hold the File Name

        self.filename = ''

        self.leftMarginWidth = 25

        # Toggle line numbers in preferences menu

        self.lineNumbersEnable = True

        wx.Frame.__init__(self, parent, title=title, size=(800, 600))

        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        # Control + = TO Zoom in

        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)

        # Control - = TO Zoom out

        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        # not show white space

        self.control.SetViewWhiteSpace(False)

        # Line Numbers

        self.control.SetMargins(5, 0)

        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)

        self.control.SetMarginWidth(1, self.leftMarginWidth)

        # status bar

        self.CreateStatusBar()

        self.StatusBar.SetBackgroundColour((220, 220, 220))

        # Menu bar

        # Functionality of File Menu

        fileMenu = wx.Menu()

        new = fileMenu.Append(wx.ID_NEW, "&New", "Create a new Document")

        openFile = fileMenu.Append(wx.ID_OPEN, "&Open", "Open an existing Document")

        save = fileMenu.Append(wx.ID_SAVE, "&Save", "Save the current Document")

        saveAs = fileMenu.Append(wx.ID_SAVEAS, "Save &As", "Save New Document")

        fileMenu.AppendSeparator()

        exitEditor = fileMenu.Append(wx.ID_EXIT, "&Exit", "Close The Application")

        # Functionality of Edit Menu

        editMenu = wx.Menu()

        undo = editMenu.Append(wx.ID_UNDO, "&Undo", "Undo last action")

        redo = editMenu.Append(wx.ID_REDO, "&Redo", "Redo last action")

        editMenu.AppendSeparator()

        selectAll = editMenu.Append(wx.ID_SELECTALL, "&Select All", "Select the entire Document")

        copy = editMenu.Append(wx.ID_COPY, "&Copy", "Copy Selected text")

        cut = editMenu.Append(wx.ID_CUT, "&Cut", "Cut the selected text")

        paste = editMenu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard")

        # Functionality of Preference Menu

        preferenceMenu = wx.Menu()

        lineNumber = preferenceMenu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show/Hide line numbers column")

        # Functionality of Help Menu

        helpMenu = wx.Menu()

        howTo = helpMenu.Append(wx.ID_ANY, "&How to", "Get help using the editor")

        helpMenu.AppendSeparator()

        about = helpMenu.Append(wx.ID_ABOUT, "&about", "Read about the editor and its making")

        # Creating Menu Bar

        menuBar = wx.MenuBar()

        menuBar.Append(fileMenu, "&File")

        menuBar.Append(editMenu, "&Edit")

        menuBar.Append(preferenceMenu, "&Preferences")

        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        # Calling the Functions

        self.Bind(wx.EVT_MENU, self.OnNew, new)

        self.Bind(wx.EVT_MENU, self.OnOpen, openFile)

        self.Bind(wx.EVT_MENU, self.OnSave, save)

        self.Bind(wx.EVT_MENU, self.OnSaveAS, saveAs)

        self.Bind(wx.EVT_MENU, self.onClose, exitEditor)

        self.Bind(wx.EVT_MENU, self.OnUndo, undo)

        self.Bind(wx.EVT_MENU, self.OnRedo, redo)

        self.Bind(wx.EVT_MENU, self.OnSelectAll, selectAll)

        self.Bind(wx.EVT_MENU, self.OnCopy, copy)

        self.Bind(wx.EVT_MENU, self.OnCut, cut)

        self.Bind(wx.EVT_MENU, self.OnPaste, paste)

        self.Bind(wx.EVT_MENU, self.OnToggleLineNUmber, lineNumber)

        self.Bind(wx.EVT_MENU, self.OnHowTo, howTo)

        self.Bind(wx.EVT_MENU, self.OnAbout, about)

        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)

        # Key Bind

        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)

        self.Show()

        self.UpdateLineCol(self)

    # Functions on Menu Bars

    # New File Creating Function

    def OnNew(self, e):

        self.filename = ''

        self.control.SetValue("")

    # Open Document Function

    def OnOpen(self, e):

        try:

            dlg = wx.FileDialog(self, "Choose a file", self.dirName, "", "*.*", wx.FD_OPEN)

            # title ,directory, type, id

            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()

                self.dirName = dlg.GetDirectory()

                f = open(os.path.join(self.dirName, self.filename), 'r')

                self.control.SetValue(f.read())

                f.close()

            dlg.Destroy()

        except FileNotFoundError:

            dlg = wx.MessageDialog(self, "Coudn't open the file", "Error", wx.ICON_ERROR)

            dlg.ShowModal()

            dlg.Destroy()

    # Save Document Function

    def OnSave(self, e):

        try:

            f = open(os.path.join(self.dirName, self.filename), 'w')

            f.write(self.control.GetValue())

        except FileNotFoundError:

            try:

                dlg = wx.FileDialog(self, "Save file as", self.dirName, "Untitled", "*.*",

                                    wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

                if dlg.ShowModal() == wx.ID_OK:
                    self.filename = dlg.GetFilename()

                    self.dirName = dlg.GetDirectory()

                    f = open(os.path.join(self.dirName, self.filename), 'w')

                    f.write(self.control.GetValue())

                    f.close()

                dlg.Destroy()

            except FileNotFoundError:

                pass

    # Save As Function

    def OnSaveAS(self, e):

        try:

            dlg = wx.FileDialog(self, "Save file as", self.dirName, "Untitled", "*.*",

                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()

                self.dirName = dlg.GetDirectory()

                f = open(os.path.join(self.dirName, self.filename), 'w')

                f.write(self.control.GetValue())

                f.close()

            dlg.Destroy()

        except FileExistsError:

            pass

    # Exit Function

    def onClose(self, e):

        self.Close(True)

    # Undo Function

    def OnUndo(self, e):

        self.control.Undo()

    # Redo Function

    def OnRedo(self, e):

        self.control.Redo()

    # Select All Function

    def OnSelectAll(self, e):

        self.control.SelectAll()

    # Copy Function

    def OnCopy(self, e):

        self.control.Copy()

    # Cut Function

    def OnCut(self, e):

        self.control.Cut()

    # Paste Function

    def OnPaste(self, e):

        self.control.Paste()

    # Toggle Line Function

    def OnToggleLineNUmber(self, e):

        if self.lineNumbersEnable:

            self.control.SetMarginWidth(1, 0)

            self.lineNumbersEnable = False

        else:

            self.control.SetMarginWidth(1, self.leftMarginWidth)

            self.lineNumbersEnable = True

    # How To Function

    def OnHowTo(self, e):

        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "This is how to.", "How to", size=(400, 400))

        dlg.ShowModal()

        dlg.Destroy()

    # About Function

    def OnAbout(self, e):

        dlg = wx.MessageDialog(self, "My advance text editor, I made with python3 and wx", " About", wx.OK)

        dlg.ShowModal()

        dlg.Destroy()

    # Update Line and Column Function

    def UpdateLineCol(self, e):

        line = self.control.GetCurrentLine() + 1

        col = self.control.GetColumn(self.control.GetCurrentPos())

        stat = "Line %s, Column %s" % (line, col)

        self.StatusBar.SetStatusText(stat, 0)

    # Making KeyBoard ShortCuts

    def OnCharEvent(self, e):

        keyCode = e.GetKeyCode()

        altDown = e.AltDown()

        # print(keyCode)

        if keyCode == 14:  # Ctrl + N

            self.OnNew(self)

        elif keyCode == 15:  # Ctrl + o

            self.OnOpen(self)

        elif keyCode == 19:  # Ctrl + s

            self.OnSave(self)

        elif altDown and (keyCode == 115):  # Alt + s

            self.OnSaveAS(self)

        elif keyCode == 23:  # Ctrl + w

            self.OnClose(self)

        elif keyCode == 340:  # F1

            self.OnHowTo(self)

        elif keyCode == 341:  # F2

            self.OnAbout(self)

        else:

            e.Skip()

            # pass
            # pass wont work cause then it will check all the keyword so you cant code


# Creating WX Application

app = wx.App()

# Object of MainWindow Class
frame = MainWindow(None, "TextStudio")

app.MainLoop()
