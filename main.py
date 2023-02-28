from wildberries.wb_worker import WbWorker
from ozon.ozon_worker import OzonWorker
from ozon.ozon_product import Product
import sys


def main():
    ozon()

def wb():
    try:
        wb_worker = WbWorker()
        wb_worker.update_price()
        # wb_worker.update_stock()
        # wb_worker.to_excel()
    except Exception as e:
        print('Произошла ошибка, обратитесь к разработчику')
        print(e)


def ozon():
    try:
        ozon_worker = OzonWorker()
        ozon_worker.update_stock()
        ozon_worker.update_price()
    except Exception as e:
        print('Произошла ошибка, обратитесь к разработчику')
        print(e)


if __name__ == '__main__':
    main()
