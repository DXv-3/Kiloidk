"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-50">
        Something went wrong
      </h1>
      <p className="mt-4 text-neutral-600 dark:text-neutral-400">{error.message}</p>
      <Button onClick={reset} className="mt-8">
        Try again
      </Button>
    </div>
  );
}