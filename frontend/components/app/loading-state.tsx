export function LoadingState({ label = "Loading PlateWise insights..." }: { label?: string }) {
  return (
    <div className="flex min-h-48 items-center justify-center rounded-[28px] border border-dashed border-border bg-white/70 p-8">
      <div className="space-y-3 text-center">
        <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-secondary border-t-primary" />
        <p className="text-sm text-muted-foreground">{label}</p>
      </div>
    </div>
  );
}

