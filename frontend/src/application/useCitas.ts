import { useCallback, useEffect, useState } from "react";

import type { Cita } from "@/domain/types";
import { citasApi, type FiltrosCitas } from "@/infrastructure/citasApi";
import { extraerMensajeError } from "@/infrastructure/apiClient";

export function useCitas(filtros: FiltrosCitas) {
  const [citas, setCitas] = useState<Cita[]>([]);
  const [total, setTotal] = useState(0);
  const [hayPaginaAnterior, setHayPaginaAnterior] = useState(false);
  const [hayPaginaSiguiente, setHayPaginaSiguiente] = useState(false);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const clave = JSON.stringify(filtros);

  const recargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const pagina = await citasApi.listar(filtros);
      setCitas(pagina.results);
      setTotal(pagina.count);
      setHayPaginaAnterior(Boolean(pagina.previous));
      setHayPaginaSiguiente(Boolean(pagina.next));
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
    // clave representa el contenido serializado de filtros; se usa como dependencia estable
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clave]);

  useEffect(() => {
    recargar();
  }, [recargar]);

  const actualizarCitaLocal = useCallback((cita: Cita) => {
    setCitas((anteriores) => anteriores.map((c) => (c.id === cita.id ? cita : c)));
  }, []);

  const cancelar = useCallback(
    async (id: number) => {
      const actualizada = await citasApi.cancelar(id);
      actualizarCitaLocal(actualizada);
      return actualizada;
    },
    [actualizarCitaLocal],
  );

  const atender = useCallback(
    async (id: number, observaciones: string) => {
      const actualizada = await citasApi.atender(id, observaciones);
      actualizarCitaLocal(actualizada);
      return actualizada;
    },
    [actualizarCitaLocal],
  );

  const marcarNoAsistio = useCallback(
    async (id: number) => {
      const actualizada = await citasApi.marcarNoAsistio(id);
      actualizarCitaLocal(actualizada);
      return actualizada;
    },
    [actualizarCitaLocal],
  );

  return {
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
  };
}
