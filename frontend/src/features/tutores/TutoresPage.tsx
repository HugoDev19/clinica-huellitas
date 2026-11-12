import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useTutores } from "@/application/useTutores";
import { useToast } from "@/components/feedback/ToastProvider";
import { BUTTON_PRIMARY_CLASS, BUTTON_SECONDARY_CLASS, INPUT_CLASS } from "@/components/ui/classNames";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { FormField } from "@/components/ui/FormField";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";
import { extraerMensajeError } from "@/infrastructure/apiClient";

const esquemaTutor = z.object({
  nombre: z.string().min(1, "El nombre es obligatorio").max(150),
  documento: z.string().min(1, "El documento es obligatorio").max(30),
  telefono: z.string().min(1, "El teléfono es obligatorio").max(30),
  correo: z.string().email("Correo electrónico inválido"),
});
type TutorFormValues = z.infer<typeof esquemaTutor>;

export function TutoresPage() {
  const { tutores, cargando, error, registrar } = useTutores();
  const { notificarExito, notificarError } = useToast();
  const [modalAbierto, setModalAbierto] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TutorFormValues>({ resolver: zodResolver(esquemaTutor) });

  const onSubmit = async (valores: TutorFormValues) => {
    try {
      await registrar(valores);
      notificarExito(`Tutor ${valores.nombre} registrado correctamente.`);
      reset();
      setModalAbierto(false);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Tutores</h1>
          <p className="text-sm text-slate-500">Personas responsables de las mascotas atendidas</p>
        </div>
        <button type="button" className={BUTTON_PRIMARY_CLASS} onClick={() => setModalAbierto(true)}>
          + Nuevo tutor
        </button>
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando ? (
        <LoadingSpinner />
      ) : tutores.length === 0 ? (
        <EmptyState
          titulo="Aún no hay tutores registrados"
          descripcion="Registra el primer tutor para comenzar a agendar citas."
        />
      ) : (
        <Table>
          <TableHead>
            <tr>
              <Th>Nombre</Th>
              <Th>Documento</Th>
              <Th>Teléfono</Th>
              <Th>Correo</Th>
            </tr>
          </TableHead>
          <TableBody>
            {tutores.map((tutor) => (
              <tr key={tutor.id}>
                <Td>{tutor.nombre}</Td>
                <Td>{tutor.documento}</Td>
                <Td>{tutor.telefono}</Td>
                <Td>{tutor.correo}</Td>
              </tr>
            ))}
          </TableBody>
        </Table>
      )}

      <Modal abierto={modalAbierto} onCerrar={() => setModalAbierto(false)} titulo="Registrar tutor">
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Nombre completo" error={errors.nombre?.message}>
            <input className={INPUT_CLASS} {...register("nombre")} />
          </FormField>
          <FormField label="Documento" error={errors.documento?.message}>
            <input className={INPUT_CLASS} {...register("documento")} />
          </FormField>
          <FormField
            label="Teléfono"
            error={errors.telefono?.message}
            hint="Se usará para enviar notificaciones por WhatsApp"
          >
            <input className={INPUT_CLASS} {...register("telefono")} />
          </FormField>
          <FormField label="Correo electrónico" error={errors.correo?.message}>
            <input type="email" className={INPUT_CLASS} {...register("correo")} />
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
