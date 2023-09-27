// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('python-konkurs');

// Create a new document in the collection.
// db.getCollection('tasks').insertOne({
//     "name": "Dodawanie",
//     "edition": "Python 2023",
//     "initial-code": "x = int(input())",
//     "description" : "Napisz program, który doda *dwie* liczby pobrane ze standardowego wejścia funkcją `input()`. Aby przekształcić tekst na liczbę użyj funkcji `int()`",
//     "test-cases": [
//         {"input": "1\\n2", "output": "3"},
//         {"input": "3\\n4", "output": "7"}
//     ]
// });

// Create a new document in the collection.
db.getCollection('tasks').insertOne({
    "name": "Odejmowanie",
    "edition": "Python 2023",
    "initial-code": "haha = int(input())",
    "description" : "Napisz program, który odejmie *dwie* liczby pobrane ze standardowego wejścia funkcją `input()`. Aby przekształcić tekst na liczbę użyj funkcji `int()`",
    "test-cases": [
        {"input": "1\\n2", "output": "-1"},
        {"input": "4\\n4", "output": "0"}
    ]
});