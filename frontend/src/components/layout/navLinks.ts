export interface EnlaceNav {
  to: string;
  etiqueta: string;
  icono: string;
}

export const ENLACES_NAV: EnlaceNav[] = [
  { to: "/", etiqueta: "Dashboard", icono: "🏠" },
  { to: "/citas", etiqueta: "Historial de citas", icono: "📋" },
  { to: "/citas/agendar", etiqueta: "Agendar cita", icono: "➕" },
  { to: "/agenda", etiqueta: "Agenda diaria", icono: "🗓️" },
  { to: "/tutores", etiqueta: "Tutores", icono: "🧑" },
  { to: "/mascotas", etiqueta: "Mascotas", icono: "🐾" },
  { to: "/veterinarios", etiqueta: "Veterinarios", icono: "🩺" },
];
