import pandas as pd
import datetime


class FileManager:

    def to_excel(self, data_to_upload):
        date_time = datetime.datetime.now().strftime('%d-%m-%y-%H-%M')
        file_name = f'ozon {date_time}.xlsx'
        pd.DataFrame(data=data_to_upload).to_excel(file_name, index=False)
        print('Результат выгружен в эксель и находится в папке со скриптом.')


