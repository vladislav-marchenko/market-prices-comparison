import os
import requests
from urllib.parse import quote
from datetime import datetime

from pydantic import BaseModel, TypeAdapter
from typing import Optional, List


class MrktTopOrder(BaseModel):
    id: str
    collectionName: str
    modelName: Optional[str]
    backdropName: Optional[str]
    symbolName: Optional[str]
    priceMinNanoTONs: int
    priceMaxNanoTONs: int
    completedQuantity: int
    totalQuantity: int
    createdAt: datetime
    endAt: datetime
    isNotificationSeen: bool


mrkt_top_order_adapter = TypeAdapter(MrktTopOrder)


class MrktCollection(BaseModel):
    name: str
    modelStickerThumbnailKey: str
    floorPriceNanoTons: int
    previousDayFloorPriceNanoTons: int
    volume: Optional[int]
    isNew: bool
    order: Optional[MrktTopOrder] = None


mrkt_collections_adapter = TypeAdapter(List[MrktCollection])


MRKT_TMA = os.getenv('MRKT_TMA')
MRKT_BASE_URL = 'https://api.tgmrkt.io/api/v1'


def get_mrkt_token():
    url = f'{MRKT_BASE_URL}/auth'
    data = {
        "data": MRKT_TMA,
        "photo": "https://t.me/i/userpic/320/dC8A7k3lxiZDaFVGhU16_enWClpxh5nJSlGTuCy3UAE.svg",
        "appId": None
    }

    response = requests.post(url=url, json=data)
    response.raise_for_status()

    return response.json()['token']


def get_mrkt_collections(auth_token: str) -> List[MrktCollection]:
    url = f'{MRKT_BASE_URL}/gifts/collections'
    headers = {'Authorization': auth_token}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return mrkt_collections_adapter.validate_python(response.json())


def get_mrkt_collection_top_order(name: str, auth_token: str) -> MrktTopOrder | None:
    url = f'{MRKT_BASE_URL}/orders/top?collectionName={quote(name)}'
    headers = {'Authorization': auth_token}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    data = response.json()

    if len(data):
        return mrkt_top_order_adapter.validate_python(data[0])


def get_mrkt_data() -> List[MrktCollection]:
    auth_token = get_mrkt_token()
    collections = get_mrkt_collections(auth_token)

    for collection in collections:
        top_order = get_mrkt_collection_top_order(collection.name, auth_token)
        collection.order = top_order

    return collections


if __name__ == '__main__':
    data = get_mrkt_data()
    json_data = mrkt_collections_adapter.dump_json(data).decode('utf-8')
    print(json_data)
