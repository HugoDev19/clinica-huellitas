import { useState } from "react";
import { NavLink } from "react-router-dom";

import { ENLACES_NAV } from "./navLinks";

export function Topbar() {
  const [abierto, setAbierto] = useState(false);

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white">
      <div className="flex items-center justify-between px-4 py-3 md:px-6">
        <button
          type="button"
          className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 md:hidden"
          onClick={() => setAbierto((valor) => !valor)}
          aria-label="Abrir menú de navegación"
        >
          ☰
        </button>
        <div className="flex items-center gap-2 md:hidden">
          <span className="text-xl">🐾</span>
          <span className="font-bold text-slate-900">Huellitas</span>
        </div>
        <p className="hidden text-sm text-slate-500 md:block">Panel administrativo</p>
        <div className="flex items-center gap-3">
          <span className="hidden text-sm text-slate-600 md:inline">Clínica Veterinaria</span>
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-600 text-sm font-semibold text-white">
            H
          </div>
        </div>
      </div>
      {abierto && (
        <nav className="flex flex-col gap-1 border-t border-slate-200 bg-white p-2 md:hidden">
          {ENLACES_NAV.map((enlace) => (
            <NavLink
              key={enlace.to}
              to={enlace.to}
              end={enlace.to === "/"}
              onClick={() => setAbierto(false)}
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm font-medium ${
                  isActive ? "bg-indigo-50 text-indigo-700" : "text-slate-600 hover:bg-slate-100"
                }`
              }
            >
              {enlace.icono} {enlace.etiqueta}
            </NavLink>
          ))}
        </nav>
      )}
    </header>
  );
}
