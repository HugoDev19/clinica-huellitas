import { createContext, type ReactNode, useCallback, useContext, useState } from "react";

type TipoToast = "exito" | "error";

interface ToastItem {
  id: number;
  mensaje: string;
  tipo: TipoToast;
}

interface ToastContextValue {
  notificarExito: (mensaje: string) => void;
  notificarError: (mensaje: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

let contadorToast = 0;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const quitar = useCallback((id: number) => {
    setToasts((anteriores) => anteriores.filter((toast) => toast.id !== id));
  }, []);

  const agregar = useCallback(
    (mensaje: string, tipo: TipoToast) => {
      const id = ++contadorToast;
      setToasts((anteriores) => [...anteriores, { id, mensaje, tipo }]);
      setTimeout(() => quitar(id), 5000);
    },
    [quitar],
  );

  const value: ToastContextValue = {
    notificarExito: (mensaje) => agregar(mensaje, "exito"),
    notificarError: (mensaje) => agregar(mensaje, "error"),
  };

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 flex w-80 flex-col gap-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            role="alert"
            className={`rounded-lg px-4 py-3 text-sm font-medium text-white shadow-lg ${
              toast.tipo === "exito" ? "bg-emerald-600" : "bg-rose-600"
            }`}
          >
            {toast.mensaje}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const contexto = useContext(ToastContext);
  if (!contexto) {
    throw new Error("useToast debe usarse dentro de ToastProvider");
  }
  return contexto;
}
