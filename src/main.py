import json

with open('mrkt_data.json', 'r') as mrkt, \
        open('portals_data.json', 'r') as portals:
    mrkt_data = json.loads(mrkt.read())
    portals_data = json.loads(portals.read())

    for name, mrkt_collection in mrkt_data.items():
        if name not in portals_data:
            continue

        portals_collection = portals_data[name]

        mrkt_floor = mrkt_collection['floorPriceNanoTons'] / 1000000000
        portals_floor = portals_collection['floor_price']

        mrkt_instant_sell = mrkt_collection['order']
        portals_instant_sell = portals_collection['order']

        mrkt_instant_sell_price = mrkt_instant_sell['priceMaxNanoTONs'] / 1000000000
        portals_instant_sell_price = portals_instant_sell['amount']

        mrkt_instant_sell_created_at = mrkt_instant_sell['createdAt']
        portals_instant_sell_created_at = portals_instant_sell['created_at']

        print(f'''
        🏷️ Name: {mrkt_collection['name']}

        📉Floor Prices:
            🟡 Mrkt: {mrkt_floor}
            🟣 Portals: {portals_floor}

        💰Max Instant Sell:
            🟡 Mrkt: {mrkt_instant_sell_price}
            🟣 Portals: {portals_instant_sell_price}

        📅Created At:
            🟡 Mrkt: {mrkt_instant_sell_created_at}
            🟣 Portals: {portals_instant_sell_created_at}

        ---------------------------------------------------------------
        ''')
