import openpyxl as pyxl

import app.utils as u


async def find_user(id):
    wb = pyxl.load_workbook('example.xlsx')
    sheet = wb["data"]

    i = 1
    while sheet[f"A{i}"].value != None:
        if sheet[f"A{i}"].value==id:
            wb.close()
            return True
        i+=1
    wb.close()
    return False


async def register_user(name, email, number, id):
    await u.valid_email(email)
    e = await find_user(id)
    if not e:
        wb = pyxl.load_workbook('example.xlsx')
        sheet = wb["data"]
        sheet.append([id, name, email, number])
        wb.save('example.xlsx')
        wb.close()
    else:
        print("Такой пользователь уже существует")
