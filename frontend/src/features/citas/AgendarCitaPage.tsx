import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useMascotas } from "@/application/useMascotas";
import { useTutores } from "@/application/useTutores";
import { useVeterinarios } from "@/application/useVeterinarios";
import { useToast } from "@/components/feedback/ToastProvider";
import { BUTTON_PRIMARY_CLASS, BUTTON_SECONDARY_CLASS, INPUT_CLASS } from "@/components/ui/classNames";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { FormField } from "@/components/ui/FormField";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ETIQUETAS_TIPO_CONSULTA, TipoConsulta } from "@/domain/enums";
import { extraerMensajeError } from "@/infrastructure/apiClient";
import { citasApi } from "@/infrastructure/citasApi";

const esquemaCita = z.object({
  mascota_id: z.coerce.number({ invalid_type_error: "Selecciona una mascota" }).int().min(1, "Selecciona una mascota"),
  veterinario_id: z
    .coerce.number({ invalid_type_error: "Selecciona un veterinario" })
    .int()
    .min(1, "Selecciona un veterinario"),
  fecha_hora: z.string().min(1, "Selecciona fecha y hora"),
  tipo_consulta: z.nativeEnum(TipoConsulta, { errorMap: () => ({ message: "Selecciona un tipo de consulta" }) }),
  observaciones: z.string().optional(),
});
type CitaFormValues = z.infer<typeof esquemaCita>;

export function AgendarCitaPage() {
  const navigate = useNavigate();
  const { notificarExito, notificarError } = useToast();
  const {
    mascotas,
    cargando: cargandoMascotas,
    error: errorMascotas,
  } = useMascotas();
  const { tutores, cargando: cargandoTutores, error: errorTutores } = useTutores();
  const {
    veterinarios,
    cargando: cargandoVeterinarios,
    error: errorVeterinarios,
  } = useVeterinarios();
  const cargandoCatalogos = cargandoMascotas || cargandoTutores || cargandoVeterinarios;
  const errorCatalogos = errorMascotas || errorTutores || errorVeterinarios;

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CitaFormValues>({ resolver: zodResolver(esquemaCita) });

  const nombreTutor = (tutorId: number) => tutores.find((tutor) => tutor.id === tutorId)?.nombre ?? "";

  const onSubmit = async (valores: CitaFormValues) => {
    try {
      const cita = await citasApi.agendar(valores);
      notificarExito(`Cita ${cita.codigo} agendada correctamente. Se notificó al tutor.`);
      navigate("/citas");
    } catch (err) {
      notificarError(extraerMensajeError(err));
    }
  };

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Agendar cita</h1>
        <p className="text-sm text-slate-500">
          Horario de atención: lunes a sábado, de 8:00 a 17:00, en bloques de 30 minutos. Máximo 30 días de
          anticipación.
        </p>
      </div>

      {errorCatalogos && <ErrorBanner mensaje={errorCatalogos} />}
      {cargandoCatalogos && <LoadingSpinner etiqueta="Cargando mascotas, tutores y veterinarios..." />}
      {!cargandoCatalogos && !errorCatalogos && mascotas.length === 0 && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
          Para agendar, primero registra un tutor y su mascota en las secciones de{" "}
          <Link className="font-semibold underline" to="/tutores">Tutores</Link> y{" "}
          <Link className="font-semibold underline" to="/mascotas">Mascotas</Link>.
        </div>
      )}

      <form
        className="flex flex-col gap-4 rounded-xl border border-slate-200 bg-white p-6"
        onSubmit={handleSubmit(onSubmit)}
      >
        <FormField label="Mascota" error={errors.mascota_id?.message}>
          <select className={INPUT_CLASS} defaultValue="" disabled={cargandoCatalogos || !mascotas.length} {...register("mascota_id")}>
            <option value="" disabled>
              Selecciona una mascota
            </option>
            {mascotas.map((mascota) => (
              <option key={mascota.id} value={mascota.id}>
                {mascota.nombre} ({mascota.especie}, {mascota.edad_anios} años) — {nombreTutor(mascota.tutor_id)}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="Veterinario" error={errors.veterinario_id?.message}>
          <select className={INPUT_CLASS} defaultValue="" disabled={cargandoCatalogos || !veterinarios.length} {...register("veterinario_id")}>
            <option value="" disabled>
              Selecciona un veterinario
            </option>
            {veterinarios.map((veterinario) => (
              <option key={veterinario.id} value={veterinario.id}>
                {veterinario.codigo} — {veterinario.nombre}
              </option>
            ))}
          </select>
        </FormField>

        <FormField
          label="Fecha y hora"
          error={errors.fecha_hora?.message}
          hint="Debe estar dentro de los próximos 30 días"
        >
          <input type="datetime-local" step={1800} className={INPUT_CLASS} {...register("fecha_hora")} />
        </FormField>

        <FormField label="Tipo de consulta" error={errors.tipo_consulta?.message}>
          <select className={INPUT_CLASS} defaultValue="" {...register("tipo_consulta")}>
            <option value="" disabled>
              Selecciona un tipo
            </option>
            {Object.values(TipoConsulta).map((tipo) => (
              <option key={tipo} value={tipo}>
                {ETIQUETAS_TIPO_CONSULTA[tipo]}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="Observaciones (opcional)">
          <textarea className={INPUT_CLASS} rows={3} {...register("observaciones")} />
        </FormField>

        <div className="flex justify-end gap-3">
          <button type="button" className={BUTTON_SECONDARY_CLASS} onClick={() => navigate("/citas")}>
            Cancelar
          </button>
          <button
            type="submit"
            className={BUTTON_PRIMARY_CLASS}
            disabled={isSubmitting || cargandoCatalogos || !mascotas.length || !veterinarios.length}
          >
            {isSubmitting ? "Agendando..." : "Agendar cita"}
          </button>
        </div>
      </form>
    </div>
  );
}
