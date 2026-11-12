import { NavLink } from "react-router-dom";

import { ENLACES_NAV } from "./navLinks";

export function Sidebar() {
  return (
    <aside className="hidden w-64 flex-col border-r border-slate-200 bg-white px-4 py-6 md:flex">
      <div className="mb-8 flex items-center gap-2 px-2">
        <span className="text-2xl">🐾</span>
        <span className="text-lg font-bold text-slate-900">Huellitas</span>
      </div>
      <nav className="flex flex-col gap-1">
        {ENLACES_NAV.map((enlace) => (
          <NavLink
            key={enlace.to}
            to={enlace.to}
            end={enlace.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive ? "bg-indigo-50 text-indigo-700" : "text-slate-600 hover:bg-slate-100"
              }`
            }
          >
            <span aria-hidden>{enlace.icono}</span>
            {enlace.etiqueta}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
