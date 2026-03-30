import { cn } from "@/lib/utils";

function Owl({
  className,
  bodyClassName
}: {
  className?: string;
  bodyClassName?: string;
}) {
  return (
    <div className={cn("relative h-20 w-20", className)}>
      <div className={cn("absolute inset-x-2 bottom-0 h-14 rounded-[40px] border border-amber-200", bodyClassName)} />
      <div className="absolute left-2 top-5 h-8 w-8 rounded-full border border-amber-200 bg-white" />
      <div className="absolute right-2 top-5 h-8 w-8 rounded-full border border-amber-200 bg-white" />
      <div className="absolute left-5 top-8 h-3 w-3 rounded-full bg-foreground" />
      <div className="absolute right-5 top-8 h-3 w-3 rounded-full bg-foreground" />
      <div className="absolute left-7 top-2 h-5 w-5 rotate-[-20deg] rounded-t-full border-l border-t border-amber-300 bg-transparent" />
      <div className="absolute right-7 top-2 h-5 w-5 rotate-[20deg] rounded-t-full border-r border-t border-amber-300 bg-transparent" />
      <div className="absolute left-1/2 top-11 h-0 w-0 -translate-x-1/2 border-l-[6px] border-r-[6px] border-t-[10px] border-l-transparent border-r-transparent border-t-orange-400" />
      <div className="absolute bottom-2 left-5 h-4 w-1 rounded-full bg-orange-300" />
      <div className="absolute bottom-2 right-5 h-4 w-1 rounded-full bg-orange-300" />
      <div className="absolute inset-x-6 bottom-3 h-5 rounded-full bg-white/35" />
    </div>
  );
}

export function OwlCluster({ compact = false }: { compact?: boolean }) {
  if (compact) {
    return (
      <div className="relative hidden h-14 w-20 items-end lg:flex">
        <Owl className="absolute left-0 bottom-0 h-10 w-10" bodyClassName="bg-[#d6f0d2]" />
        <Owl className="absolute right-0 bottom-0 h-12 w-12" bodyClassName="bg-[#f7d98e]" />
      </div>
    );
  }

  return (
    <div className="relative h-56 w-full max-w-sm">
      <div className="absolute left-2 top-12 h-24 w-24 rounded-full bg-emerald-100 blur-2xl" />
      <div className="absolute right-6 top-4 h-28 w-28 rounded-full bg-amber-100 blur-2xl" />
      <div className="absolute left-2 bottom-2">
        <Owl className="h-28 w-28" bodyClassName="bg-[#d9f0d5]" />
      </div>
      <div className="absolute left-24 top-0">
        <Owl className="h-24 w-24" bodyClassName="bg-[#f4d68c]" />
      </div>
      <div className="absolute right-8 bottom-0">
        <Owl className="h-32 w-32" bodyClassName="bg-[#f6efdb]" />
      </div>
      <div className="absolute right-0 top-24 rounded-full border border-white/70 bg-white/80 px-4 py-2 text-sm font-semibold text-foreground shadow-soft">
        Goal-first choices
      </div>
    </div>
  );
}
