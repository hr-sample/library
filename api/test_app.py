import uuid
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def app_client(monkeypatch) -> TestClient:
    """Creates api_client for API testing purposes"""
    monkeypatch.setenv("DB_URI", f"sqlite:///test_{uuid.uuid4()}.db")
    from library_app import app

    return TestClient(app)


def test_add_book(app_client):
    """Test adding a book."""
    response = app_client.post(
        "/v1/add_book/",
        json={
            "serial_number": "123456",
            "title": "Book Title",
            "author": "Author Name",
            "is_taken": False,
            "borrower": None,
            "borrowed_at": None,
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_add_book_negative(app_client):
    """Test adding a book with missing fields."""
    response = app_client.post(
        "/v1/add_book/",
        json={
            "serial_number": "12345",
            "title": "Book Title",
            "author": "Author Name",
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_book_with_wrong_id(app_client):
    """Test adding a book with wrong id."""
    response = app_client.post(
        "/v1/add_book/",
        json={
            "serial_number": 1234,
            "title": "Book Title",
            "author": "Author Name",
            "is_taken": False,
            "borrower": None,
            "borrowed_at": None,
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_remove_book(app_client):
    """Test removing a book."""
    response = app_client.post(
        "/v1/add_book/",
        json={
            "serial_number": "123457",
            "title": "Book Title",
            "author": "Author Name",
            "is_taken": False,
            "borrower": None,
            "borrowed_at": None,
        },
    )
    response = app_client.delete("/v1/remove_book/123457")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Book removed successfully."


def test_remove_non_existing_book(app_client):
    """Test removing a non-existing book."""
    response = app_client.delete("/v1/remove_book/129457")
    assert response.status_code == 404
    assert (
        response.json()["detail"]["message"]
        == "Book with serial number 129457 not found!"
    )


def test_get_books(app_client):
    """Test getting books."""
    response = app_client.get("/v1/get_books/")
    assert response.status_code == HTTPStatus.OK
    books = response.json()
    assert isinstance(books, list)
    assert len(books) >= 0


def test_update_book(app_client):
    """Test updating a book."""
    response = app_client.post(
        "/v1/add_book/",
        json={
            "serial_number": "123458",
            "title": "Book Title",
            "author": "Author Name",
            "is_taken": False,
            "borrower": None,
            "borrowed_at": None,
        },
    )
    assert response.status_code == HTTPStatus.OK

    response = app_client.put(
        "/v1/update_book/123458",
        json={
            "is_taken": True,
            "borrower": 654321,
            "borrowed_at": "2025-01-01T11:30:00",
        },
    )

    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert result["message"] == "Book updated successfully."