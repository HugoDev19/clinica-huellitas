import { ETIQUETAS_ESTADO_CITA, EstadoCita } from "@/domain/enums";

const ESTILOS: Record<EstadoCita, string> = {
  [EstadoCita.PROGRAMADA]: "bg-blue-100 text-blue-700",
  [EstadoCita.ATENDIDA]: "bg-emerald-100 text-emerald-700",
  [EstadoCita.CANCELADA]: "bg-rose-100 text-rose-700",
  [EstadoCita.NO_ASISTIO]: "bg-amber-100 text-amber-700",
};

export function EstadoBadge({ estado }: { estado: EstadoCita }) {
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${ESTILOS[estado]}`}>
      {ETIQUETAS_ESTADO_CITA[estado]}
    </span>
  );
}
