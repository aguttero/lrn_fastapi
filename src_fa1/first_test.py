from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/pol")
def pol():
    return {"message": "hello you! :-)"}

@app.get("/book/{dyn_param}")
async def read_parameter_sample(dyn_param):
    return {'dynamic_param': dyn_param}

# --- Path PArameter
@app.get("/books/{book_title}")
async def read_single_book(book_title:str):
    for book in BOOKS:
        if book.get('title').lower() == book_title.lower():
        # if book.get('title').casefold() == book_tile.casefold():
            return book

# --- Add a Query Parameter
@app.get("/books/")
async def read_category_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').lower() == category.lower():
            books_to_return.append(book)
    return books_to_return

# --- Add query parameter to path parameter
@app.get("/books/{book_author}/")
async def read_author_category_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').lower() == book_author.lower() and book.get('category').lower() == category.lower():
            books_to_return.append(book)
        # if book.get('title').casefold() == book_tile.casefold():
    return books_to_return

@app.get("/all_books")
async def read_all_books():
    return BOOKS
