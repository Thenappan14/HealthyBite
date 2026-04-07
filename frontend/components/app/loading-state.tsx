import { cn } from "@/lib/utils";

export function LoadingState({
  label = "Loading PlateWise insights...",
  fullScreen = false
}: {
  label?: string;
  fullScreen?: boolean;
}) {
  return (
    <div
      className={cn(
        "flex items-center justify-center rounded-[28px] border border-dashed border-border bg-white/80 p-8 backdrop-blur-sm",
        fullScreen ? "fixed inset-0 z-50 rounded-none border-0 bg-stone-950/20 px-4" : "min-h-48"
      )}
    >
      <div className="w-full max-w-xl rounded-[32px] border border-white/70 bg-[#fffaf3] p-8 shadow-[0_20px_80px_rgba(43,63,53,0.18)]">
        <div className="space-y-6 text-center">
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.34em] text-muted-foreground">
              PlateWise
            </p>
            <h3 className="font-display text-3xl text-foreground md:text-4xl">
              Building your healthy bowl
            </h3>
          </div>

          <div className="relative mx-auto h-56 w-72">
            <div className="absolute inset-x-6 bottom-8 h-20 rounded-[0_0_90px_90px] border-[6px] border-[#2f5a48] border-t-0 bg-gradient-to-b from-[#f8d57a] to-[#f2c25a] shadow-[inset_0_-10px_24px_rgba(141,88,19,0.15)]" />
            <div className="absolute inset-x-12 bottom-24 h-10 rounded-full bg-[#f5f0df]" />

            <IngredientBlob className="left-8 top-12 bg-[#ff8d6b] delay-75" />
            <IngredientBlob className="left-20 top-6 bg-[#71c17a] delay-150" />
            <IngredientBlob className="left-36 top-14 bg-[#f6c453] delay-300" />
            <IngredientBlob className="left-52 top-8 bg-[#c86f8a] delay-500" />
            <IngredientBlob className="left-24 top-24 bg-[#96d8dc] delay-700" />
            <IngredientBlob className="left-44 top-26 bg-[#7bbf5c] delay-1000" />

            <div className="absolute inset-x-16 bottom-12 h-2 rounded-full bg-[#d89a33]/40 blur-sm" />
          </div>

          <div className="space-y-2">
            <p className="text-lg font-medium text-foreground">{label}</p>
            <p className="text-sm text-muted-foreground">
              Extracting menu text, checking dish fit, and plating your best options.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function IngredientBlob({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "absolute h-11 w-11 animate-bounce rounded-full shadow-[0_8px_18px_rgba(43,63,53,0.12)]",
        className
      )}
    />
  );
}
