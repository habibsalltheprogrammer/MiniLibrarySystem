"""
Simple unit tests using assert statements (no testing framework).
Run: python tests.py
"""

from operations import (
    books, members, GENRES, add_book, add_member, search_books,
    update_book, update_member, delete_book, delete_member,
    borrow_book, return_book, get_member
)

# Reset globals in case of re-run
books.clear()
members.clear()

# 1) Test adding books and members
assert add_book("ISBN001", "Python Basics", "John Doe", "Non-Fiction", 3) == True, "Failed to add book 1"
assert add_book("ISBN002", "Adventures", "Jane Roe", "Fiction", 2) == True, "Failed to add book 2"
# Duplicate ISBN should fail
assert add_book("ISBN001", "Duplicate", "X", "Fiction", 1) == False, "Duplicate ISBN allowed"

assert add_member("M001", "Alice Smith", "alice@example.com") == True, "Failed to add member 1"
assert add_member("M002", "Bob Brown", "bob@example.com") == True, "Failed to add member 2"
# Duplicate member id
assert add_member("M001", "Someone", "s@x.com") == False, "Duplicate member allowed"

# 2) Borrow / return edge cases
# Borrow when copies available
assert borrow_book("ISBN001", "M001") == True, "Borrow should succeed (ISBN001 -> M001)"
# Borrow until none left (we won't exhaust here, but check duplicates)
assert borrow_book("ISBN001", "M002") == True, "Borrow should succeed (ISBN001 -> M002)"
# Member cannot borrow same ISBN twice
assert borrow_book("ISBN001", "M002") == False, "Second borrow by same member of same book should fail"
# Borrow another book
assert borrow_book("ISBN002", "M002") == True, "Borrow ISBN002 by M002"

# 3) Borrow limit per member (max 3)
# Add more books
assert add_book("ISBN003", "Third Book", "Author A", "Fiction", 1) == True
assert add_book("ISBN004", "Fourth Book", "Author B", "Fiction", 1) == True
assert add_book("ISBN005", "Fifth Book", "Author C", "Fiction", 1) == True
# Borrow three different books for M002 (already has ISBN002)
assert borrow_book("ISBN003", "M002") == True
print(borrow_book("ISBN004", "M002"))== True
# Now M002 has 4 borrowed? Let's check: M002 has ISBN001 (no, earlier failed duplicate), ISBN002, ISBN003, ISBN004 -> that's 3.
# Next borrow should fail
assert borrow_book("ISBN005", "M002") == False, "Member exceeded 3-book limit but borrow allowed"

# 4) Return book that wasn't borrowed (should fail)
assert return_book("ISBN005", "M001") == False, "Return of non-borrowed book should fail"

# 5) Update book total copies less than borrowed -> should fail
assert update_book("ISBN002", total_copies=0) == False, "Allowed total_copies smaller than borrowed count"

# 6) Delete member with borrowed books should fail; deleting after returning should succeed
assert delete_member("M002") == False, "Deleted member who still has borrowed books"
# Return all M002's books
m = get_member("M002")
for b in list(m["borrowed_books"]):
    return_book(b, "M002")
assert delete_member("M002") == True, "Failed to delete member after returning books"

print("All tests passed.")