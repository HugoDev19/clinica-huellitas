export function EmptyState({ titulo, descripcion }: { titulo: string; descripcion?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-1 rounded-xl border border-dashed border-slate-300 bg-slate-50 py-12 text-center">
      <p className="text-base font-semibold text-slate-700">{titulo}</p>
      {descripcion && <p className="text-sm text-slate-500">{descripcion}</p>}
    </div>
  );
}
