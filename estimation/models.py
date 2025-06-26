from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from django.db import models

class Accessibilite(models.Model):
    nom = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'accessibilites'
        verbose_name = "Accessibilité"
        verbose_name_plural = "Accessibilités"
    
    def __str__(self):
        return self.nom

class Type(models.Model):
    nom = models.CharField(max_length=20)
    logement = models.CharField(max_length=20)  # "appartement" ou "maison"
    
    class Meta:
        db_table = 'types'
        verbose_name = "Type de logement"
        verbose_name_plural = "Types de logement"
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'logement'],
                name='unique_type_logement'
            )
        ]
    
    def __str__(self):
        return f"{self.logement} {self.nom}"
    
class Type_papier(models.Model):
    nom = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'types_papiers'
        verbose_name = "Type de papiers"
        verbose_name_plural = "Type de papiers"
    
    def __str__(self):
        return self.nom

class Commodite(models.Model):
    nom = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'commodites'
        verbose_name = "Commodité"
        verbose_name_plural = "Commodités"
    
    def __str__(self):
        return self.nom
    
class Maison(models.Model):
    ville = models.CharField(max_length=20, verbose_name=_("Ville"))
    accessibilite = models.ForeignKey(
        Accessibilite,
        on_delete=models.PROTECT,
        db_column='accessibilite'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        db_column='type'
    )
    
    commodite = models.ManyToManyField(
        Commodite,
        related_name='maisons',
        db_table='maison_commodites'
    )

    nb_chambres = models.IntegerField()
    prix = models.IntegerField()
    
    class Meta:
        db_table = 'maisons'
        verbose_name = "Maison"
        verbose_name_plural = "Maisons"
    
    def __str__(self):
        return f"{self.type} à {self.ville} - {self.prix}€"

class Terrain(models.Model):
    ville = models.CharField(max_length=20, verbose_name=_("Ville"))
    type_papier = models.ForeignKey(
        Type_papier,
        on_delete=models.PROTECT,
        db_column='type_papier'
    )
    accessibilite = models.ForeignKey(
        Accessibilite,
        on_delete=models.PROTECT,
        db_column='accessibilite'
    )
    est_cloture = models.BooleanField(default=False, verbose_name="Clôturé")
    est_pret_a_construire = models.BooleanField(
        default=False,
        verbose_name="Prêt à construire"
    )
    prix = models.IntegerField()
    
    class Meta:
        db_table = 'terrains'
        verbose_name = "Terrain"
        verbose_name_plural = "Terrains"
    
    def __str__(self):
        return f"Terrain {self.superficie}m² à {self.ville} - {self.prix}€"