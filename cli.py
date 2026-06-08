import argparse

from bot.client import get_client
from bot.orders import OrderManager
from bot.validators import validate_order
import bot.logging_config


def main():

    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot"
    )

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    validate_order(
        args.symbol,
        args.side,
        args.type,
        args.quantity,
        args.price
    )

    client = get_client()

    manager = OrderManager(client)

    if args.type == "MARKET":

        response = manager.place_market_order(
            args.symbol,
            args.side,
            args.quantity
        )

    else:

        response = manager.place_limit_order(
            args.symbol,
            args.side,
            args.quantity,
            args.price
        )

    print("\n===== ORDER RESPONSE =====")

    print("Order ID :", response.get("orderId"))
    print("Status   :", response.get("status"))
    print("Executed :", response.get("executedQty"))
    print("Avg Price:", response.get("avgPrice"))
    print("Side     :", response.get("side"))
    print("Type     :", response.get("type"))


if __name__ == "__main__":
    main()