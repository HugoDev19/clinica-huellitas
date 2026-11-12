import type { Tutor } from "@/domain/types";

import { apiClient, listarTodasLasPaginas } from "./apiClient";

export interface RegistrarTutorInput {
  nombre: string;
  documento: string;
  telefono: string;
  correo: string;
}

export const tutoresApi = {
  async listar(): Promise<Tutor[]> {
    return listarTodasLasPaginas<Tutor>("/tutores/");
  },
  async crear(input: RegistrarTutorInput): Promise<Tutor> {
    const { data } = await apiClient.post<Tutor>("/tutores/", input);
    return data;
  },
};
