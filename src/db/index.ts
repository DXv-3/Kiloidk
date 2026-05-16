let db: unknown = null;

export async function getDb(): Promise<unknown> {
  if (db) return db;
  if (!process.env.DB_URL) return null;
  
  try {
    const { createDatabase } = await import("@kilocode/app-builder-db");
    const schema = await import("./schema");
    db = createDatabase(schema);
  } catch {
    console.warn("Database not available");
  }
  return db;
}

export { db };

export * from "./schema";