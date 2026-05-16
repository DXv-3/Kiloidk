"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Upload, X, FileText } from "lucide-react";

interface FileUploadProps {
  onUpload: (files: File[]) => void;
  accept?: string;
  multiple?: boolean;
  maxSize?: number;
}

export function FileUpload({ onUpload, accept = "*", multiple = false, maxSize = 5 }: FileUploadProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [dragActive, setDragActive] = useState(false);

  const handleFiles = (newFiles: FileList) => {
    const fileArray = Array.from(newFiles).filter(
      (f) => f.size <= maxSize * 1024 * 1024
    );
    setFiles((prev) => [...prev, ...fileArray]);
    onUpload(fileArray);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          dragActive ? "border-blue-500 bg-blue-50" : "border-neutral-300"
        }`}
        onDragEnter={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setDragActive(false);
        }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          setDragActive(false);
          handleFiles(e.dataTransfer.files);
        }}
      >
        <Upload className="mx-auto h-12 w-12 text-neutral-400" />
        <p className="mt-2 text-sm text-neutral-600">
          Drop files here or <label className="text-blue-600 cursor-pointer">browse</label>
        </p>
        <input
          type="file"
          className="hidden"
          accept={accept}
          multiple={multiple}
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
      </div>

      {files.length > 0 && (
        <div className="space-y-2">
          {files.map((file, i) => (
            <div key={i} className="flex items-center gap-2 p-2 bg-neutral-50 rounded">
              <FileText className="h-4 w-4" />
              <span className="flex-1 text-sm">{file.name}</span>
              <button onClick={() => removeFile(i)}>
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      <Button onClick={() => onUpload(files)} disabled={files.length === 0}>
        Upload {files.length} file(s)
      </Button>
    </div>
  );
}