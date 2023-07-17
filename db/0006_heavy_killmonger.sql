ALTER TABLE "tasks" ADD COLUMN "description" text;
ALTER TABLE "tasks" DROP COLUMN IF EXISTS "input";
ALTER TABLE "tasks" DROP COLUMN IF EXISTS "expectedOutput";