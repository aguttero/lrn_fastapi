from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional [int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]



@app.get("/")
def pol():
    return {"message": "pol ok!"}


@app.get("/books")
async def read_all_books():
    return BOOKS

# PATH parameter
@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

# QUERY parameter
@app.get ("/books/")
async def filter_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
           books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/")
async def filter_by_published_year(book_year: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_year:
            books_to_return.append(book)
    return books_to_return


# -- ID Auto increment:
def find_book_id (book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    # refactor in one line:
    # book.id = 1 if len (BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # new_book = Book(**book_request.dict()) # Pydantic V1
    new_book = Book(**book_request.model_dump()) # Pydantic V2
    # BOOKS.append(book_request)
    BOOKS.append(find_book_id(new_book))
    print(type(book_request))
    print(type(new_book))
    return f"book_req= {type(book_request)}, new_book= {type(new_book)}"

@app.put("/books/update_book")
async def update_book(book: BookRequest): # en el body viene instancia de BookRequest
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
