from buscador import buscador, palabras_cercanas, fecha_cercana_despido, salario, indemnizacion_despido_completa, antiguedad, abrirpdf, preparar_texto

pdfname = "147.20.pdf"
my_outfile = ".".join(pdfname.split('.')[:-1]) + '.txt'

document = abrirpdf(pdfname)
textdef = preparar_texto(document)



salario = salario(textdef)
efectos = buscador(textdef, "efectos")
despido = palabras_cercanas(textdef, "despido", *efectos)
fecha_despido = fecha_cercana_despido(textdef, despido)
indemnizacion = indemnizacion_despido_completa(textdef)
antiguedad = antiguedad(textdef)

print(salario, antiguedad, fecha_despido, indemnizacion)
