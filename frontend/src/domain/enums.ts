export enum TipoConsulta {
  GENERAL = "GENERAL",
  VACUNACION = "VACUNACION",
  CONTROL = "CONTROL",
}

export enum EstadoCita {
  PROGRAMADA = "PROGRAMADA",
  ATENDIDA = "ATENDIDA",
  CANCELADA = "CANCELADA",
  NO_ASISTIO = "NO_ASISTIO",
}

export const ETIQUETAS_TIPO_CONSULTA: Record<TipoConsulta, string> = {
  [TipoConsulta.GENERAL]: "General",
  [TipoConsulta.VACUNACION]: "Vacunación",
  [TipoConsulta.CONTROL]: "Control",
};

export const ETIQUETAS_ESTADO_CITA: Record<EstadoCita, string> = {
  [EstadoCita.PROGRAMADA]: "Programada",
  [EstadoCita.ATENDIDA]: "Atendida",
  [EstadoCita.CANCELADA]: "Cancelada",
  [EstadoCita.NO_ASISTIO]: "No asistió",
};
