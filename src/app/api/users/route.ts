import { NextResponse } from "next/server";
import { getDb } from "@/db";
import { users } from "@/db/schema";

export async function GET() {
  const db = await getDb();
  if (!db) return NextResponse.json({ error: "Database not configured" }, { status: 503 });
  
  try {
    const allUsers = await (db as any).select().from(users);
    return NextResponse.json(allUsers);
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch users" }, { status: 500 });
  }
}

export async function POST(request: Request) {
  const db = await getDb();
  if (!db) return NextResponse.json({ error: "Database not configured" }, { status: 503 });
  
  try {
    const body = await request.json();
    const newUser = await (db as any).insert(users).values(body).returning();
    return NextResponse.json(newUser[0], { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Failed to create user" }, { status: 500 });
  }
}