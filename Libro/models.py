from django.db import models

class Genero(models.Model):
    nombre_genero = models.CharField(verbose_name='Genero', max_length=50)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'
        unique_together = ['nombre_genero',]

    def __str__(self):
        return f'{self.nombre_genero}'

    def save(self, *args, **kwargs):
        self.nombre_genero = self.nombre_genero.upper()
        super(Genero, self).save(*args, **kwargs)
    
class Autor(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    apellido = models.CharField(verbose_name='Apellido', max_length=100)
    fecha_nacimiento = models.DateTimeField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autors'

    def __str__(self):
        return f'{self.apellido} {self.nombre}'
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Autor, self).save(*args, **kwargs)

class Libro(models.Model):
    titulo = models.CharField(verbose_name='Titulo', max_length=150)
    autor = models.ForeignKey(Autor, on_delete = models.SET_NULL, null=True)
    genero = models.ForeignKey(Genero, on_delete = models.SET_NULL, null=True)
    editorial = models.CharField(verbose_name='Etitorial', max_length=150)
    precio = models.DecimalField(verbose_name='Precio', default=0, max_digits=10, decimal_places=2)
    portada = models.ImageField(verbose_name='Portada', upload_to='media/portada/%Y/%m/%d')
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        unique_together = ['titulo',]

    def __str__(self):
        return f'{self.titulo}'
    
    def save(self, *args, **kwargs):
        self.titulo = self.titulo.upper()
        self.editorial = self.editorial.upper()
        super(Genero, self).save(*args, **kwargs)