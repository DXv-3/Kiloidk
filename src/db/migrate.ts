import { runMigrations } from "@kilocode/app-builder-db";
import { db } from "./index";

runMigrations(db, {}, { migrationsFolder: "./src/db/migrations" });