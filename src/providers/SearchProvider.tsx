"use client";

import { createContext, useContext, useEffect, useState } from "react";

interface SearchContextValue {
  query: string;
  setQuery: (q: string) => void;
  results: string[];
}

const SearchContext = createContext<SearchContextValue | null>(null);

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);

  useEffect(() => {
    if (!query) return;

    const timer = setTimeout(() => {
      setResults([`Result 1 for "${query}"`, `Result 2 for "${query}"`]);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <SearchContext.Provider value={{ query, setQuery, results }}>
      {children}
    </SearchContext.Provider>
  );
}

export function useSearch() {
  const ctx = useContext(SearchContext);
  if (!ctx) throw new Error("useSearch must be used within SearchProvider");
  return ctx;
}