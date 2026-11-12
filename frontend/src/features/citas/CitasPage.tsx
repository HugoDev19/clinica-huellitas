import { type FormEvent, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { useCitas } from "@/application/useCitas";
import { useMascotas } from "@/application/useMascotas";
import { useVeterinarios } from "@/application/useVeterinarios";
import { useToast } from "@/components/feedback/ToastProvider";
import {
  BUTTON_GHOST_CLASS,
  BUTTON_PRIMARY_CLASS,
  BUTTON_SECONDARY_CLASS,
  INPUT_CLASS,
} from "@/components/ui/classNames";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { EstadoBadge } from "@/components/ui/EstadoBadge";
import { FormField } from "@/components/ui/FormField";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Table, TableBody, TableHead, Td, Th } from "@/components/ui/Table";
import type { Cita } from "@/domain/types";
import { EstadoCita } from "@/domain/enums";
import { extraerMensajeError } from "@/infrastructure/apiClient";

export function CitasPage() {
  const [fecha, setFecha] = useState("");
  const [veterinarioId, setVeterinarioId] = useState("");
  const [mascotaId, setMascotaId] = useState("");
  const [estado, setEstado] = useState("");
  const [pagina, setPagina] = useState(1);

  const filtros = useMemo(
    () => ({
      fecha: fecha || undefined,
      veterinario_id: veterinarioId ? Number(veterinarioId) : undefined,
      mascota_id: mascotaId ? Number(mascotaId) : undefined,
      estado: estado || undefined,
      page: pagina,
    }),
    [fecha, veterinarioId, mascotaId, estado, pagina],
  );

  const {
    citas,
    total,
    hayPaginaAnterior,
    hayPaginaSiguiente,
    cargando,
    error,
    recargar,
    cancelar,
    atender,
    marcarNoAsistio,
  } = useCitas(filtros);
  const { veterinarios } = useVeterinarios();
  const { mascotas } = useMascotas();
  const { notificarExito, notificarError } = useToast();

  const [citaParaCancelar, setCitaParaCancelar] = useState<Cita | null>(null);
  const [citaParaNoAsistio, setCitaParaNoAsistio] = useState<Cita | null>(null);
  const [citaParaAtender, setCitaParaAtender] = useState<Cita | null>(null);
  const [observaciones, setObservaciones] = useState("");
  const [procesando, setProcesando] = useState(false);

  const nombreMascota = (id: number) => mascotas.find((mascota) => mascota.id === id)?.nombre ?? `Mascota #${id}`;
  const nombreVeterinario = (id: number) =>
    veterinarios.find((veterinario) => veterinario.id === id)?.nombre ?? `Veterinario #${id}`;

  const hayFiltrosActivos = Boolean(fecha || veterinarioId || mascotaId || estado);
  const limpiarFiltros = () => {
    setFecha("");
    setVeterinarioId("");
    setMascotaId("");
    setEstado("");
    setPagina(1);
  };

  const confirmarCancelacion = async () => {
    if (!citaParaCancelar) return;
    setProcesando(true);
    try {
      await cancelar(citaParaCancelar.id);
      await recargar();
      notificarExito(`Cita ${citaParaCancelar.codigo} cancelada. Se notificó al tutor.`);
      setCitaParaCancelar(null);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    } finally {
      setProcesando(false);
    }
  };

  const confirmarNoAsistio = async () => {
    if (!citaParaNoAsistio) return;
    setProcesando(true);
    try {
      await marcarNoAsistio(citaParaNoAsistio.id);
      await recargar();
      notificarExito(`Cita ${citaParaNoAsistio.codigo} marcada como no asistida.`);
      setCitaParaNoAsistio(null);
    } catch (err) {
      notificarError(extraerMensajeError(err));
    } finally {
      setProcesando(false);
    }
  };

  const confirmarAtencion = async (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    if (!citaParaAtender) return;
    setProcesando(true);
    try {
      await atender(citaParaAtender.id, observaciones);
      await recargar();
      notificarExito(`Cita ${citaParaAtender.codigo} marcada como atendida.`);
      setCitaParaAtender(null);
      setObservaciones("");
    } catch (err) {
      notificarError(extraerMensajeError(err));
    } finally {
      setProcesando(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Historial de citas</h1>
          <p className="text-sm text-slate-500">{total} cita(s) encontradas</p>
        </div>
        <Link to="/citas/agendar" className={BUTTON_PRIMARY_CLASS}>
          + Agendar cita
        </Link>
      </div>

      <div className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <input
          type="date"
          className={`${INPUT_CLASS} w-auto`}
          value={fecha}
          onChange={(evento) => {
            setFecha(evento.target.value);
            setPagina(1);
          }}
        />
        <select
          className={`${INPUT_CLASS} w-auto`}
          value={veterinarioId}
          onChange={(evento) => {
            setVeterinarioId(evento.target.value);
            setPagina(1);
          }}
        >
          <option value="">Todos los veterinarios</option>
          {veterinarios.map((veterinario) => (
            <option key={veterinario.id} value={veterinario.id}>
              {veterinario.nombre}
            </option>
          ))}
        </select>
        <select
          className={`${INPUT_CLASS} w-auto`}
          value={mascotaId}
          onChange={(evento) => {
            setMascotaId(evento.target.value);
            setPagina(1);
          }}
        >
          <option value="">Todas las mascotas</option>
          {mascotas.map((mascota) => (
            <option key={mascota.id} value={mascota.id}>
              {mascota.nombre}
            </option>
          ))}
        </select>
        <select
          className={`${INPUT_CLASS} w-auto`}
          value={estado}
          onChange={(evento) => {
            setEstado(evento.target.value);
            setPagina(1);
          }}
        >
          <option value="">Todos los estados</option>
          {Object.values(EstadoCita).map((valor) => (
            <option key={valor} value={valor}>
              {valor}
            </option>
          ))}
        </select>
        {hayFiltrosActivos && (
          <button type="button" className={BUTTON_GHOST_CLASS} onClick={limpiarFiltros}>
            Limpiar filtros
          </button>
        )}
      </div>

      {error && <ErrorBanner mensaje={error} />}
      {cargando ? (
        <LoadingSpinner />
      ) : citas.length === 0 ? (
        <EmptyState titulo="No se encontraron citas" descripcion="Ajusta los filtros o agenda una nueva cita." />
      ) : (
        <Table>
          <TableHead>
            <tr>
              <Th>Código</Th>
              <Th>Mascota</Th>
              <Th>Veterinario</Th>
              <Th>Fecha y hora</Th>
              <Th>Tipo</Th>
              <Th>Valor</Th>
              <Th>Estado</Th>
              <Th>Acciones</Th>
            </tr>
          </TableHead>
          <TableBody>
            {citas.map((cita) => (
              <tr key={cita.id}>
                <Td>{cita.codigo}</Td>
                <Td>{nombreMascota(cita.mascota_id)}</Td>
                <Td>{nombreVeterinario(cita.veterinario_id)}</Td>
                <Td>{new Date(cita.fecha_hora).toLocaleString("es-CO")}</Td>
                <Td>{cita.tipo_consulta}</Td>
                <Td>${Number(cita.valor).toLocaleString("es-CO")}</Td>
                <Td>
                  <EstadoBadge estado={cita.estado} />
                </Td>
                <Td>
                  {cita.estado === EstadoCita.PROGRAMADA ? (
                    <div className="flex flex-wrap gap-2">
                      <button type="button" className={BUTTON_GHOST_CLASS} onClick={() => setCitaParaAtender(cita)}>
                        Atender
                      </button>
                      <button type="button" className={BUTTON_GHOST_CLASS} onClick={() => setCitaParaNoAsistio(cita)}>
                        No asistió
                      </button>
                      <button
                        type="button"
                        className={`${BUTTON_GHOST_CLASS} text-rose-600 hover:bg-rose-50`}
                        onClick={() => setCitaParaCancelar(cita)}
                      >
                        Cancelar
                      </button>
                    </div>
                  ) : (
                    <span className="text-xs text-slate-400">—</span>
                  )}
                </Td>
              </tr>
            ))}
          </TableBody>
        </Table>
      )}

      {(hayPaginaAnterior || hayPaginaSiguiente) && (
        <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3">
          <button
            type="button"
            className={BUTTON_SECONDARY_CLASS}
            disabled={!hayPaginaAnterior || cargando}
            onClick={() => setPagina((actual) => Math.max(1, actual - 1))}
          >
            Anterior
          </button>
          <span className="text-sm text-slate-500">Página {pagina}</span>
          <button
            type="button"
            className={BUTTON_SECONDARY_CLASS}
            disabled={!hayPaginaSiguiente || cargando}
            onClick={() => setPagina((actual) => actual + 1)}
          >
            Siguiente
          </button>
        </div>
      )}

      <ConfirmDialog
        abierto={Boolean(citaParaCancelar)}
        titulo="Cancelar cita"
        mensaje={`¿Confirmas cancelar la cita ${citaParaCancelar?.codigo}? Esta acción libera el bloque horario y notifica al tutor. Solo se permite con al menos dos horas de anticipación.`}
        etiquetaConfirmar="Sí, cancelar"
        cargando={procesando}
        onCancelar={() => setCitaParaCancelar(null)}
        onConfirmar={confirmarCancelacion}
      />

      <ConfirmDialog
        abierto={Boolean(citaParaNoAsistio)}
        titulo="Marcar inasistencia"
        mensaje={`¿Confirmas que la mascota no asistió a la cita ${citaParaNoAsistio?.codigo}?`}
        etiquetaConfirmar="Sí, marcar"
        cargando={procesando}
        onCancelar={() => setCitaParaNoAsistio(null)}
        onConfirmar={confirmarNoAsistio}
      />

      <Modal abierto={Boolean(citaParaAtender)} onCerrar={() => setCitaParaAtender(null)} titulo="Atender cita">
        <form className="flex flex-col gap-4" onSubmit={confirmarAtencion}>
          <FormField label="Observaciones">
            <textarea
              className={INPUT_CLASS}
              rows={4}
              value={observaciones}
              onChange={(evento) => setObservaciones(evento.target.value)}
              placeholder="Diagnóstico, tratamiento, recomendaciones..."
            />
          </FormField>
          <div className="flex justify-end gap-3">
            <button type="button" className={BUTTON_SECONDARY_CLASS} onClick={() => setCitaParaAtender(null)}>
              Cancelar
            </button>
            <button type="submit" className={BUTTON_PRIMARY_CLASS} disabled={procesando}>
              {procesando ? "Guardando..." : "Marcar como atendida"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
