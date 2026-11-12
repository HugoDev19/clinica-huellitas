import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useMascotas } from "@/application/useMascotas";
import { useTutores } from "@/application/useTutores";
import { useToast } from "@/components/feedback/ToastProvider";
import {
  BUTTON_DANGER_CLASS,
  BUTTON_GHOST_CLASS,
  BUTTON_PRIMARY_CLASS,
  BUTTON_SECONDARY_CLASS,
  INPUT_CLASS,
} from "@/components/ui/classNames";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { FormField } from "@/components/ui/FormField";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";
import type { Mascota } from "@/domain/types";
import { extraerMensajeError } from "@/infrastructure/apiClient";

const esquemaMascota = z.object({
  nombre: z.string().min(1, "El nombre es obligatorio").max(100),
  especie: z.string().min(1, "La especie es obligatoria").max(50),
  edad_anios: z.coerce.number({ invalid_type_error: "Ingresa la edad" }).int().min(0).max(100),
  tutor_id: z.coerce.number({ invalid_type_error: "Selecciona un tutor" }).int().min(1, "Selecciona un tutor"),
});
type MascotaFormValues = z.infer<typeof esquemaMascota>;

export function MascotasPage() {
  const { mascotas, cargando, error, registrar, actualizar, eliminar } = useMascotas();
  const { tutores } = useTutores();
  const { notificarExito, notificarError } = useToast();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [mascotaEditando, setMascotaEditando] = useState<Mascota | null>(null);
  const [mascotaEliminando, setMascotaEliminando] = useState<Mascota | null>(null);
  const [eliminando, setEliminando] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<MascotaFormValues>({ resolver: zodResolver(esquemaMascota) });

  const nombreTutor = (tutorId: number) => tutores.find((tutor) => tutor.id === tutorId)?.nombre ?? `#${tutorId}`;

  const abrirRegistro = () => {
    setMascotaEditando(null);
    reset();
    setModalAbierto(true);
  };

  const abrirEdicion = (mascota: Mascota) => {
    setMascotaEditando(mascota);
    reset({
      nombre: mascota.nombre,
      especie: mascota.especie,
      edad_anios: mascota.edad_anios,
      tutor_id: mascota.tutor_id,
    });
    setModalAbierto(true);
  };

  const onSubmit = async (valores: MascotaFormValues) => {
    try {
      if (mascotaEditando) {
        await actualizar(mascotaEditando.id, valores);
        notificarExito(`Mascota ${valores.nombre} actualizada correctamente.`);
      } else {
        await registrar(valores);
        notificarExito(`Mascota ${valores.nombre} registrada correctamente.`);
      }
      reset();
      setModalAbierto(false);
      setMascotaEditando(null);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    }
  };

  const confirmarEliminacion = async () => {
    if (!mascotaEliminando) return;
    setEliminando(true);
    try {
      await eliminar(mascotaEliminando.id);
      notificarExito(`Mascota ${mascotaEliminando.nombre} eliminada correctamente.`);
      setMascotaEliminando(null);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    } finally {
      setEliminando(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Mascotas</h1>
          <p className="text-sm text-slate-500">Pacientes registrados en la clínica</p>
        </div>
        <button type="button" className={BUTTON_PRIMARY_CLASS} onClick={abrirRegistro}>
          + Nueva mascota
        </button>
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando ? (
        <LoadingSpinner />
      ) : mascotas.length === 0 ? (
        <EmptyState
          titulo="Aún no hay mascotas registradas"
          descripcion="Registra tutores primero y luego agrega sus mascotas."
        />
      ) : (
        <Table>
          <TableHead>
            <tr>
              <Th>Nombre</Th>
              <Th>Especie</Th>
              <Th>Edad</Th>
              <Th>Tutor</Th>
              <Th>Acciones</Th>
            </tr>
          </TableHead>
          <TableBody>
            {mascotas.map((mascota) => (
              <tr key={mascota.id}>
                <Td>{mascota.nombre}</Td>
                <Td>{mascota.especie}</Td>
                <Td>
                  {mascota.edad_anios} años
                  {mascota.edad_anios >= 10 && (
                    <span className="ml-2 inline-flex items-center rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-semibold text-indigo-700">
                      Senior · 10% dto.
                    </span>
                  )}
                </Td>
                <Td>{nombreTutor(mascota.tutor_id)}</Td>
                <Td className="whitespace-nowrap">
                  <button type="button" className={BUTTON_GHOST_CLASS} onClick={() => abrirEdicion(mascota)}>
                    Editar
                  </button>
                  <button
                    type="button"
                    className={BUTTON_DANGER_CLASS}
                    onClick={() => setMascotaEliminando(mascota)}
                  >
                    Eliminar
                  </button>
                </Td>
              </tr>
            ))}
          </TableBody>
        </Table>
      )}

      <Modal
        abierto={modalAbierto}
        onCerrar={() => {
          setModalAbierto(false);
          setMascotaEditando(null);
        }}
        titulo={mascotaEditando ? "Editar mascota" : "Registrar mascota"}
      >
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Tutor" error={errors.tutor_id?.message}>
            <select className={INPUT_CLASS} defaultValue="" {...register("tutor_id")}>
              <option value="" disabled>
                Selecciona un tutor
              </option>
              {tutores.map((tutor) => (
                <option key={tutor.id} value={tutor.id}>
                  {tutor.nombre} — {tutor.documento}
                </option>
              ))}
            </select>
          </FormField>
          <FormField label="Nombre de la mascota" error={errors.nombre?.message}>
            <input className={INPUT_CLASS} {...register("nombre")} />
          </FormField>
          <FormField label="Especie" error={errors.especie?.message}>
            <input className={INPUT_CLASS} placeholder="Perro, gato..." {...register("especie")} />
          </FormField>
          <FormField label="Edad (años)" error={errors.edad_anios?.message} hint="Desde 10 años aplica descuento del 10%">
            <input type="number" min={0} max={100} className={INPUT_CLASS} {...register("edad_anios")} />
          </FormField>
          <div className="mt-2 flex justify-end gap-3">
            <button type="button" className={BUTTON_SECONDARY_CLASS} onClick={() => setModalAbierto(false)}>
              Cancelar
            </button>
            <button type="submit" className={BUTTON_PRIMARY_CLASS} disabled={isSubmitting}>
              {isSubmitting ? "Guardando..." : mascotaEditando ? "Guardar cambios" : "Guardar"}
            </button>
          </div>
        </form>
      </Modal>
      <ConfirmDialog
        abierto={mascotaEliminando !== null}
        titulo="Eliminar mascota"
        mensaje={`¿Seguro que deseas eliminar a ${mascotaEliminando?.nombre ?? "esta mascota"}? Las mascotas con citas asociadas no se pueden eliminar.`}
        etiquetaConfirmar="Eliminar"
        cargando={eliminando}
        onCancelar={() => setMascotaEliminando(null)}
        onConfirmar={confirmarEliminacion}
      />
    </div>
  );
}
