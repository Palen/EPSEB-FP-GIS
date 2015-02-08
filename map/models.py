
from django.contrib.gis.db import models
from map.utils import point_to_wgs84


CHOICES_SRID = (
    ('4326', 'WGS84'),
    ('4258', 'ETRS89'),
    ('2061', 'ED50'),
    ('32631', 'WGS84/UTM31N'),
    ('25831', 'ETRS89/UTM31N'),
    ('23031', 'ED50/UTM31N')
)


class Job(models.Model):
    """
    Model to manage Job
    """
    # First Student data
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)

    # If necessary Second Student data
    s_first_name = models.CharField(max_length=50,  blank=True, null=True)
    s_last_name = models.CharField(max_length=50,  blank=True, null=True)

    #Techer relation
    teacher = models.ManyToManyField('Teacher',)

    # Jobs data
    title = models.CharField(max_length=300,)
    url = models.URLField()
    desc = models.TextField()
    job_type = models.ForeignKey('JobType', null=True)

    # Image only for Patrimonial
    image = models.ImageField(blank=True, null=True, upload_to='jobs/')

    # Datetime
    date_time = models.DateField(auto_now=False, default=None, null=True, blank=True)

    # Geodjango data
    point = models.PointField()

    #srid point
    srid = models.CharField(choices=CHOICES_SRID, max_length=5)

    # Objects override
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    def all_teachers(self):
        return ', '.join([obj.first_name for obj in self.teacher.all()])

    @property
    def to_wgs84(self):
        """
        Return WGS84 point object
        """
        if self.srid == '2061':
            point = point_to_wgs84(self.point, 'ED50')
        else:
            point = self.point

        return point

class Teacher(models.Model):
    """
    Model to manage teachers
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['first_name']

class JobType(models.Model):
    """
    Type of job, be aware the existing icon.
    """
    name = models.CharField(max_length=100)
    var_name = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

    # Define icons properties
    @property
    def icon_url(self):

        if self.name == 'Geodesy':
            icon_url = '../static/images/icons/geodesy-icon.png'
        elif self.name == 'Cartography and GIS':
            icon_url = '../static/images/icons/gis-icon.png'
        elif self.name == 'Civil Engineering':
            icon_url = '../static/images/icons/civil-icon.png'
        elif self.name == 'Architectural and Archaeological Survey':
            icon_url = '../static/images/icons/survey-icon.png'
        else:
            icon_url = 'images/icons/marker-icon.png'

        return icon_url

    @property
    def shadow_url(self):
        shadow_url = '../static/images/icons/marker-shadow.png'

        return shadow_url

    @property
    def icon_size(self):
        icon_size = '[25, 41]'

        return icon_size

    @property
    def icon_anchor(self):
        icon_anchor = '[12, 41]'

        return icon_anchor

    @property
    def popup_anchor(self):
        popup_anchor = '[1, -34]'

        return popup_anchor

    @property
    def shadow_size(self):
        shadow_size = '[41, 41]'

        return shadow_size


class Region(models.Model):
    """
    Define Region properties imported by .shp
    """
    name = models.CharField(max_length=50)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Province(models.Model):
    """
    Define Province properties imported by .shp
    """
    name = models.CharField(max_length=50)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class City(models.Model):
    """
    Define City properties imported by .shp
    """
    name = models.CharField(max_length=50)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']








