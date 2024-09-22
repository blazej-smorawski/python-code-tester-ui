/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'pomorski-czarodziej-development';
const collection = 'tasks';
const collection2 = 'editions';
const collection3 = 'blog';

// Create a new database.
use(database);

// Create a new collection.
db.createCollection(collection);
db.createCollection(collection2);
db.createCollection(collection3);
