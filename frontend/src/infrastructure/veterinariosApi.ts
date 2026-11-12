import type { Veterinario } from "@/domain/types";

import { apiClient } from "./apiClient";

export interface CrearVeterinarioInput {
  codigo: string;
  nombre: string;
}

export const veterinariosApi = {
  async listar(): Promise<Veterinario[]> {
    const { data } = await apiClient.get<Veterinario[]>("/veterinarios/");
    return data;
  },
  async crear(input: CrearVeterinarioInput): Promise<Veterinario> {
    const { data } = await apiClient.post<Veterinario>("/veterinarios/", input);
    return data;
  },
};
