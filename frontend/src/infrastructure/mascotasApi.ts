import type { Mascota } from "@/domain/types";

import { apiClient, listarTodasLasPaginas } from "./apiClient";

export interface RegistrarMascotaInput {
  nombre: string;
  especie: string;
  edad_anios: number;
  tutor_id: number;
}

export const mascotasApi = {
  async listar(tutorId?: number): Promise<Mascota[]> {
    return listarTodasLasPaginas<Mascota>(
      "/mascotas/",
      tutorId ? { tutor_id: tutorId } : {},
    );
  },
  async obtener(id: number): Promise<Mascota> {
    const { data } = await apiClient.get<Mascota>(`/mascotas/${id}/`);
    return data;
  },
  async crear(input: RegistrarMascotaInput): Promise<Mascota> {
    const { data } = await apiClient.post<Mascota>("/mascotas/", input);
    return data;
  },
  async actualizar(id: number, input: RegistrarMascotaInput): Promise<Mascota> {
    const { data } = await apiClient.put<Mascota>(`/mascotas/${id}/`, input);
    return data;
  },
  async eliminar(id: number): Promise<void> {
    await apiClient.delete(`/mascotas/${id}/`);
  },
};
