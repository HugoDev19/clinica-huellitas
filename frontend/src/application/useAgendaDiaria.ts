import { useCallback, useEffect, useState } from "react";

import type { Cita } from "@/domain/types";
import { citasApi } from "@/infrastructure/citasApi";
import { extraerMensajeError } from "@/infrastructure/apiClient";

export function useAgendaDiaria(veterinarioId: number | null, fecha: string) {
  const [citas, setCitas] = useState<Cita[]>([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const recargar = useCallback(async () => {
    if (!veterinarioId || !fecha) {
      setCitas([]);
      return;
    }
    setCargando(true);
    setError(null);
    try {
      setCitas(await citasApi.agendaDiaria(veterinarioId, fecha));
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
  }, [veterinarioId, fecha]);

  useEffect(() => {
    recargar();
  }, [recargar]);

  return { citas, cargando, error, recargar };
}
