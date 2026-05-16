"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { BarChart3, TrendingUp, TrendingDown } from "lucide-react";

interface Metric {
  name: string;
  value: number;
  change: number;
  trend: "up" | "down";
}

const mockMetrics: Metric[] = [
  { name: "Users", value: 1249, change: 12, trend: "up" },
  { name: "Revenue", value: 45231, change: 8.2, trend: "up" },
  { name: "Orders", value: 842, change: -3.1, trend: "down" },
  { name: "Growth", value: 23.5, change: 5.4, trend: "up" },
];

export function DashboardMetrics() {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setMetrics(mockMetrics);
      setLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-32 bg-neutral-100 animate-pulse rounded-lg" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.name}>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
            <BarChart3 className="h-4 w-4 text-neutral-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metric.value.toLocaleString()}</div>
            <div className="flex items-center text-xs text-neutral-500">
              {metric.trend === "up" ? (
                <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
              ) : (
                <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
              )}
              {metric.change > 0 ? "+" : ""}
              {metric.change}% from last month
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}