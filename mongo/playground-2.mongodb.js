// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('pomorski-czarodziej-development');

// Create a new document in the collection.
db.getCollection('tasks').insertOne({
    "name": "Odejmowanie",
    "edition": "Python Testing",
    "initial-code": "haha = int(input())",
    "description" : "Napisz program, który odejmie *dwie* liczby pobrane ze standardowego wejścia funkcją `input()`. Aby przekształcić tekst na liczbę użyj funkcji `int()`",
    "test-cases": [
        {"input": "1\\n2", "output": "-1"},
        {"input": "4\\n4", "output": "0"}
    ]
});
