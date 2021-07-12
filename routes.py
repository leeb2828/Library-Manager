from flask import render_template, request, redirect, url_for

# this needs a post
def home_route():
    from app import get_all_books, insert_new_book, check_entry
    if request.method == 'POST':
        X1 = request.form['title']
        X2 = request.form.get("author")
        X3 = request.form['genre']
        X4 = request.form['year']
        # check if book entry exists
        already_exists = check_entry(X1, X2)
        if not already_exists:
            # insert new book
            insert_new_book(X1, X2, X3, X4)

    rows = get_all_books()
    return render_template('all_books.html', rows=rows)



def new_book():
    return render_template('new_book.html')


def edit_book(title, author, genre, year):
    if request.method == 'POST':
        from app import modify_book_info
        X1 = request.form['title']
        X2 = request.form['author']
        X3 = request.form['genre']
        X4 = request.form['year']

        items_to_modify = {}
        all_items = {'title': X1, 'author': X2, 'genre': X3, 'year': X4}
        for key, value in all_items.items():
            if value:
                items_to_modify[key] = value
            else:
                items_to_modify[key] = None
        
        modify_book_info(items_to_modify, title, author)
        return redirect(url_for('home_route'))


def delete_book(title, author):
    if request.method == 'POST':
        from app import delete_book 
        delete_book(title, author) 
    return redirect(url_for('home_route'))


def view_book(title, author, genre, year):        
    row = {'title': title, 'author': author, 'genre': genre, 'year': year}
    return render_template('book_detail.html', row=row)
