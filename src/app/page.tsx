import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-900">
      <div className="container mx-auto px-4 py-16">
        <div className="flex flex-col items-center justify-center space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold tracking-tight text-neutral-900 dark:text-neutral-50 sm:text-6xl">
              Next.js Starter Template
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400">
              A minimal Next.js 16 starter with TypeScript and Tailwind CSS
            </p>
          </div>

          <div className="flex gap-4">
            <Button>Get Started</Button>
            <Button variant="outline">Learn More</Button>
          </div>

          <div className="grid gap-6 md:grid-cols-3 w-full max-w-4xl">
            <Card>
              <CardHeader>
                <CardTitle>TypeScript</CardTitle>
                <CardDescription>Strict mode enabled for type safety</CardDescription>
              </CardHeader>
              <CardContent>
                <LoadingSpinner className="text-blue-600" />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tailwind CSS 4</CardTitle>
                <CardDescription>Utility-first CSS framework</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-4 w-full bg-gradient-to-r from-blue-500 to-purple-500 rounded" />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Ready to Extend</CardTitle>
                <CardDescription>Build anything with AI assistance</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Add Features
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </main>
  );
}