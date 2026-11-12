import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useVeterinarios } from "@/application/useVeterinarios";
import { useToast } from "@/components/feedback/ToastProvider";
import { BUTTON_PRIMARY_CLASS, BUTTON_SECONDARY_CLASS, INPUT_CLASS } from "@/components/ui/classNames";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { FormField } from "@/components/ui/FormField";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";
import { extraerMensajeError } from "@/infrastructure/apiClient";

const esquemaVeterinario = z.object({
  codigo: z.string().trim().min(1, "El código es obligatorio").max(20, "Máximo 20 caracteres"),
  nombre: z.string().trim().min(1, "El nombre es obligatorio").max(150, "Máximo 150 caracteres"),
});
type VeterinarioFormValues = z.infer<typeof esquemaVeterinario>;

export function VeterinariosPage() {
  const { veterinarios, cargando, error, registrar } = useVeterinarios();
  const { notificarExito, notificarError } = useToast();
  const [modalAbierto, setModalAbierto] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<VeterinarioFormValues>({ resolver: zodResolver(esquemaVeterinario) });

  const onSubmit = async (valores: VeterinarioFormValues) => {
    try {
      const veterinario = await registrar(valores);
      notificarExito(`Veterinario ${veterinario.nombre} registrado correctamente.`);
      reset();
      setModalAbierto(false);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Veterinarios</h1>
          <p className="text-sm text-slate-500">Equipo médico de la clínica</p>
        </div>
        <button type="button" className={BUTTON_PRIMARY_CLASS} onClick={() => setModalAbierto(true)}>
          + Nuevo veterinario
        </button>
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

      <Modal
        abierto={modalAbierto}
        onCerrar={() => setModalAbierto(false)}
        titulo="Registrar veterinario"
      >
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Código" error={errors.codigo?.message}>
            <input
              className={INPUT_CLASS}
              placeholder="Ej. VET-03"
              maxLength={20}
              {...register("codigo")}
            />
          </FormField>
          <FormField label="Nombre completo" error={errors.nombre?.message}>
            <input className={INPUT_CLASS} maxLength={150} {...register("nombre")} />
          </FormField>
          <div className="mt-2 flex justify-end gap-3">
            <button type="button" className={BUTTON_SECONDARY_CLASS} onClick={() => setModalAbierto(false)}>
              Cancelar
            </button>
            <button type="submit" className={BUTTON_PRIMARY_CLASS} disabled={isSubmitting}>
              {isSubmitting ? "Guardando..." : "Guardar"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
