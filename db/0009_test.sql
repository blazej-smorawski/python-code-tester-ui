INSERT INTO "group" ("name")
VALUES ('Python 2023'), ('Python 2024');

INSERT INTO "tasks" ("name", "description", "group_id")
VALUES ('Dodawanie', 'Napisz program, który doda *dwie* liczby pobrane ze standardowego wejścia funkcją `input()`. Aby przekształcić tekst na liczbę użyj funkcji `int()`', 1),
       ('Task 2', 'Expected Output 2', 1),
       ('Task 3', 'Expected Output 3', 2);


INSERT INTO "testcase" ("taskId", "input", "expected")
VALUES (
    (SELECT "id" FROM "tasks" WHERE "name" = 'Dodawanie'),
    '1\n2',
    '3'
);

INSERT INTO "testcase" ("taskId", "input", "expected")
VALUES (
    (SELECT "id" FROM "tasks" WHERE "name" = 'Task 2'),
    '1234',
    '2468'
);

INSERT INTO "testcase" ("taskId", "input", "expected")
VALUES (
    (SELECT "id" FROM "tasks" WHERE "name" = 'Task 3'),
    '12',
    '24'
);