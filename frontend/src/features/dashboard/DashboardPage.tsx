import { useState } from "react";

import { useDashboard } from "@/application/useDashboard";
import { useVeterinarios } from "@/application/useVeterinarios";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { EstadoBadge } from "@/components/ui/EstadoBadge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { StatCard } from "@/components/ui/StatCard";
import { INPUT_CLASS } from "@/components/ui/classNames";

function hoyISO(): string {
  const ahora = new Date();
  const local = new Date(ahora.getTime() - ahora.getTimezoneOffset() * 60_000);
  return local.toISOString().slice(0, 10);
}

export function DashboardPage() {
  const [fecha, setFecha] = useState(hoyISO());
  const { stats, cargando, error } = useDashboard(fecha);
  const { veterinarios } = useVeterinarios();

  const nombreVeterinario = (id: number) =>
    veterinarios.find((veterinario) => veterinario.id === id)?.nombre ?? `Veterinario #${id}`;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-sm text-slate-500">Resumen de la actividad diaria de la clínica</p>
        </div>
        <input
          type="date"
          value={fecha}
          onChange={(evento) => setFecha(evento.target.value)}
          className={`${INPUT_CLASS} w-auto`}
        />
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando && !stats && <LoadingSpinner etiqueta="Cargando estadísticas..." />}

      {stats && (
        <>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <StatCard titulo="Citas del día" valor={stats.total_citas} acento="border-indigo-500" />
            <StatCard titulo="Programadas" valor={stats.programadas} acento="border-blue-500" />
            <StatCard titulo="Atendidas" valor={stats.atendidas} acento="border-emerald-500" />
            <StatCard titulo="Canceladas" valor={stats.canceladas} acento="border-rose-500" />
            <StatCard titulo="No asistió" valor={stats.no_asistio} acento="border-amber-500" />
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <section className="rounded-xl border border-slate-200 bg-white p-4">
              <h2 className="mb-3 text-base font-semibold text-slate-900">Próximas citas</h2>
              {stats.proximas_citas.length === 0 ? (
                <EmptyState
                  titulo="Sin próximas citas"
                  descripcion="No hay citas programadas pendientes para este día."
                />
              ) : (
                <ul className="flex flex-col gap-3">
                  {stats.proximas_citas.map((cita) => (
                    <li
                      key={cita.id}
                      className="flex items-center justify-between rounded-lg border border-slate-100 px-3 py-2"
                    >
                      <div>
                        <p className="text-sm font-medium text-slate-800">{cita.codigo}</p>
                        <p className="text-xs text-slate-500">
                          {new Date(cita.fecha_hora).toLocaleString("es-CO")}
                        </p>
                      </div>
                      <EstadoBadge estado={cita.estado} />
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section className="rounded-xl border border-slate-200 bg-white p-4">
              <h2 className="mb-3 text-base font-semibold text-slate-900">Distribución por veterinario</h2>
              {stats.distribucion_por_veterinario.length === 0 ? (
                <EmptyState titulo="Sin datos" descripcion="No hay citas registradas este día." />
              ) : (
                <ul className="flex flex-col gap-3">
                  {stats.distribucion_por_veterinario.map((item) => {
                    const porcentaje =
                      stats.total_citas > 0 ? Math.round((item.total / stats.total_citas) * 100) : 0;
                    return (
                      <li key={item.veterinario_id}>
                        <div className="mb-1 flex justify-between text-sm text-slate-600">
                          <span>{nombreVeterinario(item.veterinario_id)}</span>
                          <span>{item.total}</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-100">
                          <div
                            className="h-2 rounded-full bg-indigo-500"
                            style={{ width: `${porcentaje}%` }}
                          />
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
            </section>
          </div>
        </>
      )}
    </div>
  );
}
