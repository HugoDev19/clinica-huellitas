import type { Veterinario } from "@/domain/types";

import { apiClient } from "./apiClient";

export const veterinariosApi = {
  async listar(): Promise<Veterinario[]> {
    const { data } = await apiClient.get<Veterinario[]>("/veterinarios/");
    return data;
  },
};
