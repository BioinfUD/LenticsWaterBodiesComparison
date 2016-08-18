# -*- coding: utf-8 -*-
from django.db import models
from django import forms
import subprocess
import datetime
import threading
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from time import sleep
from django.core.files import File as Django_File
from django.conf import settings
from random import randint
import os
import csv
#from image_cropping import ImageCropWidget
#from image_cropping import ImageCropField, ImageRatioField

# Opciones estáticas
POSIBLES_ESTADOS_PROCESOS = (
    (0, "Terminado exitosamente"),
    (1, "Terminado con errores"),
    (2, "Ejecutandose"),
    (3, "En espera")
)
TIPO = (
    (0, "output"),
    (1, "input"),
)
FORMATO = (
    (0, "tif"),
    (1, "tiff"),
)

class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Perfiles'

    def __unicode__(self):
        return unicode(self.email)


class File(models.Model):
    fileUpload = models.FileField()
    #pan_image = ImageCropField(blank=True, upload_to='uploaded_images')
    # size is "width x height"
    #cropping = ImageRatioField('pan_image', '430x360')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    cell_size = models.IntegerField(default=1)
    description = models.TextField(default="")
    profile = models.ForeignKey(Profile)
    ext = models.CharField(max_length=7)
    tipo = models.IntegerField(choices=TIPO, default=0)
    test = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Archivos'

    def get_contenido(self):
        # falta/pendiente cambiar direccion
        return Django_File(open("%s%s" % (settings.BASE_DIR, self.fileUpload.url))).read()

    def get_kmer_dict(self):
        with open("%s%s" % (settings.BASE_DIR, self.fileUpload.url)) as file_object:
            d = list(csv.reader(file_object, delimiter="\t", dialect=csv.excel))
        return sorted(d)

    def __unicode__(self):
        return u"Imagen\nDescription: %s " % (self.description)


#class ImagesForm(forms.ModelForm):
#    class Meta:
#        model = File
#        fields = ('pan_image',)


class Proceso(models.Model):

    estado = models.IntegerField(choices=POSIBLES_ESTADOS_PROCESOS, default=3)
    std_err = models.TextField(default="None")
    std_out = models.TextField(default="None")
    comando = models.CharField(max_length=2000, default="echo Hola mundo")
    profile = models.ForeignKey(Profile)
    inicio = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(null=True)
    resultado = models.ForeignKey(File, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Procesos'

    def get_estado(self):
        return POSIBLES_ESTADOS_PROCESOS[self.estado][1] if self.estado <= 3 else "Terminado con errores"

    def get_resultado(self):
        return self.resultado.get_contenido()

    def get_kmer_dict(self):
        if "Tallymer" == self.contador:
            return sorted(self.resultado.get_kmer_dict(), key=lambda x: x[1])
        else:
            return self.resultado.get_kmer_dict()

    def run_process(self):
        self.estado = 2
        self.save()
        try:
            p = subprocess.Popen(
                str(self.comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            self.std_out, self.std_err = p.communicate()
            self.estado = p.returncode
            print p.returncode
            self.fin = datetime.datetime.now()
        except:
            try:
                self.std_out, self.std_err = p.communicate()
                self.estado = 0
                self.save()
                self.fin = datetime.datetime.now()
            except:
                self.estado = 0
                self.save()
                self.fin = datetime.datetime.now()
        #  self.std_out = self.std_out.replace("\n", "<br>")
        #  self.std_err = self.std_err.replace("\n", "<br>")
        self.save()

    def run(self):
        t = threading.Thread(target=self.run_process)
        t.setDaemon(True)
        t.start()

    def __unicode__(self):
        return u"ID: %s Estado: %s \n Comando: %s \n" % (str(self.id), str(self.estado), str(self.comando))


class Fusion(models.Model):

    name = models.TextField(default="Image Fusion Multispectral and Pancromatic")
    procesos = models.ManyToManyField(Proceso)
    profile = models.ForeignKey(Profile)
    out_file = models.ForeignKey(File, null=True)
    nivel = models.IntegerField(default=1)

    def run_this(self, file_pan="", file_mul="", nivel=""):
        self.name = "Fusión #%s" % self.id
        self.save()
        tmp_dir = "fusion_%s" % randint(1, 1000000)
        # Se ejecuta el Scrip creado para fusionar las imagenes
        comando = "python /home/nazkter/Sofware_Develop/fusion_multipan/bin/fusionScript.py %s %s %s /tmp/%s" % (file_mul, file_pan, nivel, tmp_dir)
        print "comando: %s" % (comando)
        # Se crea el proseso y se envia a la cola
        p1 = Proceso(comando=str(comando),profile=self.profile)
        p1.save()
        self.procesos.add(p1)
        # To get files with path: tales.fileUpload.path
        # Se genera indice y espero hasta que este listo
        t1 = threading.Thread(target=p1.run_process)
        t1.setDaemon(True)
        t1.start()
        while t1.isAlive():
            sleep(1)
        file_name = "/tmp/%s.tif" % tmp_dir

        '''
        with open(file_name, 'r+') as f:
            text = f.read()
            f.seek(0)
            f.truncate()
            f.write(text.replace(' ', '\t'))
        '''
        out_file = File(fileUpload=Django_File(open(
            file_name)), description="Salida " + self.name, profile=self.profile, ext="results")
        out_file.save()
        self.out_file = out_file
        p1.resultado = out_file
        p1.save()

    def run(self, file_pan="", file_mul="", nivel=""):
        t = threading.Thread(target=self.run_this, kwargs=dict(
            file_pan=file_pan, file_mul=file_mul, nivel=nivel))
        t.setDaemon(True)
        t.start()

    class Meta:
        verbose_name_plural = "Procesos de alinear y estimar abundancia"

    def __unicode__(self):
        return u"Alineamiento y estimación \n %s" % self.name
