import { Route, Routes } from "react-router-dom";

import { Layout } from "@/components/layout/Layout";
import { AgendaDiariaPage } from "@/features/citas/AgendaDiariaPage";
import { AgendarCitaPage } from "@/features/citas/AgendarCitaPage";
import { CitasPage } from "@/features/citas/CitasPage";
import { DashboardPage } from "@/features/dashboard/DashboardPage";
import { MascotasPage } from "@/features/mascotas/MascotasPage";
import { TutoresPage } from "@/features/tutores/TutoresPage";
import { VeterinariosPage } from "@/features/veterinarios/VeterinariosPage";

function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-20 text-center">
      <p className="text-3xl font-bold text-slate-900">404</p>
      <p className="text-sm text-slate-500">La página que buscas no existe.</p>
    </div>
  );
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="citas" element={<CitasPage />} />
        <Route path="citas/agendar" element={<AgendarCitaPage />} />
        <Route path="agenda" element={<AgendaDiariaPage />} />
        <Route path="tutores" element={<TutoresPage />} />
        <Route path="mascotas" element={<MascotasPage />} />
        <Route path="veterinarios" element={<VeterinariosPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
