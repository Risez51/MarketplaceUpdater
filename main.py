from wildberries.wb_worker import WbWorker
from wildberries.wb_handler import WbHandler
import api_config


def main():
    # OZON price and warehouse update
    # try:
    #     worker = OzonWorker()
    #     worker.update_price()
    #     worker.update_stock()
    # except Exception as e:
    #     print('Произошла ошибка, обратитесь к разрабочику')
    #     print(f'Error key: {e}')

    # Список номенклатеры на вб
    # WbWorker().get_products_from_wb()
    wb_worker = WbWorker()
    wb_worker.update_price()
    wb_worker.update_stock()


if __name__ == '__main__':
    main()
