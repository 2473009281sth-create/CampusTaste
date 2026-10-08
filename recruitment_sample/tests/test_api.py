from unittest.mock import Mock

from fastapi.testclient import TestClient

from app import main


def test_endpoint_returns_and_caches_dish(redis_fake, monkeypatch):
    source = Mock(wraps=main.load_demo_dish)
    monkeypatch.setattr(main, 'load_demo_dish', source)
    with TestClient(main.app) as client:
        for _ in range(2):
            response = client.get('/dishes/demo-dish')
            assert response.status_code == 200
            assert response.json() == {'id': 'demo-dish', 'name': '示例菜品'}
    source.assert_called_once_with('demo-dish')


def test_missing_dish_returns_404_and_is_negative_cached(redis_fake, monkeypatch):
    source = Mock(wraps=main.load_demo_dish)
    monkeypatch.setattr(main, 'load_demo_dish', source)
    with TestClient(main.app) as client:
        for _ in range(2):
            assert client.get('/dishes/missing').status_code == 404
    source.assert_called_once_with('missing')


def test_endpoint_rate_limit(redis_fake):
    with TestClient(main.app) as client:
        for _ in range(10):
            assert client.get('/dishes/demo-dish').status_code == 200
        response = client.get('/dishes/demo-dish')
    assert response.status_code == 429
    assert response.headers['Retry-After'] == '60'


def test_endpoint_redis_unavailable(redis_fake):
    redis_fake.fail.add('eval')
    with TestClient(main.app) as client:
        assert client.get('/dishes/demo-dish').status_code == 503
