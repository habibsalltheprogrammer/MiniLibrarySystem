"""
demo.py - sequential demo of library operations (non-interactive).
Run: python demo.py
"""

from operations import (
    books, members, GENRES, add_book, add_member, search_books,
    update_book, update_member, delete_book, delete_member,
    borrow_book, return_book, get_book, get_member
)
import pprint
pp = pprint.PrettyPrinter(indent=2).pprint
import time

def print_state(stage):
    print("\n" + "="*10 + f" {stage} " + "="*10)
    print("Books:")
    pp(books)
    print("Members:")
    pp(members)
    print("="*40 + "\n")


def main():
    print("GENRES available:", GENRES)

    # Initialize with at least 5 books and 3 members
    add_book("B001", "Python Basics", "John Doe", "Non-Fiction", 3)
    add_book("B002", "Data Structures", "Jane Roe", "Non-Fiction", 2)
    add_book("B003", "Space Odyssey", "Arthur C", "Sci-Fi", 1)
    # Attempt to add invalid genre (will fail) to show validation
    added = add_book("B004", "Love in Py", "Rom Com", "Romance", 2)
    print("Attempted to add B004 with genre 'Romance' ->", added)
    # Add correctly
    add_book("B004", "Love in Py", "Rom Com", "Fiction", 2)
    add_book("B005", "History of Time", "S. Hawking", "History", 1)

    add_member("M001", "Alice Smith", "alice@example.com")
    add_member("M002", "Bob Brown", "bob@example.com")
    add_member("M003", "Carol King", "carol@example.com")

    print_state("Initial data")

    # Search by title (partial)
    print("Search results for 'python' by title:")
    pp(search_books("python", by="title"))

    # Update a book
    print("Update B002 total_copies -> 4")
    update_book("B002", total_copies=4)
    print_state("After updating B002")

    # Member M001 borrows B001
    print("M001 borrows B001:", borrow_book("B001", "M001"))
    time.sleep(0.3)
    print("M001 borrows B003:", borrow_book("B003", "M001"))
    time.sleep(0.3)
    print_state("After M001 borrows two books")

    # Attempt to borrow unavailable book
    print("M002 attempts to borrow B003 (should fail, only 1 copy):", borrow_book("B003", "M002"))

    # Return a book
    print("M001 returns B003:", return_book("B003", "M001"))
    print_state("After M001 returns B003")

    # Delete book that still has borrowed copies (should fail)
    print("Attempt delete B001 (should fail if copies borrowed):", delete_book("B001"))

    # Return B001 then delete
    print("M001 returns B001:", return_book("B001", "M001"))
    print("Now delete B001 (should succeed):", delete_book("B001"))
    print_state("After deleting B001")

    # Update member details
    print("Update M003 email/name:", update_member("M003", name="Caroline King", email="caroline@example.com"))
    print_state("Final state")

if __name__ == "__main__":
    main()
