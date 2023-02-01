import time

import requests
import json
import math

import api_config


class OzonHandler:

    def get_info_price_items(self) -> list:
        items = self.__get_items_info(api_config.OZON_URL_PRICES_INFO)
        return items

    def get_info_stock_items(self) -> list:
        items = self.__get_items_info(api_config.OZON_URL_STOCK_QUANTITY_INFO)
        return items

    def __get_items_info(self, url) -> list:
        items = []
        first_report = self.__send_info_request(url)
        items.append(first_report)
        product_count = first_report['result']['total']
        request_count = math.ceil(product_count / api_config.OZON_INCOMING_LIMIT)
        if request_count > 1:
            last_id = first_report['result']['last_id']
            for i in range(request_count-1):
                report = self.__send_info_request(url, last_id)
                last_id = report['result']['last_id']
                items.append(report)
        return items

    @staticmethod
    def __send_info_request(url: str, last_id: str = '') -> dict:
        time.sleep(1)
        data = {
                "filter": {
                    "offer_id": [],
                    "product_id": [],
                    "visibility": "ALL"
                          },
                "last_id": last_id,
                "limit": api_config.OZON_INCOMING_LIMIT
                }
        answer = requests.post(url, json=data, headers=api_config.OZON_HEADERS)
        content = answer.content
        content = json.loads(content.decode('utf-8'))
        return content

    def update_price(self, prepared_products_lists: list):
        for prepared_products_list in prepared_products_lists:
            data = {'prices': prepared_products_list}
            anwswer = self.send_request(api_config.OZON_URL_PRICES_UPDATE, data)
            time.sleep(1)
        print('ozon: цены обновлены')

    def update_stock(self, prepared_products_lists: list):
        for prepared_products_list in prepared_products_lists:
            data = {'stocks': prepared_products_list}
            anwswer = self.send_request(api_config.OZON_URL_STOCK_QUANTITY_UPDATE_V2, data)
            time.sleep(1)
        print('ozon: остатки обновлены')

    @staticmethod
    def send_request(url: str, data: dict):
        answer = requests.post(url, json=data, headers=api_config.OZON_HEADERS)
        content = answer.content
        content = json.loads(content.decode('utf-8'))
        return content
