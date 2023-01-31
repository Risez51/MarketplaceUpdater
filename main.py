from Ozon.ozon_worker import OzonWorker


def main():
    worker = OzonWorker()
    worker.update_price()
   # worker.update_stock()


if __name__ == '__main__':
    main()
