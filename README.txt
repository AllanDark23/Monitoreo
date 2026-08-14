DASHBOARD CMT  — DEMO
==========================
Contenido:
  index.html        -> Panel principal + Tomzin (analista IA)
  incidencias.html  -> Galeria de evidencias por caso (fotos incrustadas)
  evidencias/       -> Fotos como archivos, nomenclatura INC-AAAAMM-####_##.jpg
  servidor_ia.py    -> OPCIONAL: conecta Tomzin a la API de Claude (ver dentro)
  bitacora_con_ids.csv, data.json -> datos fuente

Uso: abrir index.html en Chrome/Edge. Funciona sin instalar nada.
El boton de tema (Claro/Oscuro) se recuerda entre paginas y entre sesiones.

TOM: responde con un motor analitico local que calcula sobre los datos
visibles y respeta los filtros aplicados. Entiende preguntas abiertas,
nombres de unidades (ej. "contame de C425") y CEDIs (ej. "que pasa en Monca").
