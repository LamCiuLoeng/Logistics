# -*- coding: utf-8 -*-
import os, traceback, logging, datetime
import win32com.client
import pythoncom

from win32com.client import DispatchEx
from common import *
from sys2do.util.common import number2alphabet

__all__ = ["ExcelBasicGenerator", ]


class ExcelBasicGenerator:
    def __init__(self, templatePath = None, destinationPath = None, overwritten = True):
        #solve the problem when create the excel at second time ,the exception is occur.
        pythoncom.CoInitialize()

        self.excelObj = DispatchEx('Excel.Application')
        self.excelObj.Visible = False

        if templatePath and os.path.exists(templatePath):
            self.workBook = self.excelObj.Workbooks.open(templatePath)
        else:
            self.workBook = self.excelObj.Workbooks.Add()

        self.destinationPath = os.path.normpath(destinationPath) if destinationPath else None
        self.overwritten = overwritten

    def inputData(self): pass

    def outputData(self):
        try:
            if not self.destinationPath : pass
            elif os.path.exists(self.destinationPath):
                if self.overwritten:
                    os.remove(self.destinationPath)
                    self.excelObj.ActiveWorkbook.SaveAs(self.destinationPath)
            else:
                self.excelObj.ActiveWorkbook.SaveAs(self.destinationPath)
        except:
            traceback.print_exc()
        finally:
            try:
                self.workBook.Close(SaveChanges = 0)
            except:
                traceback.print_exc()

    def clearData(self):
        try:
            if hasattr(self, "workBook"): self.workBook.Close(SaveChanges = 0)
        except:
            traceback.print_exc()





class SummaryReport(ExcelBasicGenerator):
    def inputData(self, data):
        excelSheet = self.workBook.Sheets(1)
        startRow = 2
        row = len(data)
        col = len(data[0])
        lastRow = startRow + row
        excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), startRow + row - 1)).Value = data



