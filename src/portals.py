import os
import requests
from datetime import datetime

from pydantic import BaseModel, TypeAdapter, HttpUrl
from typing import List, Optional, Dict


class PortalsTopOrder(BaseModel):
    id: str
    collection_id: str
    amount: float
    max_nfts: int
    current_nfts: int
    created_at: datetime
    updated_at: Optional[datetime]
    expires_at: Optional[datetime]


portals_top_order_adapter = TypeAdapter(PortalsTopOrder)


class PortalsCollection(BaseModel):
    id: str
    name: str
    short_name: str
    photo_url: HttpUrl
    day_volume: float
    volume: float
    floor_price: float
    supply: int
    is_favorite: bool
    order: Optional[PortalsTopOrder] = None


class PortalsCollectionsResponse(BaseModel):
    collections: List[PortalsCollection]


portals_collections_adapter = TypeAdapter(PortalsCollectionsResponse)
portals_result_adapter = TypeAdapter(Dict[str, PortalsCollection])


PORTALS_TMA = os.getenv('TMA')
PORTALS_BASE_URL = 'https://portals-market.com/api'
headers = {'Authorization': PORTALS_TMA}


def get_portals_collections() -> PortalsCollectionsResponse:
    url = f'{PORTALS_BASE_URL}/collections?limit=9999'

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return portals_collections_adapter.validate_python(response.json()).collections


def get_portals_collection_top_order(id: str) -> PortalsTopOrder | None:
    url = f'{PORTALS_BASE_URL}/collection-offers/{id}/top'

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    data = response.json()

    if len(data):
        return portals_top_order_adapter.validate_python(data[0])


def get_portals_data() -> Dict[str, PortalsCollection]:
    collections = get_portals_collections()

    result = {}
    for collection in collections:
        top_order = get_portals_collection_top_order(collection.id)
        collection.order = top_order

        result[collection.short_name] = collection

    return result


if __name__ == '__main__':
    data = get_portals_data()
    json_data = portals_result_adapter.dump_json(data).decode('utf-8')
    print(json_data)
