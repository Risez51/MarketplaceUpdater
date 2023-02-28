from ozon.ozon_handler import OzonHandler
from kalibron_handler import KalibronHandler
from ozon.ozon_product_handler import ProductHandler
from file_manager import FileManager


class OzonWorker:
    def __init__(self):
        # Получение списка продуктов из xml калиброна
        self.__kalibron_products = KalibronHandler().get_products_ozon()

    def update_price(self):
        # Получение list[json] с ozon.ru - отчет по текущим ценам на площадке
        ozon_price_items = OzonHandler().get_info_price_items()
        # price_items -> convert to list[Product]
        ozon_products = ProductHandler().get_products_from_price_items(ozon_price_items)
        # Merge products from kalibron with ozon products -> list[Product]
        merged_products = ProductHandler().get_merged_products_for_price(ozon_products, self.__kalibron_products)
        # Создает список словарей для отправки запроса на обновление цены
        prepared_products_lists: list[list[dict]] = ProductHandler().get_prepared_products_for_price_update(
            merged_products)
        #print(f'Количество запросов на обновление {len(prepared_products_lists)} шт.')
        # FileManager().to_excel(prepared_products_lists[0])
        # Реализация функции - для отправки данных на ozon.ru !!! РАСКОМЕНТИРОВАТЬ !!!
        OzonHandler().update_price(prepared_products_lists)

    def update_stock(self):
        ozon_stock_items = OzonHandler().get_info_stock_items()
        ozon_products = ProductHandler().get_products_from_stock_items(ozon_stock_items)
        merged_products = ProductHandler().get_merged_products_for_stock(ozon_products, self.__kalibron_products)
        prepared_products_lists = ProductHandler().get_prepared_products_for_stock_update(merged_products)
        # print(f'Количество запросов на обновление {len(prepared_products_lists)} шт.')
        FileManager().to_excel(prepared_products_lists[0])
        # Отправка данных на ozon.ru
        OzonHandler().update_stock(prepared_products_lists)

    def get_stock_items(self):
        stock = OzonHandler().get_info_stock_items()
        FileManager().to_excel(stock[0]['result']['items'])
        for item in stock[0]['result']['items']:
            print(item)

