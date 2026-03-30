"use client";

import { useRef, useState } from "react";
import { FileImage, FileText, FileUp, ScanSearch } from "lucide-react";

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
        "group relative flex min-h-72 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-[36px] border-2 border-dashed px-6 py-10 text-center transition",
        dragging
          ? "border-primary bg-primary/10"
          : "border-border bg-white/80 hover:border-primary/60 hover:bg-white"
      )}
    >
      <div className="absolute left-4 top-4 h-16 w-16 rounded-full bg-emerald-100 blur-2xl" />
      <div className="absolute right-6 top-8 h-20 w-20 rounded-full bg-amber-100 blur-2xl" />
      <input
        ref={inputRef}
        type="file"
        accept=".png,.jpg,.jpeg,.pdf,.webp"
        className="hidden"
        onChange={(event) => handleFile(event.target.files?.[0])}
      />
      <div className="relative z-10 rounded-full bg-primary/10 p-5">
        <FileUp className="h-10 w-10 text-primary" />
      </div>
      <p className="relative z-10 mt-5 text-2xl font-semibold text-foreground md:text-3xl">
        Drag and drop menu images or PDFs
      </p>
      <p className="relative z-10 mt-3 max-w-xl text-base text-muted-foreground md:text-lg">
        Upload a hawker menu snapshot, cafe menu screenshot, or restaurant PDF and PlateWise will turn it into structured food options.
      </p>
      <div className="relative z-10 mt-6 flex flex-wrap justify-center gap-3">
        <div className="rounded-full bg-white px-4 py-2 text-sm font-semibold text-foreground shadow-soft">
          <FileImage className="mr-2 inline h-4 w-4 text-primary" />
          JPG / PNG / WEBP
        </div>
        <div className="rounded-full bg-white px-4 py-2 text-sm font-semibold text-foreground shadow-soft">
          <FileText className="mr-2 inline h-4 w-4 text-primary" />
          PDF menus
        </div>
        <div className="rounded-full bg-white px-4 py-2 text-sm font-semibold text-foreground shadow-soft">
          <ScanSearch className="mr-2 inline h-4 w-4 text-primary" />
          OCR + ranking
        </div>
      </div>
      {fileName ? (
        <p className="relative z-10 mt-6 rounded-full bg-secondary px-4 py-2 text-sm font-medium text-foreground">
          Selected: {fileName}
        </p>
      ) : (
        <p className="relative z-10 mt-6 text-sm text-muted-foreground">
          Tap anywhere in this panel to browse files
        </p>
      )}
    </div>
  );
}
