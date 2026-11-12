import type { Cita, DashboardStats, Paginado } from "@/domain/types";
import type { TipoConsulta } from "@/domain/enums";

import { apiClient } from "./apiClient";

export interface AgendarCitaInput {
  mascota_id: number;
  veterinario_id: number;
  fecha_hora: string;
  tipo_consulta: TipoConsulta;
  observaciones?: string;
}

export interface FiltrosCitas {
  fecha?: string;
  veterinario_id?: number;
  mascota_id?: number;
  estado?: string;
  page?: number;
}

export const citasApi = {
  async listar(filtros: FiltrosCitas = {}): Promise<Paginado<Cita>> {
    const { data } = await apiClient.get<Paginado<Cita>>("/citas/", { params: filtros });
    return data;
  },
  async obtener(id: number): Promise<Cita> {
    const { data } = await apiClient.get<Cita>(`/citas/${id}/`);
    return data;
  },
  async agendar(input: AgendarCitaInput): Promise<Cita> {
    const { data } = await apiClient.post<Cita>("/citas/", input);
    return data;
  },
  async agendaDiaria(veterinarioId: number, fecha: string): Promise<Cita[]> {
    const { data } = await apiClient.get<Cita[]>("/citas/agenda/", {
      params: { veterinario_id: veterinarioId, fecha },
    });
    return data;
  },
  async cancelar(id: number): Promise<Cita> {
    const { data } = await apiClient.post<Cita>(`/citas/${id}/cancelar/`);
    return data;
  },
  async atender(id: number, observaciones: string): Promise<Cita> {
    const { data } = await apiClient.post<Cita>(`/citas/${id}/atender/`, { observaciones });
    return data;
  },
  async marcarNoAsistio(id: number): Promise<Cita> {
    const { data } = await apiClient.post<Cita>(`/citas/${id}/no-asistio/`);
    return data;
  },
  async dashboard(fecha?: string): Promise<DashboardStats> {
    const { data } = await apiClient.get<DashboardStats>("/citas/dashboard/", {
      params: fecha ? { fecha } : undefined,
    });
    return data;
  },
};
