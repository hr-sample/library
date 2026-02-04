import os

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base, Book, BookUpdate, DbBook

DB_URI = os.environ["DB_URI"]

engine = create_engine(DB_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

app = FastAPI()


@app.post("/v1/add_book/")
async def add_book(book: Book) -> dict:
    session = Session(bind=engine)
    book = DbBook(
        serial_number=book.serial_number,
        title=book.title,
        author=book.author,
        borrower=book.borrower,
        is_taken=book.is_taken,
    )
    session.add(book)
    session.commit()
    return {"message": "Book added successfully."}


@app.get("/v1/get_books/")
async def get_books() -> list[dict]:
    session = Session(bind=engine)
    books = session.query(DbBook).all()
    return [book.as_dict() for book in books]


@app.delete("/v1/remove_book/{serial_number}")
async def remove_book(serial_number: int) -> dict:
    session = Session(bind=engine)
    book_to_remove = (
        session.query(DbBook).filter_by(serial_number=serial_number).first()
    )
    if book_to_remove:
        session.delete(book_to_remove)
        session.commit()
        return {"message": "Book removed successfully."}
    else:
        raise HTTPException(
            status_code=404,
            detail={"message": f"Book with serial number {serial_number} not found!"},
        )


@app.put("/v1/update_book/{serial_number}")
async def update_book(book: BookUpdate, serial_number: int) -> dict:
    """Update the book with serial number."""

    session = Session(bind=engine)
    book_to_update = (
        session.query(DbBook).filter_by(serial_number=serial_number).first()
    )

    if book_to_update:
        if book.title is not None:
            book_to_update.title = book.title

        if book.author is not None:
            book_to_update.author = book.author

        if book.is_taken is not None:
            book_to_update.borrower = book.borrower
            book_to_update.is_taken = book.is_taken
            book_to_update.borrowed_at = book.borrowed_at

        session.commit()

        return {"message": "Book updated successfully."}
    else:
        raise HTTPException(
            status_code=404,
            detail={"message": f"Book with serial number {serial_number} not found!"},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)
