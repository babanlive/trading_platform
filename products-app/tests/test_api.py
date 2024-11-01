import pytest
from httpx import AsyncClient


BASE_URL = '/api/v1'


@pytest.mark.asyncio
async def test_create_category(ac: AsyncClient):
    response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Fruits'})

    assert response.status_code == 200
    assert response.json()['name'] == 'Fruits'


@pytest.mark.asyncio
async def test_get_categories(ac: AsyncClient):
    response = await ac.get(f'{BASE_URL}/categories')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
