from httpx import AsyncClient


BASE_URL = '/api/v1'

async def test_create_product(ac: AsyncClient):
    category_response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Fruits'})
    category_id = category_response.json()['id']
    product_data = {
        'name': 'Banana',
        'description': 'Price for 1kg bananas',
        'price': 175,
        'image_url': 'http://example_picture.com/banana.png',
        'category_id': category_id,
    }
    response = await ac.post(f'{BASE_URL}/products', json=product_data)
    assert response.status_code == 200
    product = response.json()
    assert product['name'] == product_data['name']
    assert product['price'] == product_data['price']


async def test_get_products(ac: AsyncClient):
    response = await ac.get(f'{BASE_URL}/products')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_update_product(ac: AsyncClient):
    category_response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Vegetables'})
    category_id = category_response.json()['id']

    product_response = await ac.post(
        f'{BASE_URL}/products',
        json={
            'name': 'Tomatos',
            'description': 'Red tomatos',
            'price': 50,
            'image_url': 'http://example_picture.com/tomatos_red.png',
            'category_id': category_id,
        },
    )
    product_id = product_response.json()['id']
    updated_data = {
        'name': 'Tomatos fresh',
        'description': 'Fresh and yellow tomatos',
        'price': 60,
        'image_url': 'http://example_picture.com/tomatos_yellow.png',
        'category_id': category_id,
    }
    response = await ac.put(f'{BASE_URL}/products/{product_id}', json=updated_data)
    assert response.status_code == 200
    assert response.json()['name'] == updated_data['name']
    assert response.json()['price'] == updated_data['price']


async def test_delete_product(ac: AsyncClient):
    category_response = await ac.post(f'{BASE_URL}/categories', json={'name': 'Phones'})
    category_id = category_response.json()['id']

    product_response = await ac.post(
        f'{BASE_URL}/products',
        json={
            'name': 'Huawei P40',
            'description': 'Flagship model',
            'price': 120,
            'image_url': 'http://example_picture.com/huawei_p40.png',
            'category_id': category_id,
        },
    )
    product_id = product_response.json()['id']
    response = await ac.delete(f'{BASE_URL}/products/{product_id}')
    assert response.status_code == 200
