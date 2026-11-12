export function ErrorBanner({ mensaje }: { mensaje: string }) {
  return (
    <div role="alert" className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
      {mensaje}
    </div>
  );
}
