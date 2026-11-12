import { useCallback, useEffect, useState } from "react";

import type { Mascota } from "@/domain/types";
import { extraerMensajeError } from "@/infrastructure/apiClient";
import { mascotasApi, type RegistrarMascotaInput } from "@/infrastructure/mascotasApi";

export function useMascotas(tutorId?: number) {
  const [mascotas, setMascotas] = useState<Mascota[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const recargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      setMascotas(await mascotasApi.listar(tutorId));
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
  }, [tutorId]);

  useEffect(() => {
    recargar();
  }, [recargar]);

  const registrar = useCallback(async (input: RegistrarMascotaInput) => {
    const mascota = await mascotasApi.crear(input);
    setMascotas((anteriores) => [...anteriores, mascota]);
    return mascota;
  }, []);

  const actualizar = useCallback(async (id: number, input: RegistrarMascotaInput) => {
    const mascota = await mascotasApi.actualizar(id, input);
    setMascotas((anteriores) => anteriores.map((actual) => (actual.id === id ? mascota : actual)));
    return mascota;
  }, []);

  const eliminar = useCallback(async (id: number) => {
    await mascotasApi.eliminar(id);
    setMascotas((anteriores) => anteriores.filter((mascota) => mascota.id !== id));
  }, []);

  return { mascotas, cargando, error, recargar, registrar, actualizar, eliminar };
}
