import { useCallback, useEffect, useState } from "react";

import type { Veterinario } from "@/domain/types";
import { extraerMensajeError } from "@/infrastructure/apiClient";
import { type CrearVeterinarioInput, veterinariosApi } from "@/infrastructure/veterinariosApi";

export function useVeterinarios() {
  const [veterinarios, setVeterinarios] = useState<Veterinario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const recargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      setVeterinarios(await veterinariosApi.listar());
    } catch (err) {
      setError(extraerMensajeError(err));
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    recargar();
  }, [recargar]);

  const registrar = useCallback(async (input: CrearVeterinarioInput) => {
    const veterinario = await veterinariosApi.crear(input);
    setVeterinarios((anteriores) =>
      [...anteriores, veterinario].sort((a, b) => a.codigo.localeCompare(b.codigo)),
    );
    return veterinario;
  }, []);

  return { veterinarios, cargando, error, recargar, registrar };
}
