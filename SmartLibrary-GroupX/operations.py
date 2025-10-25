"""
operations.py

Mini Library Management System (procedural, no OOP).
Global data structures: books (dict), members (list), GENRES (tuple).

Each book stored as:
    books[isbn] = {
        "title": str,
        "author": str,
        "genre": str,
        "total_copies": int,      # original total number of copies
        "available_copies": int   # current available copies for borrowing
    }

Each member is a dict inside the members list:
    {
        "member_id": str,
        "name": str,
        "email": str,
        "borrowed_books": [isbn, ...]
    }
"""

# Global data storage
books = {}
members = []
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Biography", "History", "Romance")

# -----------------------
# Create operations
# -----------------------
def add_book(isbn, title, author, genre, total_copies):
    """
    Add a new book to the books dictionary.
    Returns True if successful, False if ISBN exists or genre invalid or bad total_copies.
    """
    if not isinstance(isbn, str) or not isbn.strip():
        return False
    if isbn in books:
        # ISBN must be unique
        return False
    if genre not in GENRES:
        return False
    try:
        total = int(total_copies)
    except (ValueError, TypeError):
        return False
    if total < 1:
        return False

    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total,         # original total
        "available_copies": total     # initially all copies available
    }
    return True


def add_member(member_id, name, email):
    """
    Add a new member to the members list.
    Returns True if successful, False if member_id already exists or invalid params.
    """
    if not isinstance(member_id, str) or not member_id.strip():
        return False
    if any(m["member_id"] == member_id for m in members):
        return False
    member = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []
    }
    members.append(member)
    return True

# -----------------------
# Read operations
# -----------------------
def search_books(query, by="title"):
    """
    Search books by title or author, case-insensitive partial matches.
    Returns a list of matching dictionaries. Each dict includes 'isbn' key as well.
    """
    results = []
    q = str(query).strip().lower()
    if not q:
        return results
    if by not in ("title", "author"):
        by = "title"
    for isbn, info in books.items():
        if q in info.get(by, "").lower():
            # Return a copy with isbn included to help caller
            entry = info.copy()
            entry["isbn"] = isbn
            results.append(entry)
    return results

# -----------------------
# Update operations
# -----------------------
def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """
    Update specified fields of a book if it exists.
    - genre must be in GENRES if provided.
    - total_copies must be >= number of currently borrowed copies.
    Returns True if successful, False otherwise.
    """
    if isbn not in books:
        return False
    book = books[isbn]

    if genre is not None:
        if genre not in GENRES:
            return False
        book["genre"] = genre

    if title is not None:
        book["title"] = title

    if author is not None:
        book["author"] = author

    if total_copies is not None:
        try:
            new_total = int(total_copies)
        except (ValueError, TypeError):
            return False
        borrowed_count = book["total_copies"] - book["available_copies"]
        if new_total < borrowed_count or new_total < 0:
            # Can't set total to less than already borrowed copies
            return False
        # adjust available copies proportionally: new_available = new_total - borrowed_count
        book["total_copies"] = new_total
        book["available_copies"] = new_total - borrowed_count

    return True


def update_member(member_id, name=None, email=None):
    """
    Update specified fields of a member if they exist.
    Returns True if successful, False otherwise.
    """
    for m in members:
        if m["member_id"] == member_id:
            if name is not None:
                m["name"] = name
            if email is not None:
                m["email"] = email
            return True
    return False

# -----------------------
# Delete operations
# -----------------------
def delete_book(isbn):
    """
    Remove a book if it exists and has no borrowed copies.
    We ensure available_copies == total_copies (i.e., nobody borrowed it).
    Returns True if deleted, False otherwise.
    """
    if isbn not in books:
        return False
    book = books[isbn]
    if book["available_copies"] != book["total_copies"]:
        # some copies are borrowed
        return False
    del books[isbn]
    return True


def delete_member(member_id):
    """
    Remove a member if they exist and have no borrowed books.
    Returns True if deleted, False otherwise.
    """
    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            if m["borrowed_books"]:
                return False
            members.pop(i)
            return True
    return False

# -----------------------
# Borrow / Return
# -----------------------
def borrow_book(isbn, member_id):
    """
    Member borrows a book:
    - Book must exist and available_copies > 0.
    - Member must exist and have fewer than 3 borrowed books.
    If valid: decrement available_copies and add ISBN to member's borrowed_books.
    Returns True if successful, False otherwise.
    """
    if isbn not in books:
        return False
    book = books[isbn]
    if book["available_copies"] <= 0:
        return False

    member = next((m for m in members if m["member_id"] == member_id), None)
    if member is None:
        return False
    if len(member["borrowed_books"]) >= 3:
        return False
    if isbn in member["borrowed_books"]:
        # Avoid duplicate borrow
        return False

    member["borrowed_books"].append(isbn)
    book["available_copies"] -= 1
    return True


def return_book(isbn, member_id):
    """
    Member returns a book:
    - Book must exist and be in the member's borrowed_books.
    If valid: increment available_copies and remove the isbn from borrowed_books.
    Returns True if successful, False otherwise.
    """
    if isbn not in books:
        return False
    book = books[isbn]
    member = next((m for m in members if m["member_id"] == member_id), None)
    if member is None:
        return False
    if isbn not in member["borrowed_books"]:
        return False

    member["borrowed_books"].remove(isbn)
    # Ensure we don't exceed total_copies
    if book["available_copies"] < book["total_copies"]:
        book["available_copies"] += 1
    else:
        # This should not usually happen, but protect invariants
        book["available_copies"] = book["total_copies"]
    return True

# -----------------------
# Utility / Debug helpers
# -----------------------
def get_book(isbn):
    """Return a copy of book dict with isbn included or None if not found."""
    if isbn not in books:
        return None
    b = books[isbn].copy()
    b["isbn"] = isbn
    return b


def get_member(member_id):
    """Return the member dict or None if not found."""
    return next((m for m in members if m["member_id"] == member_id), None)
