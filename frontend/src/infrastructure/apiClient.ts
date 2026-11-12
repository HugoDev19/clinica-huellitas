import axios from "axios";
import type { Paginado } from "@/domain/types";

export const apiClient = axios.create({
    baseURL: import.meta.env.PROD ? "/api" : (import.meta.env.VITE_API_BASE_URL ?? "/api"),
  headers: { "Content-Type": "application/json" },
});

export async function listarTodasLasPaginas<T>(
  ruta: string,
  params: Record<string, string | number> = {},
): Promise<T[]> {
  const resultados: T[] = [];
  let pagina = 1;

  while (true) {
    const { data } = await apiClient.get<Paginado<T>>(ruta, {
      params: { ...params, page: pagina },
    });
    resultados.push(...data.results);

    if (!data.next) return resultados;

    const siguiente = new URL(data.next, "http://api.local").searchParams.get("page");
    if (!siguiente || Number(siguiente) <= pagina) return resultados;
    pagina = Number(siguiente);
  }
}

interface ErrorApi {
  error: string;
  detalle: string;
}

export function extraerMensajeError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as (ErrorApi & { detail?: string }) | undefined;
    if (data?.detalle) return data.detalle;
    if (data?.detail) return data.detail;
    if (data && typeof data === "object") {
      const primerError = Object.values(data).flat().find((valor) => typeof valor === "string");
      if (primerError) return primerError;
    }
    if (error.response?.status === 404) return "No se encontró el recurso solicitado.";
    if (!error.response) return "No se pudo conectar con el servidor. Verifica que el backend esté iniciado.";
  }
  return "Ocurrió un error inesperado. Intenta nuevamente.";
}
