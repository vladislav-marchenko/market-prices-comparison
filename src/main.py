import json

with open('mrkt_data.json', 'r') as mrkt, \
        open('portals_data.json', 'r') as portals, \
        open('tonnel_data.json', 'r') as tonnel:
    mrkt_data = json.loads(mrkt.read())
    portals_data = json.loads(portals.read())
    tonnel_data = json.loads(tonnel.read())

    for name, mrkt_collection in mrkt_data.items():
        if any(name not in data for data in (tonnel_data, portals_data)):
            continue

        portals_collection = portals_data[name]
        tonnel_collection = tonnel_data[name]

        mrkt_floor = mrkt_collection['floorPriceNanoTons'] / 1000000000
        portals_floor = portals_collection['floor_price']
        tonnel_floor = tonnel_collection['floorPrice']

        mrkt_instant_sell = mrkt_collection['order']
        portals_instant_sell = portals_collection['order']

        mrkt_instant_sell_price = mrkt_instant_sell['priceMaxNanoTONs'] / 1000000000
        portals_instant_sell_price = portals_instant_sell['amount']
        portals_instant_sell_price_without_fee = round(
            portals_instant_sell_price * 0.95, 2)

        mrkt_instant_sell_created_at = mrkt_instant_sell['createdAt']
        portals_instant_sell_created_at = portals_instant_sell['created_at']

        withdraw_fee = deposit_fee = 0.1

        mrkt_to_portals_profit = portals_instant_sell_price_without_fee -\
            mrkt_floor - withdraw_fee
        portals_to_mrkt_profit = mrkt_instant_sell_price - portals_floor -\
            withdraw_fee - deposit_fee
        tonnel_to_mrkt_profit = mrkt_instant_sell_price - tonnel_floor -\
            deposit_fee
        tonnel_to_portals_profit = portals_instant_sell_price_without_fee -\
            tonnel_floor

        is_profit = any(profit > 0 for profit in
                        (mrkt_to_portals_profit,
                         portals_to_mrkt_profit,
                         tonnel_to_mrkt_profit,
                         tonnel_to_portals_profit)
                        )

        if is_profit:
            print(f'''
                🏷️ Name: {mrkt_collection['name']}

                📉Floor Prices:
                    🟡 Mrkt: {mrkt_floor}
                    🟣 Portals: {portals_floor}
                    🟢 Tonnel: {tonnel_floor}

                💰Max Instant Sell:
                    🟡 Mrkt: {mrkt_instant_sell_price}
                    🟣 Portals: {portals_instant_sell_price}

                💰Possible profits:
                    🟡 Mrkt to Portals: {mrkt_to_portals_profit}
                    🟣 Portals to Mrkt: {portals_to_mrkt_profit}
                    🟢 Tonnel to Mrkt: {tonnel_to_mrkt_profit}
                    🟢 Tonnel to Portals: {tonnel_to_portals_profit}

                📅Created At:
                    🟡 Mrkt: {mrkt_instant_sell_created_at}
                    🟣 Portals: {portals_instant_sell_created_at}

                ---------------------------------------------------------------
                ''')
