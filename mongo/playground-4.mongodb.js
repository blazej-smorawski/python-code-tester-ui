// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('python-konkurs');

// Update records in the collection where edition is "Python 2023"
db.getCollection('tasks').find({ "edition": "Python 2023" }).forEach(function(task) {
    // Update each task
    if (task["edition"] === "Python 2023") {
        for (var i = 0; i < task["test-cases"].length; i++) {
            // Add "public" key to each test case
            task["test-cases"][i]["public"] = true;
        }
        
        // Update the task in the collection
        db.getCollection('tasks').updateOne(
            { _id: task._id }, // Filter based on the document ID
            { $set: { "test-cases": task["test-cases"] } } // Update the test-cases field
        );
    }
});
