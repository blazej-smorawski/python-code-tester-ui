CREATE TABLE IF NOT EXISTS "group" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS "tasks" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar NOT NULL,
	"input" varchar NOT NULL,
	"expectedOutput" varchar NOT NULL,
	"group_id" integer NOT NULL,
    CONSTRAINT "fk_tasks_group"
        FOREIGN KEY ("group_id")
        REFERENCES "group" ("id")
);
