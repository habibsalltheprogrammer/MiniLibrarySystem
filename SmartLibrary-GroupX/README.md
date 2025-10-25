# SmartLibrary (Mini Library Management System)

This is a console-based Mini Library Management System implemented in Python using only functions, lists, dictionaries and tuples (no OOP).

## Files
- `operations.py` : Core functions implementing CRUD, borrow/return, and global data structures.
- `demo.py` : Sequential demo script that initializes the system and performs operations (run to see example flows).
- `tests.py` : Simple unit tests using `assert` statements.
- `DesignRationale.txt` : Design rationale content to paste into a Word/LibreOffice document and export as PDF.
- `UML_GUIDE.txt` : Instructions to hand-draw the UML diagram and include it as `UML.png` or `UML.pdf`.
- `submission.txt` : Submission metadata template.

## Requirements
- Python 3.8+ (tested with Python 3.10/3.12)
- No external libraries required.

## How to run
1. Open the folder `SmartLibrary-GroupX` in PyCharm (File -> Open).
2. Run the demo:
```bash
python demo.py
```
3. Run the tests:
```bash
python tests.py
```

## Notes
- GENRES are defined in `operations.py` (immutable tuple).
- Books stored in `books` global dictionary keyed by ISBN.
- Members stored in `members` global list.
- The system does not persist data; it runs in-memory per session.
