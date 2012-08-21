# -*- coding: utf-8 -*-
import os, traceback, logging, datetime
import win32com.client
import pythoncom

from win32com.client import DispatchEx
from sys2do.util.common import *

__all__ = ["ExcelBasicGenerator", ]


class ExcelBasicGenerator:

    XlBordersIndex = {
                  "xlDiagonalDown" : 5,
                  "xlDiagonalUp" : 6,
                  "xlEdgeBottom" : 9,
                  "xlEdgeLeft" : 7,
                  "xlEdgeRight" : 10,
                  "xlEdgeTop" : 8,
                  "xlInsideHorizontal" : 12,
                  "xlInsideVertical" : 11,
                  }


    XlBorderWeight = {
                  "xlHairline" : 1,
                  "xlThin" : 2,
                  "xlMedium" : 3,
                  "xlThick" : 4
                  }


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


    def _drawCellLine(self, sheet, left, top, right, bottom):
        sheet_range = "%s%s:%s%s" % (left, top, right, bottom)
        for line in ["xlEdgeBottom", "xlEdgeLeft", "xlEdgeRight", "xlEdgeTop"]:
            sheet.Range(sheet_range).Borders(self.XlBordersIndex[line]).Weight = self.XlBorderWeight["xlMedium"]
            sheet.Range(sheet_range).Borders(self.XlBordersIndex[line]).LineStyle = 1
        for line in ["xlInsideHorizontal", "xlInsideVertical"]:
            sheet.Range(sheet_range).Borders(self.XlBordersIndex[line]).Weight = self.XlBorderWeight["xlThin"]
            sheet.Range(sheet_range).Borders(self.XlBordersIndex[line]).LineStyle = 1



class SummaryReport(ExcelBasicGenerator):
    def inputData(self, data):
        excelSheet = self.workBook.Sheets(1)
        startRow = 2
        row = len(data)
        col = len(data[0])
        lastRow = startRow + row
        excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), startRow + row - 1)).Value = data



class ProfitReport(ExcelBasicGenerator):
    def inputData(self, data):
        excelSheet = self.workBook.Sheets(1)
        startRow = 2
        row = len(data)
        col = len(data[0])
        lastRow = startRow + row - 1
        excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), lastRow)).Value = data
        self._drawCellLine(excelSheet, "A", startRow, number2alphabet(col), lastRow)

