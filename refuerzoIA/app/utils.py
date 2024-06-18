from PIL import Image, ImageDraw
from .models import Revision, Imagen, User
import json
import os

class Revision1Object:

    def __init__(self):
        self.datosImgMostrar = None
        self.jsonInf = None
        self.listaRevPendientes = []
        self.ultima = False
        self.primera = False
        self.idRevision = 0
        self.posicion = 0

    def crearListaRevisiones(self, userId):
        self.listaRevPendientes = []
        listaRev = Revision.objects.filter(usuario_id = userId, tipoRevision = 0, pendiente = 1).values()
        for r in listaRev:
            imgPosRev = Imagen.objects.get(id = r['imagen_id'])
            if imgPosRev.numRevisiones < imgPosRev.maxRevisiones:
                self.listaRevPendientes.append(r)

    def buscarImgRev(self):
        if self.listaRevPendientes:
            try:
                self.datosImgMostrar = Imagen.objects.get(id = self.listaRevPendientes[self.posicion]['imagen_id'])
            except:
                self.posicion -= 1
                self.datosImgMostrar = Imagen.objects.get(id = self.listaRevPendientes[self.posicion]['imagen_id'])
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']
        else:
            self.datosImgMostrar = None
            self.jsonInf = None

    def esPrimera(self):
        if self.datosImgMostrar:
            if self.posicion == 0:
                self.primera = True
                return True
            else:
                self.primera = False
                return False
        else:
            self.primera = False
            return False

    def esUltima(self):
        if self.datosImgMostrar:
            if self.posicion == (len(self.listaRevPendientes)-1):
                self.ultima = True
                return True
            else:
                self.ultima = False
                return False
        else:
            self.ultima = False
            return False

    def irSiguiente(self):
        if self.posicion < (len(self.listaRevPendientes)-1):
            self.posicion += 1
            idImgSig = self.listaRevPendientes[self.posicion]['imagen_id']
            self.datosImgMostrar = Imagen.objects.get(id = idImgSig)
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']

    def irAnterior(self):
        if self.posicion > 0:
            self.posicion -= 1
            idImgAnte = self.listaRevPendientes[self.posicion]['imagen_id']
            self.datosImgMostrar = Imagen.objects.get(id = idImgAnte)
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']

class Revision2Object:
    
    def __init__(self):
        self.datosImgMostrar = None
        self.jsonInf = None
        self.listaRevPendientes = []
        self.ultima = False
        self.primera = False
        self.idRevision = 0
        self.posicion = 0

    def crearListaRevisiones(self, userId):
        self.listaRevPendientes = []
        listaRev = Revision.objects.filter(usuario_id = userId, tipoRevision = 1, pendiente = 1).values()
        for r in listaRev:
            imgPosRev = Imagen.objects.get(id = r['imagen_id'])
            if imgPosRev.numRevisiones < imgPosRev.maxRevisiones:
                self.listaRevPendientes.append(r)

    def buscarImgRev(self):
        if self.listaRevPendientes:
            try:
                self.datosImgMostrar = Imagen.objects.get(id = self.listaRevPendientes[self.posicion]['imagen_id'])
            except:
                self.posicion -= 1
                self.datosImgMostrar = Imagen.objects.get(id = self.listaRevPendientes[self.posicion]['imagen_id'])
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']
        else:
            self.datosImgMostrar = None
            self.jsonInf = None

    def esPrimera(self):
        if self.datosImgMostrar:
            if self.posicion == 0:
                self.primera = True
                return True
            else:
                self.primera = False
                return False
        else:
            self.primera = False
            return False

    def esUltima(self):
        if self.datosImgMostrar:
            if self.posicion == (len(self.listaRevPendientes)-1):
                self.ultima = True
                return True
            else:
                self.ultima = False
                return False
        else:
            self.ultima = False
            return False
    
    def irSiguiente(self):
        if self.posicion < (len(self.listaRevPendientes)-1):
            self.posicion += 1
            idImgSig = self.listaRevPendientes[self.posicion]['imagen_id']
            self.datosImgMostrar = Imagen.objects.get(id = idImgSig)
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']

    def irAnterior(self):
        if self.posicion > 0:
            self.posicion -= 1
            idImgAnte = self.listaRevPendientes[self.posicion]['imagen_id']
            self.datosImgMostrar = Imagen.objects.get(id = idImgAnte)
            self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
            self.idRevision = self.listaRevPendientes[self.posicion]['id']

    def dibujarRectangulos(self):
        if self.listaRevPendientes:
            # Cargar la imagen
    
            ruta = 'app/static' + self.datosImgMostrar.nombreImg
            imagen = Image.open(ruta)

            #buscar revision 1

            revision2 = Revision.objects.get(id = self.idRevision)
            usuarioId =  revision2.usuario_id
            imagenId = revision2.imagen_id
            revision1 = Revision.objects.get(usuario_id = usuarioId, imagen_id = imagenId, tipoRevision = 0)
            
            dataInf = json.loads(self.jsonInf)
            dataRev1 = json.loads(revision1.correcion)

            # Coordenadas del rectángulo (esquina superior izquierda y esquina inferior derecha)


            for obj in dataInf['label_stats']:

                col_min_value = obj['col_min'] *2
                col_inc_value = obj['col_inc'] *2
                row_min_value = obj['row_min'] *2
                row_inc_value = obj['row_inc'] *2

                x1 = col_min_value 
                y1 = row_min_value
                x2 = col_min_value + col_inc_value
                y2 = row_min_value + row_inc_value

                # Crear un objeto ImageDraw para dibujar en la imagen
                draw = ImageDraw.Draw(imagen)

                # Dibujar el rectángulo en la imagen
                rectangulo = [(x1, y1), (x2, y2)]
                color = (64, 84, 196)  # Color del rectángulo (en formato RGB)
                for rev in dataRev1['label_review']:
                    if rev['id'] == obj ['id']:
                        if rev['state'] == 'ok':
                            color = (0, 102, 51)
                        elif rev['state'] == 'error':
                            color = (204, 0, 0)
                
                grosor = 8  # Grosor del borde del rectángulo
                draw.rectangle(rectangulo, outline=color, width=grosor)


            # Guardar la imagen con el rectángulo dibujado
                       
            nombreImgEditada = ruta[:-4] + '_modificada' + ruta[-4:]
            imagen.save(nombreImgEditada)
            x = nombreImgEditada.find("static")
            longitud = len("static")
            nombreImgEditada = nombreImgEditada[(x+longitud):]

            return nombreImgEditada
        else:
            return None

    def revisionCompleta(self, revisionComp):
        self.datosImgMostrar = Imagen.objects.get(id = revisionComp.imagen_id)
        self.jsonInf = utiles.jsonEntrada(self.datosImgMostrar.inferencia, self.datosImgMostrar.id)
        self.listaRevPendientes.append(revisionComp)
        self.idRevision = revisionComp.id
            
class utiles:
    def jsonEntrada(inferencia, idImg):
        datos = json.loads(inferencia)
        etiquetas = datos["label_stats"]
        coordenadas = []
        for rectangulo in etiquetas:
            rect = {
                "id": rectangulo["id"], 
                "col_min": rectangulo["col_min"]/2, 
                "row_min": rectangulo["row_min"]/2,
                "col_inc": rectangulo["col_inc"]/2,
                "row_inc": rectangulo["row_inc"]/2,
                "area": rectangulo["area"],
                "color": "purple",
                "state": "default"
                }
            coordenadas.append(rect)
        coorDict = {
            "idImg": idImg,
            "image_name": datos["image_name"],
            "label_number": len(etiquetas),
            "label_stats": coordenadas
        }
        jsonEtiquetas = json.dumps(coorDict)

        return jsonEtiquetas

    def salidaJSON(self,imagenRev):
        listaRev = []
        for rectangulo in imagenRev["label_stats"]:
            rectangulo.pop("col_min")
            rectangulo.pop("col_inc")
            rectangulo.pop("row_min")
            rectangulo.pop("row_inc")
            rectangulo.pop("color")
            rectangulo.pop("area")
            listaRev.append(rectangulo)
        revFormat = {
            "image_name": imagenRev["image_name"],
            "label_number": imagenRev["label_number"],
            "label_review": listaRev
        }
        
        jsonFormateado = json.dumps(revFormat)
        return jsonFormateado

    def revision2JSON(self,nombreImagen, jsonRev):
        datos = json.loads(jsonRev)
        numEtiquetas = 0
        listaEtiquetas = []
        for etiqueta in datos:
            numEtiquetas += 1
            etiquetaFormato = {
                "id": etiqueta['id'],
                "col_min": etiqueta['x']*2,
                "col_inc": etiqueta['width']*2,
                "row_min": etiqueta['y']*2,
                "row_inc": etiqueta['height']*2
            }
            listaEtiquetas.append(etiquetaFormato)
        revFormat = {
            "image_name": nombreImagen,
            "newlabel_number": numEtiquetas,
            "newlabel_review": listaEtiquetas
        }
        
        jsonFormateado = json.dumps(revFormat)
        return jsonFormateado

    def listaImagenes(self):
        listaImg = Imagen.objects.all().values()
        imagenesPorRevisar = []
        for im in listaImg:
            if im['numRevisiones'] < im['maxRevisiones']:
                imagenesPorRevisar.append(im)
        return imagenesPorRevisar
    
    def listaUsuarios(self):
        listaU = User.objects.all().values()
        return listaU
    

    # Esta funcion la utiliza la vista de Asignar Imagenes, para consultar si ya estaba asignada la revision de una imagen a un usuario
    def noExisteRev(self, img, usuId):
        listaRev = Revision.objects.filter(imagen_id = img, usuario_id = usuId).values()
        if listaRev:
            return False
        else:
            return True
        