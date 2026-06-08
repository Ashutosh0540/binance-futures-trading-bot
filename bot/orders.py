import logging
import time
from binance.exceptions import BinanceAPIException


class OrderManager:

    def __init__(self, client):
        self.client = client

    def place_market_order(self, symbol, side, quantity):

        try:
            logging.info(
                f"MARKET REQUEST => symbol={symbol}, side={side}, quantity={quantity}"
            )

            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

            time.sleep(1)

            final_response = self.client.futures_get_order(
                symbol=symbol,
                orderId=response["orderId"]
            )

            logging.info(
                f"MARKET RESPONSE => {final_response}"
            )

            return final_response

        except BinanceAPIException as e:
            logging.error(f"Binance API Error: {e}")
            raise

        except Exception as e:
            logging.error(f"Unexpected Error: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):

        try:
            logging.info(
                f"LIMIT REQUEST => symbol={symbol}, side={side}, quantity={quantity}, price={price}"
            )

            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

            logging.info(
                f"LIMIT RESPONSE => {response}"
            )

            return response

        except BinanceAPIException as e:
            logging.error(f"Binance API Error: {e}")
            raise

        except Exception as e:
            logging.error(f"Unexpected Error: {e}")
            raise