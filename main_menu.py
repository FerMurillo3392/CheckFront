import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import asyncio
from playwright.async_api import async_playwright
import threading
import webbrowser

class ModuleDetailWindow:
    #Esta clase maneja la ventana de detalles de los módulos
    #que se muestran en el Treeview de la aplicación principal.
    #Permite ver detalles completos de cada módulo, incluyendo su JSON completo.
    def __init__(self, parent, modules):
        self.parent = parent
        self.modules = modules
        
        self.window = tk.Toplevel(parent)
        self.window.title("Detalle de Módulos")
        self.window.geometry("1000x600")
        
        # Crear Treeview para mostrar los módulos
        columns = ("index", "type", "id", "template", "show")
        self.tree = ttk.Treeview(
            self.window, 
            columns=columns, 
            show="headings",
            selectmode="extended"
        )
        
        # Configurar columnas
        self.tree.heading("index", text="#")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("id", text="ID")
        self.tree.heading("template", text="Template")
        self.tree.heading("show", text="Mostrar")
        
        self.tree.column("index", width=50)
        self.tree.column("type", width=150)
        self.tree.column("id", width=80)
        self.tree.column("template", width=250)
        self.tree.column("show", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.window, 
            orient=tk.VERTICAL, 
            command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Ver Detalles Completos",
            command=self.show_full_details
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Cerrar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Llenar el Treeview con los módulos
        self.populate_tree()
    
    def populate_tree(self):
        for idx, module in enumerate(self.modules):
            mod_type = module.get("type", "N/A")
            mod_id = module.get("id", "N/A") or "N/A"
            template = module.get("template", "N/A") or "N/A"
            show_info = module.get("show", {})
            show_str = ", ".join([k for k, v in show_info.items() if v]) or "N/A"
            #Esta funcuion llena el Treeview con los módulos
            #y muestra información relevante como tipo, ID, template y qué se debe mostrar.
            #Si el template es muy largo, se acorta para no saturar la vista.
            #El campo "show" muestra qué información se debe mostrar del módulo.
            self.tree.insert("", tk.END, values=(
                idx + 1,
                mod_type,
                str(mod_id),
                template[:50] + "..." if len(template) > 50 else template,
                show_str
            ))
    # Esta función muestra los detalles completos del módulo seleccionado
    # en una nueva ventana. Si no hay módulos seleccionados, muestra un mensaje de advertencia.
    # Si el índice del módulo es inválido, muestra un mensaje de error.
    # Si se selecciona un módulo, se muestra su JSON completo en una pestaña de la ventana de detalles.
    # También se muestra una vista previa con información clave del módulo.
    # Además, permite copiar el JSON al portapapeles.
    # La ventana de detalles incluye botones para copiar el JSON y cerrar la ventana.
    def show_full_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Información", "Seleccione un módulo para ver detalles")
            return
        
        # Tomar el primer ítem seleccionado
        first_selected = selected[0]
        values = self.tree.item(first_selected, "values")
        
        if values:
            try:
                # El índice en la lista es el valor mostrado - 1
                index = int(values[0]) - 1
                if 0 <= index < len(self.modules):
                    full_module = self.modules[index]
                    self.show_module_details(full_module)
                else:
                    messagebox.showerror("Error", "Índice de módulo inválido")
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Error al obtener los datos del módulo")
    
    def show_module_details(self, full_module):
        # Crear ventana de detalles
        detail_win = tk.Toplevel(self.window)
        detail_win.title(f"Detalles del Módulo")
        detail_win.geometry("800x600")
        
        # Notebook para organizar la información
        notebook = ttk.Notebook(detail_win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de datos JSON
        json_frame = ttk.Frame(notebook)
        notebook.add(json_frame, text="Datos JSON")
        
        text_area = scrolledtext.ScrolledText(json_frame, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        formatted_data = json.dumps(full_module, indent=4, ensure_ascii=False)
        text_area.insert(tk.INSERT, formatted_data)
        text_area.config(state=tk.DISABLED)
        
        # Pestaña de vista previa
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Vista Previa")
        
        # Mostrar información clave
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        #Muestra el titulo del módulo
        ttk.Label(info_frame, text="Tipo:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=full_module.get("type", "N/A")).grid(row=0, column=1, sticky=tk.W)
        #Muestra el ID del módulo
        ttk.Label(info_frame, text="ID:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=str(full_module.get("id", "N/A"))).grid(row=1, column=1, sticky=tk.W)
        #Muestra el template del módulo
        ttk.Label(info_frame, text="Template:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)
        title = full_module.get("template", "N/A") or "N/A"
        ttk.Label(info_frame, text=title, wraplength=600).grid(row=2, column=1, sticky=tk.W)

        # Botones de acción
        btn_frame = ttk.Frame(detail_win)
        btn_frame.pack(pady=10)
        
        # Botón para copiar JSON
        ttk.Button(
            btn_frame,
            text="Copiar JSON",
            command=lambda: self.copy_to_clipboard(formatted_data)
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón para cerrar
        ttk.Button(
            btn_frame,
            text="Cerrar",
            command=detail_win.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("Información", "JSON copiado al portapapeles")

class SiteTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de Sitios API")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Cargar configuración
        self.config = self.load_config()
        if not self.config:
            messagebox.showerror("Error", "No se pudo cargar sites_config.json")
            self.root.destroy()
            return
        
        # Crear interfaz
        self.create_widgets()
        
        # Estado de pruebas
        self.testing = False
        self.results = []
        
        # Enlazar evento de clic en el Treeview
        self.results_tree.bind('<ButtonRelease-1>', self.on_module_click)

    def load_config(self):
        try:
            with open('sites_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Archivo sites_config.json no encontrado")
            return None
        except json.JSONDecodeError:
            print("Error en formato JSON")
            return None

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Selección de sitio
        site_frame = ttk.LabelFrame(main_frame, text="Sitio a probar", padding=10)
        site_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(site_frame, text="Seleccione el sitio:").pack(side=tk.LEFT, padx=5)
        #Este es para el dorpdown de selección de sitios
        #Permite seleccionar el sitio a probar de la configuración cargada.
        #Se llena con los nombres de los sitios disponibles en el archivo de configuración.
        self.site_var = tk.StringVar()
        site_names = list(self.config.keys())
        self.site_dropdown = ttk.Combobox(
            site_frame, 
            textvariable=self.site_var,
            values=site_names,
            state="readonly",
            width=40
        )
        self.site_dropdown.pack(side=tk.LEFT, padx=5)
        self.site_dropdown.current(0)
        
        # Botón de prueba
        self.test_button = ttk.Button(
            site_frame, 
            text="Ejecutar Pruebas", 
            command=self.start_tests
        )
        self.test_button.pack(side=tk.RIGHT, padx=5)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Crear tabla con columna para módulos
        columns = ("name", "slug", "status", "type", "section", "modules", "modules_ok")
        self.results_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show="headings",
            selectmode="extended"
        )
        
        # Configurar columnas
        self.results_tree.heading("name", text="Nombre")
        self.results_tree.heading("slug", text="Slug")
        self.results_tree.heading("status", text="Código")
        self.results_tree.heading("type", text="Tipo")
        self.results_tree.heading("section", text="Sección")
        self.results_tree.heading("modules", text="Módulos")
        self.results_tree.heading("modules_ok", text="Existencia de modulos")
        
        self.results_tree.column("name", width=150, anchor=tk.W)
        self.results_tree.column("slug", width=200, anchor=tk.W)
        self.results_tree.column("status", width=80, anchor=tk.CENTER)
        self.results_tree.column("type", width=100, anchor=tk.W)
        self.results_tree.column("section", width=150, anchor=tk.W)
        self.results_tree.column("modules", width=80, anchor=tk.CENTER)
        self.results_tree.column("modules_ok", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            results_frame, 
            orient=tk.VERTICAL, 
            command=self.results_tree.yview
        )
        self.results_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Etiqueta de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Botón de exportación
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            export_frame, 
            text="Exportar Resultados", 
            command=self.export_results
        ).pack(side=tk.RIGHT)

    def start_tests(self):
        if self.testing:
            return
            
        selected_site = self.site_var.get()
        if not selected_site:
            messagebox.showwarning("Advertencia", "Seleccione un sitio primero")
            return
            
        # Limpiar resultados anteriores
        for item in self.results_tree.get_children():
            self.results_tree.delete(item) 
        self.testing = True
        self.test_button.config(state=tk.DISABLED)
        self.status_var.set(f"Probando: {selected_site}...")
        
        # Obtener configuración del sitio
        site_config = self.config.get(selected_site)
        if not site_config:
            messagebox.showerror("Error", f"Configuración no encontrada para {selected_site}")
            self.testing = False
            self.test_button.config(state=tk.NORMAL)
            return
        
        # Ejecutar pruebas en un hilo separado
        threading.Thread(
            target=self.run_tests_in_thread,
            args=(site_config,),
            daemon=True
        ).start()

    def run_tests_in_thread(self, site_config):
        #define un nuevo loop de eventos para asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.test_site(site_config))#lo corre hasta que termine
        loop.close()
        
        self.root.after(0, self.on_tests_complete)

    async def test_site(self, site_config):
        self.results = [] #inicializa la lista de resultados
        # Inicia Playwright y abre el navegador
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(site_config['base_url'])# Navega a la URL base del sitio
                
                for name, slug in site_config['slugs'].items():#entra en los slugs del sitio
                    # Construir la URL de la API
                    api_url = site_config['api_base'] + slug #forma la URL de la API
                    
                    try:
                        # Capturar respuesta de la API
                        async with page.expect_response(api_url) as response_info:
                            await page.goto(api_url)
                        
                        response = await response_info.value
                        status = response.status
                        
                        try:
                            api_data = await response.json()
                            # Obtener datos JSON y contar módulos
                            modules = api_data.get("data", {}).get("modules", [])
                            modules_count = len(modules)
                            modules_ok = "Existen Modulos" if modules_count > 0 else "No"
                            
                            filtered_data = {
                                "type": api_data.get("type"),
                                "section": api_data.get("data", {}).get("section"),
                            }
                            
                            # Guardar la lista completa de módulos
                            result = {
                                "name": name,
                                "slug": slug,
                                "status": status,
                                "type": filtered_data.get("type", "N/A"),
                                "section": filtered_data.get("section", "N/A"),
                                "modules": modules_count,
                                "modules_ok": modules_ok,
                                "modules_list": modules  # Guardamos la lista completa
                            }
                            
                            self.results.append(result)
                            self.update_results_table(result)
                            
                        except Exception as e:
                            print(f"Error procesando JSON en {name}: {e}")
                            result = {
                                "name": name,
                                "slug": slug,
                                "status": status,
                                "type": "N/A",
                                "section": "N/A",
                                "modules": 0,
                                "modules_ok": "ERROR",
                                "modules_list": []
                            }
                            self.results.append(result)
                            self.update_results_table(result)
                    
                    except Exception as e:
                        print(f"Error en {name}: {e}")
                        result = {
                            "name": name,
                            "slug": slug,
                            "status": "ERROR",
                            "type": "N/A",
                            "section": "N/A",
                            "modules": 0,
                            "modules_ok": "ERROR",
                            "modules_list": []
                        }
                        self.results.append(result)
                        self.update_results_table(result)
            
            except Exception as e:
                print(f"Error general: {e}")
                messagebox.showwarning("Advertencia", "No se pudo acceder a la URL base del sitio. Pruebe encendiendo el stage o con otro sitio.")
            finally:
                await browser.close()

    def update_results_table(self, result):
        self.root.after(0, lambda: self._update_table(result))

    def _update_table(self, result):
        # Determinar color según el estado
        if result["status"] == 200:
            tags = ("success",)
        elif isinstance(result["status"], int) and result["status"] >= 400:
            tags = ("error",)
        else:
            tags = ("warning",)
        
        # Determinar color para módulos
        if result["modules_ok"] == "Existen Modulos":
            module_tags = ("module_success",)
        else:
            module_tags = ("module_error",)
        
        # Insertar en la tabla
        item_id = self.results_tree.insert(
            "", 
            tk.END, 
            values=(
                result["name"],
                result["slug"],
                result["status"],
                result["type"],
                result["section"],
                result["modules"],
                result["modules_ok"]
            ),
            tags=tags
        )
        
        # Aplicar formato de color
        self.results_tree.tag_configure("success", foreground="green")
        self.results_tree.tag_configure("error", foreground="red")
        self.results_tree.tag_configure("warning", foreground="orange")
        
        # Aplicar formato especial para la columna de módulos
        self.results_tree.tag_configure("module_success", foreground="green")
        self.results_tree.tag_configure("module_error", foreground="red")

    def on_tests_complete(self):
        self.testing = False
        self.test_button.config(state=tk.NORMAL)
        
        success_count = sum(1 for r in self.results if r["status"] == 200)
        error_count = sum(1 for r in self.results if r["status"] != 200)
        modules_ok_count = sum(1 for r in self.results if r.get("modules_ok") == "Existen Modulos")
        
        self.status_var.set(
            f"Pruebas completadas: {success_count} éxitos, {error_count} errores | "
            f"Módulos OK: {modules_ok_count}/{len(self.results)}"
        )
    #esta función exporta los resultados a un archivo JSON
    #Si no hay resultados, muestra un mensaje informativo.
    #Si hay un error al exportar, muestra un mensaje de error.
    #Si la exportación es exitosa, muestra un mensaje de éxito.
    def export_results(self):
        if not self.results:
            messagebox.showinfo("Exportar", "No hay resultados para exportar")
            return
            
        try:
            with open('test_results.json', 'w') as f:
                json.dump(self.results, f, indent=2)
            messagebox.showinfo("Éxito", "Resultados exportados a test_results.json")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")
    # Esta función maneja el evento de clic en la columna de módulos
    # del Treeview. Si se hace clic en un módulo, abre una ventana
    # de detalles mostrando la lista de módulos asociados al slug.
    # Si no hay módulos, muestra un mensaje informativo.
    # Si se hace clic en una celda que no es la de módulos, no hace nada.
    # Si se hace clic en la columna de módulos, busca el slug correspondiente
    # y muestra los detalles de los módulos en una nueva ventana.
    # Si no se encuentran módulos, muestra un mensaje informativo.
    # Si hay un error al buscar los módulos, muestra un mensaje de error.
    # Si se hace clic en una celda que no es la de módulos, no hace nada.
    # Si se hace clic en la columna de módulos, busca el slug correspondiente
    def on_module_click(self, event):
        # Identificar la región clickeada
        region = self.results_tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        # Obtener columna y item clickeado
        column = self.results_tree.identify_column(event.x)
        item_id = self.results_tree.identify_row(event.y)
        
        # Solo procesar clics en la columna de módulos (columna #6)
        if column == "#6":
            # Obtener los valores del item
            item_values = self.results_tree.item(item_id, "values")
            slug = item_values[1]
            modules_count = item_values[5]
            
            if modules_count == 0:
                messagebox.showinfo("Información", "Este slug no tiene módulos")
                return
            
            # Buscar los módulos en los resultados
            for result in self.results:
                if result['slug'] == slug:
                    modules = result.get('modules_list', [])
                    if modules:
                        ModuleDetailWindow(self.root, modules)
                    else:
                        messagebox.showinfo("Información", "No se encontraron detalles de módulos")
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = SiteTesterApp(root)
    root.mainloop()