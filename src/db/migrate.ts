import { runMigrations } from "@kilocode/app-builder-db";
import { getDb } from "./index";

async function main() {
  const db = await getDb();
  if (!db) {
    throw new Error("Database not configured");
  }
  await runMigrations(db as any, {}, { migrationsFolder: "./src/db/migrations" });
}

main();