from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

# --- Basic get
@app.get("/pol")
def pol():
    return {"message": "hello you! :-)"}

@app.get("/all_books")
async def read_all_books():
    return BOOKS

# --- dynamic paramenter
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

# --- POST
# requires import Body from fastapi
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    counter = 0
    for book in BOOKS:
        counter +=1
        print (f"{counter} {book}")
    return "ok"

# --- PUT
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range (len(BOOKS)):
        if BOOKS[i].get('title').lower() == updated_book.get('title').lower():
            BOOKS[i] = updated_book
            updated_index = i+1
    counter = 0
    for book in BOOKS:
        counter +=1
        print (f"{counter} {book}")
    print (f"ok update book {updated_index}")
    return f"ok update book {updated_index}"

# --- DELETE
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range (len(BOOKS)):
        if BOOKS[i].get('title').lower() == book_title.lower():
            BOOKS.pop(i)
            deleted_index = i+1
            break
    counter = 0
    for book in BOOKS:
        counter +=1
        print (f"{counter} {book}")
    print (f"ok delete book {deleted_index}")
    return f"ok delete book {deleted_index}"
