"""
URL configuration for refuerzoIA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from app import views
#para la imagen
from django.conf import settings
from django.conf.urls.static import static

#--------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('registro/', views.registro,name='registro'),
    path('logout/',views.cerrarSesion,name='logout'),
    path('login/', views.iniciarSesion,name='login'),

    path('home/', views.home,name='home'),

    path('revision1/', views.revision1,name='revision1'),
    path('revision1S/', views.revision1Siguiente,name='revision1S'),
    path('revision1A/', views.revision1Anterior,name='revision1A'),
    path('crearRev1/', views.crearRev1, name="crearRev1"),

    path('revision2/', views.revision2,name='revision2'),
    path('revision2S/', views.revision2Siguiente, name="revision2S"),
    path('revision2A/', views.revision2Anterior, name="revision2A"),
    path('crearRev2/', views.crearRev2, name="crearRev2"),

    path('nuevaImgPre/', views.nuevaImgPre, name="nuevaImgPre"),
    path('nuevaImgPost/', views.nuevaImgPost, name="nuevaImgPre"),
    
    path('listaImagenes/', views.listaImagenes, name="listaImagenes"),
    path('verDatosImagen/', views.verDatosImagen, name="verDatosImagen"),

    path('asignarImgPre/', views.asignarImgPre, name="asignarImgPre"),
    path('asignarImgPost/', views.asignarImgPost, name="asignarImgPost"),

    path('histRevPre/', views.histRevPre, name="histRevPre"),
    path('mostrarHistRev/', views.mostrarHistRev, name="mostrarHistRev"),

    path('usuariosPre/', views.listaUsuariosPre, name="listaUsuariosPre"),
    path('buscarUs/', views.buscarUsuario, name="buscarUsuario"),
    path('cambiosUs/', views.cambiosUs, name="cambiosUs"),

    path('estadisticas/', views.estadisticas, name="estadisticas"),
    path('grafH/', views.grafHistorico, name="grafH"),
    path('grafP/', views.grafPrecision, name="grafP"),
    path('grafA/', views.grafActividad, name="grafA"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#--------------