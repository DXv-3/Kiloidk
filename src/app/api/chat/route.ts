import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { message } = await request.json();

    // Placeholder for AI response
    const response = `Echo: ${message}`;

    return NextResponse.json({ response });
  } catch {
    return NextResponse.json({ error: "Failed to process message" }, { status: 500 });
  }
}