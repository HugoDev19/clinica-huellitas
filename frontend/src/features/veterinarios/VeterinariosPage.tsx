import { useVeterinarios } from "@/application/useVeterinarios";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";

export function VeterinariosPage() {
  const { veterinarios, cargando, error } = useVeterinarios();

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Veterinarios</h1>
        <p className="text-sm text-slate-500">Equipo médico de la clínica</p>
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando ? (
        <LoadingSpinner />
      ) : veterinarios.length === 0 ? (
        <EmptyState titulo="No hay veterinarios registrados" />
      ) : (
        <Table>
          <TableHead>
            <tr>
              <Th>Código</Th>
              <Th>Nombre</Th>
              <Th>Disponibilidad</Th>
            </tr>
          </TableHead>
          <TableBody>
            {veterinarios.map((veterinario) => (
              <tr key={veterinario.id}>
                <Td>{veterinario.codigo}</Td>
                <Td>{veterinario.nombre}</Td>
                <Td>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                      veterinario.disponible ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"
                    }`}
                  >
                    {veterinario.disponible ? "Disponible" : "No disponible"}
                  </span>
                </Td>
              </tr>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
