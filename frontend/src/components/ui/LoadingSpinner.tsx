export function LoadingSpinner({ etiqueta = "Cargando..." }: { etiqueta?: string }) {
  return (
    <div className="flex items-center justify-center gap-2 py-10 text-slate-500">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-slate-300 border-t-indigo-600" />
      <span>{etiqueta}</span>
    </div>
  );
}
