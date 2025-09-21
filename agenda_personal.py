import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
from tkcalendar import DateEntry


class AgendaApp(tk.Tk):
    """Ventana principal de la aplicación."""
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("700x450")
        self.resizable(False, False)

        # Lista interna de eventos (puede usarse para persistencia futura)
        # Cada evento será un diccionario: {"fecha": str, "hora": str, "desc": str}
        self.eventos = []

        # Configurar la interfaz
        self._create_widgets()

    def _create_widgets(self):
        """Crear y organizar widgets usando Frames."""
        # Frame superior: Treeview (visualización de eventos)
        frame_lista = ttk.Frame(self, padding=(10, 10))
        frame_lista.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        lbl_titulo = ttk.Label(frame_lista, text="Eventos Programados", font=(None, 12, 'bold'))
        lbl_titulo.pack(anchor=tk.W)

        # Treeview con 3 columnas: Fecha, Hora, Descripcion
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame_lista, columns=columns, show='headings', height=10)
        self.tree.heading('fecha', text='Fecha')
        self.tree.heading('hora', text='Hora')
        self.tree.heading('descripcion', text='Descripción')
        self.tree.column('fecha', width=120, anchor=tk.CENTER)
        self.tree.column('hora', width=80, anchor=tk.CENTER)
        self.tree.column('descripcion', width=420, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Frame medio: Entradas para agregar evento
        frame_entradas = ttk.Frame(self, padding=(10, 10))
        frame_entradas.pack(side=tk.TOP, fill=tk.X)

        # Subframe para Fecha y Hora
        frame_fecha_hora = ttk.Frame(frame_entradas)
        frame_fecha_hora.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Etiqueta y DatePicker / Combobox
        lbl_fecha = ttk.Label(frame_fecha_hora, text='Fecha:')
        lbl_fecha.grid(row=0, column=0, padx=(0, 6), pady=4, sticky=tk.W)

        self.date_entry = DateEntry(frame_fecha_hora, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=(0, 12), pady=4, sticky=tk.W)

        # Hora
        lbl_hora = ttk.Label(frame_fecha_hora, text='Hora (HH:MM):')
        lbl_hora.grid(row=1, column=0, padx=(0, 6), pady=4, sticky=tk.W)
        self.entry_hora = ttk.Entry(frame_fecha_hora, width=10)
        self.entry_hora.insert(0, '09:00')
        self.entry_hora.grid(row=1, column=1, padx=(0, 12), pady=4, sticky=tk.W)

        # Subframe para Descripción
        frame_desc = ttk.Frame(frame_entradas)
        frame_desc.pack(side=tk.LEFT, fill=tk.X, expand=True)

        lbl_desc = ttk.Label(frame_desc, text='Descripción:')
        lbl_desc.grid(row=0, column=0, padx=(0, 6), pady=4, sticky=tk.W)
        self.entry_desc = ttk.Entry(frame_desc, width=50)
        self.entry_desc.grid(row=0, column=1, padx=(0, 6), pady=4, sticky=tk.W)

        # Frame inferior: Botones de acción
        frame_acciones = ttk.Frame(self, padding=(10, 10))
        frame_acciones.pack(side=tk.BOTTOM, fill=tk.X)

        btn_agregar = ttk.Button(frame_acciones, text='Agregar Evento', command=self.agregar_evento)
        btn_eliminar = ttk.Button(frame_acciones, text='Eliminar Evento Seleccionado', command=self.eliminar_evento)
        btn_salir = ttk.Button(frame_acciones, text='Salir', command=self.quit)

        btn_agregar.pack(side=tk.LEFT, padx=(0, 6))
        btn_eliminar.pack(side=tk.LEFT, padx=(6, 6))
        btn_salir.pack(side=tk.RIGHT)

    def _leer_fecha(self):
        """Leer la fecha desde DateEntry."""
        fecha = self.date_entry.get_date()
        return fecha.strftime('%Y-%m-%d')

    def agregar_evento(self):
        """Acción para agregar un nuevo evento a la lista y al Treeview."""
        fecha = self._leer_fecha()
        hora = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        # Validaciones básicas
        if not fecha:
            messagebox.showerror('Error', 'La fecha no es válida. Verifique el formato.')
            return
        if not self._validar_hora(hora):
            messagebox.showerror('Error', 'Hora inválida. Use el formato HH:MM (24 horas).')
            return
        if not desc:
            messagebox.showerror('Error', 'La descripción no puede estar vacía.')
            return

        evento = {'fecha': fecha, 'hora': hora, 'desc': desc}
        self.eventos.append(evento)

        # Insertar en el Treeview
        self.tree.insert('', tk.END, values=(fecha, hora, desc))

        # Limpiar campos (opcional)
        self.entry_desc.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, '09:00')

    def eliminar_evento(self):
        """Eliminar el evento seleccionado en el Treeview (con confirmación)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Eliminar', 'Seleccione un evento de la lista para eliminar.')
            return

        # Pedir confirmación
        confirm = messagebox.askyesno('Confirmar eliminación', '¿Seguro que desea eliminar el/los evento(s) seleccionado(s)?')
        if not confirm:
            return

        # Eliminar del Treeview y de la lista interna
        for item in selected:
            vals = self.tree.item(item, 'values')
            # Buscar y eliminar la primera coincidencia en self.eventos
            for ev in self.eventos:
                if (ev['fecha'], ev['hora'], ev['desc']) == (vals[0], vals[1], vals[2]):
                    self.eventos.remove(ev)
                    break
            self.tree.delete(item)

    @staticmethod
    def _validar_hora(hora_str):
        """Validar que la hora esté en formato HH:MM y sea una hora válida (24h)."""
        try:
            partes = hora_str.split(':')
            if len(partes) != 2:
                return False
            h = int(partes[0])
            m = int(partes[1])
            return 0 <= h <= 23 and 0 <= m <= 59
        except Exception:
            return False


if __name__ == '__main__':
    app = AgendaApp()
    app.mainloop()
