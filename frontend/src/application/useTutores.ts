import { useCallback, useEffect, useState } from "react";

import type { Tutor } from "@/domain/types";
import { extraerMensajeError } from "@/infrastructure/apiClient";
import { type RegistrarTutorInput, tutoresApi } from "@/infrastructure/tutoresApi";

export function useTutores() {
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const recargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      setTutores(await tutoresApi.listar());
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    recargar();
  }, [recargar]);

  const registrar = useCallback(async (input: RegistrarTutorInput) => {
    const tutor = await tutoresApi.crear(input);
    setTutores((anteriores) => [...anteriores, tutor]);
    return tutor;
  }, []);

  return { tutores, cargando, error, recargar, registrar };
}
