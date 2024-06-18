from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login , logout
from .models import Imagen,Revision, User
from django.template import loader
from django.http import HttpResponse
#----.----
from PIL import Image, ImageDraw
from django.http import HttpResponse
import json
import datetime

from .utils import utiles, Revision1Object, Revision2Object

u = utiles()
# Create your views here.


def registro(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user =  authenticate(username = username , password = password)
                mensajeR = "Nuevo usuario registrado: " + user.username
                return render(request, 'home.html', {'msg': mensajeR})
            else:
                return render(request,'registro.html',{'form':form})
        else:
            form = UserCreationForm()
            return render(request,'registro.html',{'form':form})
    else:
        return redirect('/home')

def cerrarSesion(request):
    logout(request)
    return redirect('/')

def iniciarSesion(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user =  authenticate(username = username , password = password)
        if user is not None:
            login(request,user)
            return redirect('/home')
        else :
            msg = 'Nombre de usuario o contraseña incorrectos'
            form = AuthenticationForm(request.POST)
            return render(request , 'login.html', {'form':form, 'msg':msg})
    else :
        form = AuthenticationForm()
        return render(request , 'login.html', {'form':form})

def index(request):
    return render(request, 'index.html')

def home(request):
    if request.user.is_authenticated:
        global obRev1
        obRev1 = Revision1Object()
        global obRev2
        obRev2 = Revision2Object()
        return render(request, 'home.html')
    else:
        return redirect('/')


def revision1(request):
    if request.user.is_authenticated:
        obRev1.crearListaRevisiones(request.user.id)
        obRev1.buscarImgRev()
        template = loader.get_template('revision1.html')
        context = {
            'datosImagen': obRev1.datosImgMostrar,
            'jsonInf': obRev1.jsonInf,
            'primera': obRev1.esPrimera(),
            'ultima': obRev1.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')

def revision1Siguiente(request):
    if request.user.is_authenticated:
        obRev1.irSiguiente()  
        template = loader.get_template('revision1.html')
        context = {
            'datosImagen': obRev1.datosImgMostrar,
            'jsonInf': obRev1.jsonInf,
            'primera': obRev1.esPrimera(),
            'ultima': obRev1.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')

def revision1Anterior(request):
    if request.user.is_authenticated:
        obRev1.irAnterior() 
        template = loader.get_template('revision1.html')
        context = {
            'datosImagen': obRev1.datosImgMostrar,
            'jsonInf': obRev1.jsonInf,
            'primera': obRev1.esPrimera(),
            'ultima': obRev1.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
    
def crearRev1(request):
    if request.method == 'POST':
        jsonRevision = request.POST.get('jsonRevision')
        imagenRevisada = json.loads(jsonRevision)
        imagenActual = Imagen.objects.get(id=imagenRevisada["idImg"])
        imagenActual.numRevisiones += 1
        imagenActual.save()
        jsonFormateo = u.salidaJSON(imagenRevisada)
        rev = Revision.objects.get(id = obRev1.idRevision)
        rev.correcion = jsonFormateo
        rev.fechaRevision = datetime.datetime.now()
        rev.pendiente = 0
        rev.save()
        nuevaRev = Revision(usuario = request.user, imagen = imagenActual, tipoRevision = 1, pendiente = 1, fechaAsignacion = datetime.datetime.now())
        nuevaRev.save()
        obRev2.revisionCompleta(nuevaRev)
        template = loader.get_template('revision2.html')
        context = {
            'datosImagen': obRev2.datosImgMostrar,
            'imagenDibujo': obRev2.dibujarRectangulos(),
            'primera': True,
            'ultima': True,
            'revCompleta': "¿Quieres completar la revisión 2 ahora?"
        }
        return HttpResponse(template.render(context,request))
    return redirect('/revision1')

def revision2(request):
    if request.user.is_authenticated:
        obRev2.crearListaRevisiones(request.user.id)
        obRev2.buscarImgRev()
        template = loader.get_template('revision2.html')
        context = {
            'datosImagen': obRev2.datosImgMostrar,
            'imagenDibujo': obRev2.dibujarRectangulos(),
            'primera': obRev2.esPrimera(),
            'ultima': obRev2.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')

def revision2Siguiente(request):
    if request.user.is_authenticated:
        obRev2.irSiguiente()  
        template = loader.get_template('revision2.html')
        context = {
            'datosImagen': obRev2.datosImgMostrar,
            'imagenDibujo': obRev2.dibujarRectangulos(),
            'primera': obRev2.esPrimera(),
            'ultima': obRev2.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')

def revision2Anterior(request):
    if request.user.is_authenticated:
        obRev2.irAnterior() 
        template = loader.get_template('revision2.html')
        context = {
            'datosImagen': obRev2.datosImgMostrar,
            'imagenDibujo': obRev2.dibujarRectangulos(),
            'primera': obRev2.esPrimera(),
            'ultima': obRev2.esUltima()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
    
def crearRev2(request):
    if request.method == 'POST':
        rCompleta = request.POST.get('rCompleta')
        jsonRevision = request.POST.get('jsonNuevasEtiquetas')
        jsonFormateo = u.revision2JSON(obRev2.datosImgMostrar.nombreImg, jsonRevision)
        rev = Revision.objects.get(id = obRev2.idRevision)
        rev.correcion = jsonFormateo
        rev.fechaRevision = datetime.datetime.now()
        rev.pendiente = 0
        rev.save()
        if rCompleta == 'True':
            return redirect('/revision1')
        else:
            return redirect('/revision2')
    return redirect('/revision2')
        
def nuevaImgPre(request):
    if request.user.is_authenticated:
        return render(request, 'nuevaImg.html')
    else:
        return redirect('/')

def nuevaImgPost(request):
    if request.method == 'POST':
        nombreImg = request.POST.get('nombreImg')
        revMax = request.POST.get('revMax')
        jsonImg = request.POST.get('jsonImg')
        nuevaImg = Imagen(nombreImg = nombreImg, numRevisiones = 0, inferencia=jsonImg, maxRevisiones= revMax)
        nuevaImg.save()
        return render(request, 'home.html', {"msg": "Imagen añadida a la base de datos con éxito"})
    return redirect('/home')

def listaImagenes(request):
    if request.user.is_authenticated:
        template = loader.get_template('listaImagenes.html')
        context = {
            'listaImagenes': Imagen.objects.all().values(),
            'listaUsuarios': u.listaUsuarios()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
    
def verDatosImagen(request):
    if request.user.is_authenticated:
        opcion = request.GET.get('dato')
        idImg = request.GET.get('img')
        imagenMostrar = Imagen.objects.get(id=idImg)
        if opcion == "url":
            context = {
                'urlImg': imagenMostrar.nombreImg
            }
        elif opcion == "inferencia":
            context = {
                'infImg': imagenMostrar.inferencia
            }
        elif opcion == "imagen":
            context = {
                'img': imagenMostrar.nombreImg
            }
        template = loader.get_template('datosImagen.html')
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')


def asignarImgPre(request):
    if request.user.is_authenticated:
        template = loader.get_template('asignarImg.html')
        context = {
            'listaImagenes': u.listaImagenes(),
            'listaUsuarios': u.listaUsuarios()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
    
    
def asignarImgPost(request):
    if request.method == 'POST':
        mensajeC = []
        mensajeE = []
        idImgSel = request.POST.getlist('imgSel')
        idUsuSel = request.POST.getlist('userSel')
        for imgId in idImgSel:
            for usuId in idUsuSel:
                usuTemp = User.objects.get(id = usuId)
                if u.noExisteRev(imgId, usuTemp.id):
                    nuevaRev = Revision(imagen_id = imgId, usuario_id = usuTemp.id, fechaAsignacion = datetime.datetime.now(), pendiente=1, tipoRevision = 0)
                    nuevaRev.save()
                    check = "- Asignada la imagen "+imgId+" al usuario "+ usuTemp.username
                    mensajeC.append(check)
                else:
                    error = " - La imagen "+imgId+" ya tenía revisión asignada al usuario " + usuTemp.username
                    mensajeE.append(error)
        template = loader.get_template('asignarImg.html')
        context = {
            'listaImagenes': u.listaImagenes(),
            'listaUsuarios': u.listaUsuarios(),
            'mensajeC': mensajeC,
            'mensajeE': mensajeE
        }
        return HttpResponse(template.render(context,request))
    return redirect('/home')

def histRevPre(request):
    if request.user.is_authenticated:
        template = loader.get_template('histRev.html')
        context = {
            'listaUsuarios': u.listaUsuarios()
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
    
def mostrarHistRev(request):
    if request.method == 'POST':
        mensajeE = ""
        listaRevisiones = []
        usuarioSel = request.POST.get('usuarioSel')
        fechaDesde = request.POST.get('fechaDesde')
        fechaHasta = request.POST.get('fechaHasta')
        estado = request.POST.get('estado')
        tipo = request.POST.get('tipo')
        
        if not fechaDesde:
            fechaDesde = "0001-01-01"
        fechaDesde += " 00:00:00"
        if not fechaHasta:
            fechaHasta = datetime.datetime.now()
        else:
            fechaHasta += " 23:59:00"
            
        #llevarlo a u.qSetListaRev    
        if usuarioSel == "todos":
            if estado == "todos":
                if tipo == "todos":
                    listaRevisiones = Revision.objects.filter(fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values() 
                else:
                    listaRevisiones = Revision.objects.filter(tipoRevision = tipo, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
            else:
                if tipo == "todos":
                    listaRevisiones = Revision.objects.filter(pendiente = estado, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
                else:
                    listaRevisiones = Revision.objects.filter(pendiente = estado, tipoRevision = tipo, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
        else:
            usuSel = User.objects.get(username = usuarioSel)
            if estado == "todos":
                if tipo == "todos":
                    listaRevisiones = Revision.objects.filter(usuario_id = usuSel.id, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values() 
                else:
                    listaRevisiones = Revision.objects.filter(usuario_id = usuSel.id, tipoRevision = tipo, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
            else:
                if tipo == "todos":
                    listaRevisiones = Revision.objects.filter(usuario_id = usuSel.id, pendiente = estado, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
                else:
                    listaRevisiones = Revision.objects.filter(usuario_id = usuSel.id, pendiente = estado, tipoRevision = tipo, fechaAsignacion__gte = fechaDesde, fechaAsignacion__lte = fechaHasta).values()
        
        # llevarlo a u.formatearListaRev
        for rev in listaRevisiones:
            if rev['pendiente']:
                usuario = User.objects.get(id=rev['usuario_id'])
                rev['usuario_id']= usuario.username
                if rev['tipoRevision']:
                    rev['tipoRevision']= "dibujo"
                else:
                    rev['tipoRevision'] = "click"
                rev['pendiente'] = "pendiente"
                rev['fechaRevision'] = "Sin revisar"
            else:
                usuario = User.objects.get(id=rev['usuario_id'])
                rev['usuario_id']= usuario.username
                if rev['tipoRevision']:
                    rev['tipoRevision']= "dibujo"
                else:
                    rev['tipoRevision'] = "click"
                rev['pendiente'] = "revisada"

        if not listaRevisiones:
            mensajeE = "No hay revisiones que coincidan con el criterio de búsqueda"       
        template = loader.get_template('histRev.html')
        context = {
            'listaUsuarios': u.listaUsuarios(),
            'mensajeE': mensajeE,
            'listaRevisiones': listaRevisiones
        }
        return HttpResponse(template.render(context,request))
    return redirect('/home')

def listaUsuariosPre(request):
    if request.user.is_authenticated:
        lista = User.objects.all().values()
        context = {
            'allUsers': lista,
        }
        template = loader.get_template('usuarios.html')
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')

def buscarUsuario(request):
    if request.method == 'POST':
        habilitarEdicion = False
        listaUsuarios = []
        allUsers = User.objects.all().values()
        usuarioSel = request.POST.get('usuarioSel')
        if usuarioSel == "todos":
            listaUsuarios = allUsers
        else:
            usuarioBusq = User.objects.get(id = usuarioSel)
            listaUsuarios.append(usuarioBusq)
            habilitarEdicion = True
        template = loader.get_template('usuarios.html')
        context = {
            'allUsers': allUsers,
            'listaUsuarios': listaUsuarios,
            'botonEditar': habilitarEdicion
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/home')

def cambiosUs(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        uActivo = request.POST.get('uActivo')
        uAdmin = request.POST.get('uAdmin')
        usuarioCambiar = User.objects.get(id = userId)
        mensajeU = "El usuario " + usuarioCambiar.username
        if uActivo:
            usuarioCambiar.is_active = True
            mensajeU += " está activo"
            if uAdmin:
                usuarioCambiar.is_superuser = True
                mensajeU += " y es administrador"
            else:
                usuarioCambiar.is_superuser = False
                mensajeU += " y no es administrador"
        else:
            usuarioCambiar.is_active = False
            usuarioCambiar.is_superuser = False
            mensajeU += " no está activo"
        
        usuarioCambiar.save()
        template = loader.get_template('usuarios.html')
        context = {
            "mensajeU": mensajeU
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/home')

def estadisticas(request):
    if request.user.is_authenticated:
        return render(request, 'estadisticas.html')
    else:
        return redirect('/')

def grafHistorico(request):
    if request.user.is_authenticated:
        return render(request, 'graficoH.html')
    else:
        return redirect('/')

def grafPrecision(request):
    if request.user.is_authenticated:
        return render(request, 'graficoP.html')
    else:
        return redirect('/')

def grafActividad(request):
    if request.user.is_authenticated:
        datos = {
            'ejeX': ['Label 1', 'Label 2', 'Label 3', 'Label 4'],
            'ejeY': [10, 30, 15, 25],
        }
        context = {
            'datos' : json.dumps((datos))
        }
        template = loader.get_template('graficoA.html')
        return HttpResponse(template.render(context,request))
    else:
        return redirect('/')
