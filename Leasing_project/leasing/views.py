from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Prestamo, Empresa
from .forms import PrestamoForm
from .constants import *
from .pdfFunctions import *
import os
import numpy as np

class PrestamoListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'leasing/home.html'
    context_object_name= 'prestamos'

# EN ESTA FUNCIÓN VA LA LÓGICA DEL LEASING

def prestamo_tabla(request, pk):
    
    tables = [] #Arreglo de diccionarios sobre el cual vamos a iterar

    #Al crear un nuevo leasing nos traerá automáticamente a esta función

    # del prestamo

    prestamo = Prestamo.objects.filter(id=pk).first()

    switcher_fp = {
       30: 'Mensual',
       60: 'Bimestral',
       90: 'Trimestral',
       120: 'Cuatrimestral',
       180: 'Semestral'
    }
    
    frecuencia_pago = switcher_fp[prestamo.frecuencia_de_pago]

    tasa_interes = 0

    if prestamo.tipo_tasa_interes == 'TNA':
        tasa_interes = round(((1+((prestamo.tasa_de_interes/100)/prestamo.periodo_cap))**(prestamo.periodo_cap))-1, 9)
    else:
        tasa_interes = prestamo.tasa_de_interes/100

    #del arrendamiento

    IGV_del_activo = (prestamo.precio_venta_del_activo/(1+IGV))*IGV

    valor_de_venta_a = prestamo.precio_venta_del_activo - IGV_del_activo


    monto_del_leasing = (valor_de_venta_a +
    prestamo.costos_notariales + prestamo.costos_registrales +
    prestamo.tasacion + prestamo.comision_de_estudio +
    prestamo.comision_de_activacion)

    TEP = (1 + tasa_interes)**(prestamo.frecuencia_de_pago/360) - 1

    numero_cuotas_por_ano = 360/prestamo.frecuencia_de_pago

    nCuotas = numero_cuotas_por_ano*prestamo.numero_de_años

    # de los costes/gastos periodicos

    s_riesgo = (prestamo.seguro_riesgo/100)*(prestamo.precio_venta_del_activo/numero_cuotas_por_ano) 

    # … totales por …

    intereses = 0
    amortizacion_c = 0
    seguro_ctr = 0
    comisiones_p = 0
    recompra_t = 0
    desembolso_t = 0

    # Descuentos 

    tasa_desc = round((1+(prestamo.tasa_descuento_Ks/100))**(prestamo.frecuencia_de_pago/360) - 1, 9)
    tasa_desc2 = round((1+(prestamo.tasa_descuento_WACC/100))**(prestamo.frecuencia_de_pago/360) - 1, 9)

    #de Indicadores de Rentabilidad

    VAN_fb = 0
    VAN_fn = 0
    TIR_fb = 0
    TIR_fn = 0
    TCEA_fb = 0
    TCEA_fn = 0

    #Flujos brutos y netos

    flujo_br = []
    flujo_nt = []
    flujo_br.append(monto_del_leasing)
    flujo_nt.append(monto_del_leasing)

    # Llenamos la tabla con las variables calculadas
    
    inicio_periodo_pg = prestamo.periodo_inicial_pg
    fin_periodo_pg = prestamo.periodo_inicial_pg + (prestamo.plazo_de_gracia/30)

    for x in range(1, int(nCuotas) + 1):
        campo = {}
        campo["n"] = x
        if x == 1:
            campo["saldo_inicial"] = monto_del_leasing
        else:
            campo["saldo_inicial"] = tables[x-2]["saldo_final"]
        campo["interes"] = (campo["saldo_inicial"]*-1)*TEP
        if inicio_periodo_pg == x and inicio_periodo_pg < int(fin_periodo_pg):
            inicio_periodo_pg += 1
            campo["Cuota"] = 0
            campo["amortizacion"] = 0
            campo["saldo_final"] = campo["saldo_inicial"] - campo["interes"]
        else:
            campo["amortizacion"] = (campo["saldo_inicial"]*-1)/(nCuotas-x+1)
            campo["Cuota"] = campo["interes"] + campo["amortizacion"]
            campo["saldo_final"] = campo["saldo_inicial"] + campo["amortizacion"]
        campo["seguro_riesgo"] = s_riesgo*-1
        campo["comision"] = (prestamo.comision_periodica)*-1
        if x == int(nCuotas):
            campo["recompra"] = ((prestamo.recompra/100)*valor_de_venta_a)*-1
        else:
            campo["recompra"] = 0
        campo["depreciacion"] = (valor_de_venta_a/nCuotas)*-1
        campo["ahorro_t"] = (campo["interes"] + campo["seguro_riesgo"] + campo["comision"] + campo["depreciacion"])*impuesto_renta
        campo["igv"] = (campo["Cuota"] + campo["seguro_riesgo"] + campo["comision"] + campo["recompra"])*IGV
        campo["flujo_b"] = campo["Cuota"] + campo["seguro_riesgo"] + campo["comision"] + campo["recompra"]
        campo["flujo_igv"] = campo["igv"] + campo["flujo_b"]
        campo["flujo_neto"] = campo["flujo_b"] - campo["ahorro_t"]

        intereses = campo["interes"] + intereses
        amortizacion_c = campo["amortizacion"] + amortizacion_c
        seguro_ctr = campo["seguro_riesgo"] + seguro_ctr
        comisiones_p = campo["comision"] + comisiones_p
        recompra_t = recompra_t + campo["recompra"]
        flujo_br.append(campo["flujo_b"])
        flujo_nt.append(campo["flujo_neto"])

        tables.append(campo)

    # Totales por

    intereses = intereses*-1
    amortizacion_c = amortizacion_c*-1
    seguro_ctr = seguro_ctr*-1
    comisiones_p = comisiones_p*-1
    recompra_t =recompra_t*-1
    desembolso_t = intereses + amortizacion_c + seguro_ctr + comisiones_p + recompra_t
    
    #Indicadores de rentabilidad

    VAN_fb = np.npv(tasa_desc, flujo_br)
    VAN_fn = np.npv(tasa_desc2, flujo_nt)
    TIR_fb = np.irr(flujo_br)
    TIR_fn = np.irr(flujo_nt)
    TCEA_fb = ((1+TIR_fb)**(360/prestamo.frecuencia_de_pago))-1
    TCEA_fn = ((1+TIR_fn)**(360/prestamo.frecuencia_de_pago))-1
    
    # Guardar periodo elegido en formato pdf

    year = prestamo.fecha_inicio.year
    month = prestamo.fecha_inicio.month
    day = prestamo.fecha_inicio.day

    query = request.POST.get("nPeriodo")
    periodoI = request.POST.get("periodoI")
    periodoF = request.POST.get("periodoF")

    numPeriodos = ""
    valor = ""

    if 'buscar' in request.POST and query != "" or 'filtrar' in request.POST and periodoI != "" and periodoF != "":
        valor = "s"
        iType = "submit"  
    else:
        iType = "hidden"    

    if 'filtrar' in request.POST and periodoI != "" and periodoF != "": #Filtramos entre periodos
        numPeriodos = range(int(periodoI), int(periodoF)+1)

    #Path generico
    
    path = "/Users/DOMINIC/Desktop/UPC VI/FINANZAS/Trabajo parcial/leasingApp/Final-Project-Finance/Leasing_project/"

    # Del flujo de caja

    if 'PDF' in request.POST:
        nPeriodoPDF = request.POST.get("nPeriodoPDF")
        periodoIPDF = request.POST.get("periodoIPDF")
        periodoFPDF = request.POST.get("periodoFPDF")

        #Creamos el path

        nestedPath = ""

        nestedPath = path + "LeasingPDF/" + str(prestamo.empresa_solicitante.razon_social + "/flujo de caja/")

        if not os.path.exists(nestedPath): 
            os.makedirs(nestedPath)

        #Por periodo unico

        if periodoIPDF == "None" and periodoFPDF == "None":
            mess = "-Pu"

            if not os.path.exists(nestedPath + "periodo/"): 
                os.makedirs(nestedPath + "periodo/")

            for x in range(1, int(nCuotas) + 1):
                if tables[x-1]["n"] == int(nPeriodoPDF):
                    iterarPDFflujo(year, month, day, tables, x, prestamo, mess, nestedPath + "periodo/")

            messages.success(request, f'¡Se ha guardado PDF exitósamente!')

        #Consolidado

        if nPeriodoPDF == "None": 
            mess = ""
            pdf_files = []
            num = 1

            for x in range(1, int(nCuotas) + 1):  
                if tables[x-1]["n"] >= int(periodoIPDF) and tables[x-1]["n"] <= int(periodoFPDF):
                    iterarPDFflujo(year, month, day, tables, x, prestamo, mess, path)
                    pdf_files.append("LAP-Sol-" + str(prestamo.id) + " " + str(prestamo.empresa_solicitante.razon_social) + "-Periodo-" +  str(x) + " " +
                    str(year) + "-" + str(month) + "-" + str(day) + ".pdf")  

            merger = PdfFileMerger()
            for files in pdf_files:
                merger.append(path+files)

            if not os.path.exists(nestedPath + "consolidado/"): 
                os.makedirs(nestedPath + "consolidado/")
            
            while os.path.exists(nestedPath + "consolidado/" + "LAP-Sol-" + str(prestamo.id) + " " + str(prestamo.empresa_solicitante.razon_social) + "-consolidado-" + str(num) + " " +
            str(year) + "-" + str(month) + "-" + str(day) + ".pdf"):
                num += 1

            merger.write(nestedPath + "consolidado/" + "LAP-Sol-" + str(prestamo.id) + " " + str(prestamo.empresa_solicitante.razon_social) + "-consolidado-" + str(num) + " " +
            str(year) + "-" + str(month) + "-" + str(day) + ".pdf")
            merger.close()
    
            for x in range(1, int(nCuotas) + 1):  
                if tables[x-1]["n"] >= int(periodoIPDF) and tables[x-1]["n"] <= int(periodoFPDF):
                    os.remove(path+"LAP-Sol-" + str(prestamo.id) + " " + str(prestamo.empresa_solicitante.razon_social) + "-Periodo-" +  str(x) + " " +
                    str(year) + "-" + str(month) + "-" + str(day) + ".pdf")  

            messages.success(request, f'¡Se ha guardado PDF exitósamente!')

    # De los datos de entrada
        
    if 'PDFentrada' in request.POST:

        #Creamos el path

        nestedPath = path + "LeasingPDF/" + str(prestamo.empresa_solicitante.razon_social + "/datos de entrada/")

        if not os.path.exists(nestedPath): 
            os.makedirs(nestedPath)

        PDFDE(year, month, day, prestamo, nestedPath, frecuencia_pago, dias_del_ano, IGV*100, impuesto_renta*100)

        messages.success(request, f'¡Se ha guardado PDF exitósamente!')
    
    # Del resultado
    
    if 'PDResultado' in request.POST:

        #Creamos el path

        nestedPath = path + "LeasingPDF/" + str(prestamo.empresa_solicitante.razon_social + "/resultados/")

        if not os.path.exists(nestedPath): 
            os.makedirs(nestedPath)

        PDFRE(year, month, day, prestamo, nestedPath, IGV_del_activo, valor_de_venta_a, monto_del_leasing, TEP*100,
        numero_cuotas_por_ano, nCuotas, s_riesgo, intereses, amortizacion_c, seguro_ctr, comisiones_p, recompra_t,
        desembolso_t, TCEA_fb*100, TCEA_fn*100, VAN_fb, VAN_fn)

        messages.success(request, f'¡Se ha guardado PDF exitósamente!')

    

    context = {
        'tables': tables,
        'pk': pk,
        'prestamo': prestamo,
        'query': query,
        'valor': valor,
        'iType': iType,
        'numPeriodos': numPeriodos,
        'periodoI': periodoI,
        'periodoF': periodoF,
        'frecuencia_pago': frecuencia_pago,
        'dias_del_ano': dias_del_ano,
        'IGV': IGV*100,
        'impuesto_renta': impuesto_renta*100,
        'IGV_del_activo': IGV_del_activo,
        'valor_de_venta_a': valor_de_venta_a,
        'monto_del_leasing': monto_del_leasing,
        'TEP': TEP,
        'numero_cuotas_por_ano': numero_cuotas_por_ano,
        'nCuotas': nCuotas,
        's_riesgo': s_riesgo,
        'intereses': intereses, 
        'amortizacion_c': amortizacion_c,
        'seguro_ctr': seguro_ctr,
        'comisiones_p': comisiones_p,
        'recompra_t': recompra_t,
        'desembolso_t': desembolso_t,
        'TCEA_fb': TCEA_fb*100,
        'TCEA_fn': TCEA_fn*100,
        'VAN_fb': VAN_fb,
        'VAN_fn': VAN_fn
    }

    return render(request, 'leasing/prestamo_tabla.html', context)

class PrestamoCreateView(LoginRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PrestamoUpdateView(LoginRequiredMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    success_url = '/'

class PrestamoDeleteView(LoginRequiredMixin, DeleteView):
    model = Prestamo
    success_url = '/'

# Empresas

class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'leasing/empresa_list.html'
    context_object_name= 'empresas'

class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    fields = ['nombre_empresa', 'razon_social', 'ciudad', 'ruc', 'telefono']

class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    fields = ['nombre_empresa', 'razon_social', 'ciudad', 'ruc', 'telefono']

class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = Empresa
    success_url = '/empresa'