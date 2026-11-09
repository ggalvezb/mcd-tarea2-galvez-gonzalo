# 💻 Tutorial de Instalación y Uso Básico de Visual Studio Code (VS Code)

## 🏁 Introducción

**Visual Studio Code (VS Code)** es un editor de código fuente gratuito y de código abierto desarrollado por **Microsoft**.  
Está disponible para Windows, macOS y Linux, y cuenta con soporte para múltiples lenguajes de programación, extensiones, depuración y control de versiones.

---

## 📥 1. Instalación de VS Code

### 🔹 Paso 1: Descargar

Visita la página oficial:  
👉 [https://code.visualstudio.com/](https://code.visualstudio.com/)

Haz clic en el botón **Download for Windows**, **macOS**, o **Linux** según tu sistema operativo.

### 🔹 Paso 2: Instalar

1. Abre el instalador descargado.  
2. Acepta los términos de la licencia.  
3. Se recomienda marcar las siguientes opciones:
   - **Agregar al PATH** (permite usar el comando `code` desde la terminal).
   - **Registrar VS Code como editor predeterminado**.  
4. Completa la instalación haciendo clic en **Install**.

---

## 🚀 2. Primer inicio y configuración

1. Abre **Visual Studio Code**.  
2. Verás la pantalla de bienvenida donde podrás:
   - Abrir una carpeta o archivo.
   - Instalar extensiones.
   - Personalizar el tema visual.  

### 💡 Consejo
Puedes cambiar el idioma a español:
- Abre la paleta de comandos con `Ctrl + Shift + P` (Windows/Linux) o `Cmd + Shift + P` (macOS).
- Escribe **“Configure Display Language”**.  
- Selecciona **Español (Spanish)**.

---

## 📂 3. Abrir archivos o carpetas en VS Code

### 🔹 Opción A: Desde el menú

- Ve a **File → Open File...** para abrir un archivo individual.  
- O selecciona **File → Open Folder...** para abrir una carpeta completa como proyecto.

### 🔹 Opción B: Arrastrar y soltar

Simplemente arrastra un archivo o carpeta desde tu explorador del sistema hacia la ventana de VS Code.

### 🔹 Opción C: Desde la terminal

Si marcaste la opción de “Agregar al PATH” durante la instalación, puedes abrir archivos y carpetas desde la terminal con el comando:

```bash
# Abrir VS Code
code

# Abrir una carpeta específica
code nombre_de_carpeta/

# Abrir un archivo específico
code archivo.py

# Abrir la carpeta actual
code .
```

👉 El comando `code .` es muy útil para abrir el proyecto actual directamente en VS Code.

---

## 🔧 4. Ejemplo práctico

Supongamos que tienes una carpeta llamada `mi_proyecto` con los siguientes archivos:

```
mi_proyecto/
├── app.py
├── README.md
└── data/
    └── datos.csv
```

### ✅ Abrir todo el proyecto

```bash
cd ruta/donde/esta/mi_proyecto
code .
```

Esto abrirá toda la carpeta en VS Code, mostrando el contenido en el panel lateral.

### ✅ Abrir un archivo específico

```bash
code mi_proyecto/app.py
```

VS Code abrirá directamente el archivo `app.py` listo para editar.

---

## 🧩 5. Instalación de extensiones recomendadas

Desde la barra lateral izquierda, haz clic en el ícono de **Extensiones** (o presiona `Ctrl + Shift + X`).

Algunas extensiones útiles son:

| Extensión | Descripción |
|------------|--------------|
| **Python** | Soporte para ejecutar y depurar código Python. |
| **Prettier** | Formateador de código automático. |
| **GitLens** | Herramientas avanzadas para Git y GitHub. |
| **Live Server** | Permite previsualizar proyectos web en tiempo real. |

---

## 🧠 6. Atajos de teclado útiles

| Acción | Windows/Linux | macOS |
|--------|----------------|--------|
| Abrir paleta de comandos | `Ctrl + Shift + P` | `Cmd + Shift + P` |
| Abrir archivo | `Ctrl + O` | `Cmd + O` |
| Guardar archivo | `Ctrl + S` | `Cmd + S` |
| Buscar texto | `Ctrl + F` | `Cmd + F` |
| Abrir terminal integrada | `Ctrl + Ñ` o `Ctrl + \`` | `Cmd + \`` |
| Comentario de línea | `Ctrl + /` | `Cmd + /` |


---

## 📘 Referencias

- [Documentación oficial de VS Code](https://code.visualstudio.com/docs)
- [Guía de comandos `code`](https://code.visualstudio.com/docs/editor/command-line)
