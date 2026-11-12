interface StatCardProps {
  titulo: string;
  valor: string | number;
  acento?: string;
}

export function StatCard({ titulo, valor, acento = "border-indigo-500" }: StatCardProps) {
  return (
    <div className={`rounded-xl border-l-4 ${acento} bg-white p-4 shadow-sm`}>
      <p className="text-sm text-slate-500">{titulo}</p>
      <p className="mt-1 text-2xl font-bold text-slate-900">{valor}</p>
    </div>
  );
}
