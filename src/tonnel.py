import json

with open('tonnel_stats.txt', 'r') as file:
    data = json.loads(file.read())['data']

    result = {}
    for model_name, values in data.items():
        collection_short_name = model_name.replace(
            ' ', '').split('_')[0].lower()

        model_floor_price = values['floorPrice'] * 1.06  # Including fee
        current_collection_data = result.get(collection_short_name, {})
        current_collection_floor_price = current_collection_data.get(
            'floorPrice', 10 ** 10)
        model_amount = values['howMany']

        result[collection_short_name] = {
            'floorPrice': min(model_floor_price, current_collection_floor_price),
            'howMany': current_collection_data.get('howMany', 0) + model_amount
        }

    if __name__ == '__main__':
        print(json.dumps(result))
