# -*- coding: utf-8 -*-

import sys

#PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
#PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
#PYQT5 QFileDialog, QColorDialog, QDialog

from PyQt5 import QtPrintSupport
#PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
sys.path.append('C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\')
import syntax_pars

import gramatica2 as g
import ts as TS

import principal as p
from expresiones import *
from instrucciones import *
from extensiones import *
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import UniqueDotExporter
errores=[]
contador = 0
class Main(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)

        self.filename = ""

        self.changesSaved = True

        self.initUI()

    def initToolbar(self):

        self.ejecutar= QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\run.png"),"Ejecutar",self)
        self.ejecutar.setShortcut("Ctrl+R")
        self.ejecutar.setStatusTip("Compila los contenidos del editor")
        self.ejecutar.triggered.connect(self.run)


        self.descendente= QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\run.png"),"Ejecutar Descendente",self)
        self.descendente.setShortcut("Ctrl+L")
        self.descendente.setStatusTip("Compila los contenidos del editor desc")
        self.descendente.triggered.connect(self.desc)

        self.debugear= QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\debug.png"),"Debugear",self)
        self.debugear.setShortcut("Ctrl+E")
        self.debugear.setStatusTip("Compila los contenidos paso a paso")
        self.debugear.triggered.connect(self.debug)

        self.newAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\new.png"),"New",self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.printAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\print.png"),"Print document",self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\preview.png"),"Page view",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.findAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\find.png"),"Find and replace",self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\calender.png"),"Insert current date/time",self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        wordCountAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\count.png"),"See word/symbol count",self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        tableAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\table.png"),"Insert table",self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(table.Table(self).show)

        imageAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\image.png"),"Insert image",self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        bulletAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\bullet.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\number.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.ejecutar)
        self.toolbar.addAction(self.descendente)
        self.toolbar.addAction(self.debugear)
        #self.toolbar.addAction(self.printAction)
        #self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        #self.toolbar.addAction(dateTimeAction)
        #self.toolbar.addAction(wordCountAction)
        #self.toolbar.addAction(tableAction)
        #self.toolbar.addAction(imageAction)

        self.toolbar.addSeparator()

        #self.toolbar.addAction(bulletAction)
        #self.toolbar.addAction(numberedAction)

        self.addToolBarBreak()

    def initFormatbar(self):

        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))

        fontSize = QtWidgets.QSpinBox(self)

        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(14)

        fontColor = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\font-color.png"),"Change font color",self)
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)

        underlAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript)

        alignLeft = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")
        run = menubar.addMenu("Run")
        desc = menubar.addMenu("Desc")
        debug = menubar.addMenu("Debug")
        # Add the most important actions to the menubar

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        #file.addAction(self.printAction)
        #file.addAction(self.previewAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        run.addAction(self.ejecutar)
        desc.addAction(self.descendente)
        debug.addAction(self.debugear)
        # Toggling actions for the various bars
        toolbarAction = QtWidgets.QAction("Toggle Toolbar",self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Toggle Formatbar",self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Toggle Statusbar",self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        #view.addAction(formatbarAction)
        #view.addAction(statusbarAction)

    def initUI(self):

        self.text = QtWidgets.QTextEdit(self)
        self.text2 = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("""QTextEdit{
	        font-family:'Consolas'; 
        	color: #ccc; 
	        background-color: #ffffff;}""")
        self.text2.setStyleSheet("""QTextEdit{
	        font-family:'Consolas'; 
        	color: #ccc; 
	        background-color: #000000;}""")    
        highlight = syntax_pars.PythonHighlighter(self.text)
        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        self.initToolbar()
        #self.initFormatbar()
        self.initMenubar()
        
        #self.setCentralWidget(self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)
        self.text.setGeometry(0,55,1000,300)
        self.text2.setGeometry(0,355,1000,300)
        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("Augus")
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\EEGSA\\Documents\\proyecto1vacas-master\\proyecto1vacas-master\\editor\\iconos\\a.png"))

    def changed(self):
        self.changesSaved = False

    def closeEvent(self,event):

        if self.changesSaved:

            event.accept()

        else:
        
            popup = QtWidgets.QMessageBox(self)

            popup.setIcon(QtWidgets.QMessageBox.Warning)
            
            popup.setText("El documento fue modificado")
            
            popup.setInformativeText("¿Desea guardar sus cambios?")
            
            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)
            
            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

    def context(self,pos):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QtGui.QMenu(self)

            appendRowAction = QtWidgets.QAction("Append row",self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QtWidgets.QAction("Append column",self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))


            removeRowAction = QtWidgets.QAction("Remove row",self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QtWidgets.QAction("Remove column",self)
            removeColAction.triggered.connect(self.removeCol)


            insertRowAction = QtWidgets.QAction("Insert row",self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QtWidgets.QAction("Insert column",self)
            insertColAction.triggered.connect(self.insertCol)


            mergeAction = QtWidgets.QAction("Merge cells",self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)


            splitAction = QtWidgets.QAction("Split cells",self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))

            else:
                splitAction.setEnabled(False)


            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)

            menu.addSeparator()

            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)

            menu.addSeparator()

            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)

            menu.addSeparator()

            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)

            if self.formatbar.isVisible():
                pos.setY(pos.y() + 45)
                
            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        else:

            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

            self.text.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(),1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(),1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(),1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(),1)


    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):

        spawn = Main()

        spawn.show()
    def run(self):
        #f = open("./entrada.txt", "r")
        input = self.text.toPlainText()
        #print(input)
        g.cleanErrores()
        
        instrucciones = g.parse(input)
        #print("primer print:",instrucciones)
        
        errores = g.getErrores()
        gram = g.getGramatical()
        ts_global = TS.TablaDeSimbolos()
        
        p.graficar_arbol(instrucciones)
        p.procesar_instrucciones_main(instrucciones, ts_global)
        cadena = p.getCadena()
        print("esto tiene la cadena", cadena)
        if len(errores)>0:
            print("hay errores")
            p.reporte_errores(errores)
        else:
            print("no hay errores")
        p.reporte_tabla_simbolos(ts_global.simbolos)
        p.reporte_gramatica(gram)
        #print("paso el reporte gramatica")
        #p.reporte_tabla_simbolos(ts_global.simbolos)
        #print("paso el reporte ts")
        #print(ts_global.simbolos)
        #print(gram.reverse())
        #print("errores",errores)
        #print("tabla", ts_global)
        self.text2.setText(cadena)

    def desc(self):
        print("descendente")
        #f = open("./entrada.txt", "r")
        #input = self.text.toPlainText()
        #print(input)
        #g2.cleanErrores()
        #instrucciones = g2.parse(input)
        #gram = g2.getGramatical()
        #p.reporte_gramatica(gram)
        #print("primer print:",instrucciones)
        

    def debug(self):
        print("debug")
        global contador
        #f = open("./entrada.txt", "r")
        input = self.text.toPlainText()
        #print(input)
        g.cleanErrores()
        instrucciones = g.parse(input)
        #print("primer print:",instrucciones)
        
        errores = g.getErrores()
        gram = g.getGramatical()
        ts_global = TS.TablaDeSimbolos()
        
        p.graficar_arbol(instrucciones)
        p.procesar_instrucciones_main_debug(instrucciones,contador, ts_global)
        contador += 1
        cadena = p.getCadena()

        if len(errores)>0:
            p.reporte_errores(errores)

        #p.reporte_gramatica(gram)
        p.reporte_tabla_simbolos(ts_global.simbolos)
        #print(ts_global.simbolos)
        #print(gram.reverse())
        #print("errores",errores)
        #print("tabla", ts_global)
        self.text2.setText(cadena)
    def open(self):

        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".","(*.txt)")[0]

        if self.filename:
            with open(self.filename,"rt") as file:
                text = file.read()
               

                self.text.setText(text)
        
    
    def save(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Guardar Cambios')[0]

        if self.filename:
            
            # Append extension if not there yet
            if not self.filename.endswith(".txt"):
              self.filename += ".txt"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename,'wt') as file:
                file.write(self.text.toPlainText())

            self.changesSaved = True

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def wordCount(self):

        wc = wordcount.WordCount(self)

        wc.getText()

        wc.show()

    def insertImage(self):

        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:
            
            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
                popup.show()

            else:

                cursor = self.text.textCursor()

                cursor.insertImage(image,filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()
        
        # Set it as the new text color
        self.text.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()
        

        self.text.setTextBackgroundColor(color)

    def bold(self):

        if self.text.fontWeight() == QtGui.QFont.Bold:

            self.text.setFontWeight(QtGui.QFont.Normal)

        else:

            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def underline(self):

        state = self.text.fontUnderline()

        self.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):

                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self,cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):

                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)


    def bulletList(self):

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
