import type { EstadoCita, TipoConsulta } from "./enums";

export interface Tutor {
  id: number;
  nombre: string;
  documento: string;
  telefono: string;
  correo: string;
}

export interface Mascota {
  id: number;
  nombre: string;
  especie: string;
  edad_anios: number;
  tutor_id: number;
}

export interface Veterinario {
  id: number;
  codigo: string;
  nombre: string;
  disponible: boolean;
}

export interface Cita {
  id: number;
  codigo: string;
  mascota_id: number;
  veterinario_id: number;
  fecha_hora: string;
  tipo_consulta: TipoConsulta;
  valor: string;
  estado: EstadoCita;
  observaciones: string;
  creado_en: string;
}

export interface Paginado<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface DistribucionVeterinario {
  veterinario_id: number;
  total: number;
}

export interface DashboardStats {
  fecha: string;
  total_citas: number;
  programadas: number;
  atendidas: number;
  canceladas: number;
  no_asistio: number;
  proximas_citas: Cita[];
  distribucion_por_veterinario: DistribucionVeterinario[];
}
