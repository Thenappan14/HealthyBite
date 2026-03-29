"use client";

import { useRef, useState } from "react";
import { FileUp } from "lucide-react";

import { cn } from "@/lib/utils";

export function UploadDropzone({
  onFileSelected
}: {
  onFileSelected?: (file: File) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState<string>("");

  function handleFile(file?: File) {
    if (!file) {
      return;
    }
    setFileName(file.name);
    onFileSelected?.(file);
  }

  return (
    <div
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(event) => {
        event.preventDefault();
        setDragging(false);
        handleFile(event.dataTransfer.files?.[0]);
      }}
      onClick={() => inputRef.current?.click()}
      className={cn(
        "group flex min-h-64 cursor-pointer flex-col items-center justify-center rounded-[32px] border-2 border-dashed px-6 py-10 text-center transition",
        dragging ? "border-primary bg-primary/5" : "border-border bg-white/70 hover:border-primary/60 hover:bg-white"
      )}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".png,.jpg,.jpeg,.pdf,.webp"
        className="hidden"
        onChange={(event) => handleFile(event.target.files?.[0])}
      />
      <FileUp className="mb-4 h-10 w-10 text-primary" />
      <p className="font-medium text-foreground">Drag and drop menu images or PDFs</p>
      <p className="mt-2 text-sm text-muted-foreground">Tap to browse. Supported: JPG, PNG, WEBP, PDF.</p>
      {fileName ? <p className="mt-5 text-sm font-medium text-foreground">{fileName}</p> : null}
    </div>
  );
}
