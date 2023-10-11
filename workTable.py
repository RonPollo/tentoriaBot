from tables import Spreadsheet
import googleapiclient.errors
from pprint import pprint

GOOGLE_CREDENTIALS_FILE = 'tablesApi.json'

class Table: 
    def __init__(self, GOOGLE_CREDENTIALS_FILE, id=None) -> None:
        self.ss = Spreadsheet(GOOGLE_CREDENTIALS_FILE, debugMode = True)
        if id:
            self.ss.setSpreadsheetById(id)
        

    def create_sheets(self, surname):
        try:
            print(self.ss.addSheet(f'{surname}', 250, 20))
        except googleapiclient.errors.HttpError:
            print("Could not add sheet! Maybe sheet with same name already exists!")

    def create_struct_for_sheet(self):

        self.ss.prepare_setCellsFormat("A1:A2", {"textFormat": {"bold": True}, "verticalAlignment": "MIDDLE","horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("B1:C1", {"textFormat": {"bold": True}, "verticalAlignment": "MIDDLE","horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("H1:I1", {"textFormat": {"bold": True}, "verticalAlignment": "MIDDLE","horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("O1:P1", {"textFormat": {"bold": True}, "verticalAlignment": "MIDDLE","horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("R1:S1", {"textFormat": {"bold": True}, "verticalAlignment": "MIDDLE","horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("B1:B1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("F1:F1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("B2:B2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("C2:C2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("D1:D1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("E1:E1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("F1:F1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("G1:G1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("H1:H1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("H2:H2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("T2:T2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("I2:I2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("J2:J2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("K1:K1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("L1:L1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("M1:M1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("N1:N1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("O1:O1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("O2:O2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("Q2:Q2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("P2:P2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("Q1:Q1", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("R2:R2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("S2:S2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})
        self.ss.prepare_setCellsFormat("T2:T2", {"textFormat": {"bold": True}, "horizontalAlignment": "CENTER"})

        self.ss.prepare_mergeCells('A1:A2')
        self.ss.prepare_setValues('A1:A1', [['дата']])
        self.ss.prepare_mergeCells('B1:C1')
        self.ss.prepare_mergeCells('H1:J1')
        self.ss.prepare_mergeCells('P1:Q1') 
        self.ss.prepare_mergeCells('S1:T1') 
        self.ss.prepare_setValues('B1:B1', [['пробег']])
        
        self.ss.prepare_setValues('D1:D1', [['расход']])
        
        self.ss.prepare_setValues('B2:B2', [['начало']])
        self.ss.prepare_setValues('C2:C2', [['конец']])

        self.ss.prepare_setValues('E1:E1', [['перерасход']])
        self.ss.prepare_setValues('F1:F1', [['z-отчет']])
        self.ss.prepare_setValues('G1:G1', [['терминал']])
        self.ss.prepare_setValues('H1:H1', [['банк']])
        self.ss.prepare_setValues('H2:H2', [['должно']])
        self.ss.prepare_setValues('I2:I2', [['сдано']])
        self.ss.prepare_setValues('J2:J2', [['недостаточно']])
        self.ss.prepare_setValues('K1:K1', [['Viza']])
        self.ss.prepare_setValues('L1:L1', [['ЗНФ']])
        self.ss.prepare_setValues('M1:M1', [['Личный счет']])
        self.ss.prepare_setValues('N1:N1', [['бонусы']])
        self.ss.prepare_setValues('O1:O1', [['карта онлайн']])
        self.ss.prepare_setValues('P1:P1', [['яндекс']])
        self.ss.prepare_setValues('P2:P2', [['нал']])
        self.ss.prepare_setValues('Q2:Q2', [['безнал']])
        self.ss.prepare_setValues('R1:R1', [['итого']])
        self.ss.prepare_setValues('S1:S1', [['зарплата']])
        self.ss.prepare_setValues('S2:S2', [['%']])
        self.ss.prepare_setValues('T2:T2', [['выплата']])    
        self.run()
        

    def add_items(self, data):


        row = self.__get_row()
        if data['washing_type'] == 'Наличные':
            washing_count = data['washing']
        else:
            washing_count = 0
        
        if data['azs_type'] == 'Наличные':
            azs_count = data['azs']
        else:
            azs_count = 0

        
        total_shift = data['terminal'] + data['viza_discount'] + data['cash_bavaria'] + data['cash_card'] + data['znf'] + data['bonuse'] + data['yandex_nal'] + data['yandex_bez'] + data['perscash']
        total_shift = round(total_shift, 2)
        total_cash = data['yandex_nal'] + data['cash_bavaria'] - washing_count - azs_count
        flaw_cash = total_cash - data['over_cash']

        self.ss.prepare_setValues(f'A{row}:A{row}', [[data['date']]])
        self.ss.prepare_setValues(f'B{row}:B{row}', [[data['first_distance']]])
        self.ss.prepare_setValues(f'C{row}:C{row}', [[data['last_distance']]])
        self.ss.prepare_setValues(f'F{row}:F{row}', [[data['z_index']]])
        self.ss.prepare_setValues(f'G{row}:G{row}', [[data['terminal']]])
        self.ss.prepare_setValues(f'H{row}:H{row}', [[total_cash]])
        self.ss.prepare_setValues(f'I{row}:I{row}', [[data['over_cash']]])
        self.ss.prepare_setValues(f'J{row}:J{row}', [[flaw_cash]])
        self.ss.prepare_setValues(f'K{row}:K{row}', [[data['viza_discount']]])
        self.ss.prepare_setValues(f'L{row}:L{row}', [[data['znf']]])
        self.ss.prepare_setValues(f'M{row}:M{row}', [[data['perscash']]])
        self.ss.prepare_setValues(f'N{row}:N{row}', [[data['bonuse']]])
        self.ss.prepare_setValues(f'O{row}:O{row}', [[data['cash_card']]])
        self.ss.prepare_setValues(f'P{row}:P{row}', [[data['yandex_nal']]])
        self.ss.prepare_setValues(f'Q{row}:Q{row}', [[data['yandex_bez']]])
        self.ss.prepare_setValues(f'R{row}:R{row}', [[total_shift]])
        self.ss.prepare_setValues(f'S{row}:S{row}', [['23%']])
        self.ss.prepare_setValues(f'T{row}:T{row}', [[total_shift * 0.23]])
    
    def __get_row(self):
        row = 3
        while True:
            data = self.ss.getCellValue(f'A{row}:A{row}')
            print(data)
            if  data:
                row += 1
                
            else:
                return row 
            
    def is_have_list(self, list):
        if list in  self.ss.getSheetNames():
            return True
        
        return False

    def run(self):
        self.ss.runPrepared()




#cdata = {'sheet_name': '21', 'number_car': 2323, 'date': '1.12.12', 'period': 'Ночь', 'first_distance': 123, 'last_distance': 321, 'z_index': 123.0, 'cash_bavaria': 321.0, 'terminal': 0, 'viza_discount': 0, 'cash_card': 0, 'znf': 0, 'bonuse': 0, 'yandex_nal': 123.0, 'yandex_bez': 321.0, 'washing': 123.0, 'washing_type': 'Безнал', 'azs': 1234.0, 'azs_type': 'Безнал', 'water': 1234, 'count_yandex': 4321, 'count_bavaria': 1234, 'over_cash': 1234.0}

# tb = Table(GOOGLE_CREDENTIALS_FILE)
# tb.ss.create("asd", "main")
# tb.ss.shareWithAnybodyForWriting()
# tb.ss.sheetId()

# tb._Table__get_row()
# if not tb.is_have_list(cdata['sheet_name']):
#     tb.create_sheets(cdata['sheet_name'])
#     tb.create_struct_for_sheet()

# tb.ss.setSheetByName(cdata['sheet_name'])
# tb.add_items(cdata) 

# tb.run()