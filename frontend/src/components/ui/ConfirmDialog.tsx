import { BUTTON_DANGER_CLASS, BUTTON_SECONDARY_CLASS } from "./classNames";
import { Modal } from "./Modal";

interface ConfirmDialogProps {
  abierto: boolean;
  titulo: string;
  mensaje: string;
  etiquetaConfirmar?: string;
  cargando?: boolean;
  onCancelar: () => void;
  onConfirmar: () => void;
}

export function ConfirmDialog({
  abierto,
  titulo,
  mensaje,
  etiquetaConfirmar = "Confirmar",
  cargando = false,
  onCancelar,
  onConfirmar,
}: ConfirmDialogProps) {
  return (
    <Modal abierto={abierto} onCerrar={onCancelar} titulo={titulo}>
      <p className="text-sm text-slate-600">{mensaje}</p>
      <div className="mt-6 flex justify-end gap-3">
        <button type="button" className={BUTTON_SECONDARY_CLASS} onClick={onCancelar}>
          Cancelar
        </button>
        <button type="button" className={BUTTON_DANGER_CLASS} disabled={cargando} onClick={onConfirmar}>
          {cargando ? "Procesando..." : etiquetaConfirmar}
        </button>
      </div>
    </Modal>
  );
}
