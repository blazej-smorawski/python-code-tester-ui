DO $$ BEGIN
 ALTER TABLE "testcase" ADD CONSTRAINT "testcase_taskId_tasks_id_fk" FOREIGN KEY ("taskId") REFERENCES "tasks"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
