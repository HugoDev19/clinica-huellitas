import { useCallback, useEffect, useState } from "react";

import type { DashboardStats } from "@/domain/types";
import { citasApi } from "@/infrastructure/citasApi";
import { extraerMensajeError } from "@/infrastructure/apiClient";

export function useDashboard(fecha?: string) {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const recargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      setStats(await citasApi.dashboard(fecha));
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
  }, [fecha]);

  useEffect(() => {
    recargar();
  }, [recargar]);

  return { stats, cargando, error, recargar };
}
