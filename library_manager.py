import json
import os

# store library data
LIBRARY_FILE = "library.json"

# file if it exists
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Display Menu
def display_menu():
    print("\n📚 PERSONAL LIBRARY MANAGER 📚")
    print("1. Add a Book")
    print("2. Remove a Book")
    print("3. Search for a Book")
    print("4. Display All Books")
    print("5. Display Statistics")
    print("6. Exit")

# Add a book
def add_book(library):
    title = input("Enter book title: ").strip().title()
    author = input("Enter author: ").strip().title()
    
    while True:
        try:
            year = int(input("Enter publication year: "))
            break
        except ValueError:
            print("❌ Invalid input! Please enter a valid year.")

    genre = input("Enter genre: ").strip().title()
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

    for book in library:
        if book["Title"] == title and book["Author"] == author:
            print("⚠️ This book already exists in your library.")
            return

    library.append({
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    })
    save_library(library)
    print("✅ Book added successfully!")

# Remove a book
def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip().title()
    for book in library:
        if book["Title"] == title:
            library.remove(book)
            save_library(library)
            print("✅ Book removed successfully!")
            return
    print("❌ Book not found!")

# Search for a book
def search_book(library):
    print("\nSearch by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        keyword = input("Enter book title: ").strip().title()
        results = [book for book in library if keyword in book["Title"]]
    elif choice == "2":
        keyword = input("Enter author name: ").strip().title()
        results = [book for book in library if keyword in book["Author"]]
    else:
        print("❌ Invalid choice!")
        return

    if results:
        print("\n🔍 Matching Books:")
        for idx, book in enumerate(results, start=1):
            status = "✅ Read" if book["Read"] else "❌ Unread"
            print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
    else:
        print("⚠️ No exact matches found.")
        suggestions = [book["Title"] for book in library if keyword in book["Title"] or keyword in book["Author"]]
        if suggestions:
            print("🔎 Did you mean:")
            for title in suggestions:
                print(f"- {title}")

# Display all books
def display_books(library):
    if not library:
        print("📭 Your library is empty!")
        return

    print("\n📖 Your Library:")
    sort_option = input("Sort by (title/author/year): ").strip().lower()
    if sort_option == "author":
        library = sorted(library, key=lambda x: x["Author"])
    elif sort_option == "year":
        library = sorted(library, key=lambda x: x["Year"])
    else:
        library = sorted(library, key=lambda x: x["Title"])

    for idx, book in enumerate(library, start=1):
        status = "✅ Read" if book["Read"] else "❌ Unread"
        print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")

# Display statistics
def display_statistics(library):
    total_books = len(library)
    if total_books == 0:
        print("📭 No books in library!")
        return

    read_books = sum(1 for book in library if book["Read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books) * 100

    genre_count = {}
    for book in library:
        genre_count[book["Genre"]] = genre_count.get(book["Genre"], 0) + 1
    most_common_genre = max(genre_count, key=genre_count.get) if genre_count else "N/A"

    print("\n📊 Library Statistics:")
    print(f"📚 Total books: {total_books}")
    print(f"✅ Books read: {read_books} ({read_percentage:.2f}%)")
    print(f"❌ Books unread: {unread_books}")
    print(f"🏆 Most common genre: {most_common_genre}")

# Main program
def main():
    library = load_library()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library)
            print("📖 Library saved. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1-6.")

if __name__ == "__main__":
    main()