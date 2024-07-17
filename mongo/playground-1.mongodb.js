// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('pomorski-czarodziej-development');

// Create a new document in the collection.
db.getCollection('editions').insertOne({
    "name": "Python Testing",
    "public": true,
    "active": true,
    "start": new Date("2023-05-18T16:00:00Z"),
    "end": new Date("2030-05-18T16:00:00Z")
});
