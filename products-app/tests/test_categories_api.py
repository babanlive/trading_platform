from httpx import AsyncClient


BASE_URL = '/api/v1'


async def test_create_category(ac: AsyncClient):
    response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Fruits'})

    assert response.status_code == 200
    assert response.json()['name'] == 'Fruits'


async def test_get_categories(ac: AsyncClient):
    response = await ac.get(f'{BASE_URL}/categories')

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_update_category(ac: AsyncClient):
    response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Vegetables'})
    category_id = response.json()['id']
    updated_data = {'name': 'Fresh Vegetables'}
    response = await ac.put(f'{BASE_URL}/categories/{category_id}', json=updated_data)

    assert response.status_code == 200
    assert response.json()['name'] == updated_data['name']


async def test_delete_category(ac: AsyncClient):

    response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Phones'})
    assert response.status_code == 200
    category_id = response.json()['id']

    response = await ac.delete(f'{BASE_URL}/categories/{category_id}')
    assert response.status_code == 200
