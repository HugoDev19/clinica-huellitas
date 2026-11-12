import { useState } from "react";

import { useAgendaDiaria } from "@/application/useAgendaDiaria";
import { useMascotas } from "@/application/useMascotas";
import { useVeterinarios } from "@/application/useVeterinarios";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { EstadoBadge } from "@/components/ui/EstadoBadge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";
import { INPUT_CLASS } from "@/components/ui/classNames";

function hoyISO(): string {
  const ahora = new Date();
  const local = new Date(ahora.getTime() - ahora.getTimezoneOffset() * 60_000);
  return local.toISOString().slice(0, 10);
}

export function AgendaDiariaPage() {
  const { veterinarios } = useVeterinarios();
  const { mascotas } = useMascotas();
  const [veterinarioId, setVeterinarioId] = useState<number | null>(null);
  const [fecha, setFecha] = useState(hoyISO());

  const idEfectivo = veterinarioId ?? veterinarios[0]?.id ?? null;
  const { citas, cargando, error } = useAgendaDiaria(idEfectivo, fecha);

  const nombreMascota = (id: number) => mascotas.find((mascota) => mascota.id === id)?.nombre ?? `Mascota #${id}`;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Agenda diaria</h1>
        <p className="text-sm text-slate-500">Consulta cronológica de las citas de un veterinario (CU3)</p>
      </div>

      <div className="flex flex-wrap gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <select
          className={`${INPUT_CLASS} w-auto`}
          value={idEfectivo ?? ""}
          onChange={(evento) => setVeterinarioId(Number(evento.target.value))}
        >
          {veterinarios.map((veterinario) => (
            <option key={veterinario.id} value={veterinario.id}>
              {veterinario.codigo} — {veterinario.nombre}
            </option>
          ))}
        </select>
        <input
          type="date"
          className={`${INPUT_CLASS} w-auto`}
          value={fecha}
          onChange={(evento) => setFecha(evento.target.value)}
        />
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando ? (
        <LoadingSpinner />
      ) : citas.length === 0 ? (
        <EmptyState
          titulo="Sin citas para este día"
          descripcion="No hay citas programadas para el veterinario y fecha seleccionados."
        />
      ) : (
        <Table>
          <TableHead>
            <tr>
              <Th>Hora</Th>
              <Th>Código</Th>
              <Th>Mascota</Th>
              <Th>Tipo</Th>
              <Th>Estado</Th>
            </tr>
          </TableHead>
          <TableBody>
            {citas.map((cita) => (
              <tr key={cita.id}>
                <Td>
                  {new Date(cita.fecha_hora).toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" })}
                </Td>
                <Td>{cita.codigo}</Td>
                <Td>{nombreMascota(cita.mascota_id)}</Td>
                <Td>{cita.tipo_consulta}</Td>
                <Td>
                  <EstadoBadge estado={cita.estado} />
                </Td>
              </tr>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
