import numpy as np
import math
from utm.conversion import from_latlon, to_latlon
from django.contrib.gis.geos import GEOSGeometry
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


np.set_printoptions(threshold=np.nan)

def ed50_to_etrs89(x, y):
    """
    This function converts ed50 coordinates to etrs89
    Based on icc.cat info
    """

    # Define vars
    Tx = -129.549
    Ty = -208.185
    variation = 0.0000015504
    alpha = -1.56504/3600*math.pi/180  # toRadians

    # Define matrix
    traslation_matrix = np.array([Tx, Ty])
    rotate_matrix = np.array([[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]])
    starter_matrix = np.array([x, y])
    variation_matrix = (1 + variation)

    # Final Matrix calc
    A = np.transpose(np.dot(rotate_matrix, starter_matrix))
    BA = variation_matrix * A
    final_matrix = traslation_matrix + BA
    xf, yf = final_matrix[0], final_matrix[1]

    return xf, yf


def point_to_wgs84(point, srid=None):
    """
    return wgs84 coords, etr89-wgs84 deprecated
    """
    x = point.x
    y = point.y

    #Conversion to utm coords to transform it
    utm = from_latlon(y, x)
    zone = utm[2]
    zone_letter = utm[3]

    if zone == 31 or zone == 30:
        y, x = utm[0], utm[1]
    else:
        raise Exception(" This coords are not in 31T or 30T")

    if srid == 'ED50':
        x, y = ed50_to_etrs89(x, y)

    # Back to geographic
    y, x = to_latlon(y, x, zone, zone_letter)
    point = 'POINT({0} {1})'.format(x, y)
    point = GEOSGeometry(point)

    return point

def put_in_one_region():
    """
    Return a dict with the correct values for regions
    """
    from .models import Region
    regions = Region.objects.all()
    region_dict = {}
    for i in regions:
        if region_dict.has_key(i.name):
            mpoly = region_dict[i.name]
            mpoly += i.mpoly
            region_dict.update({i.name: mpoly})
        else:
            region_dict.update({i.name: i.mpoly})

    return region_dict

def truncate_region_objects():
    """
    Truncate the repeated regions
    """
    from .models import Region
    region_dict = put_in_one_region()
    regions = Region.objects.all()
    for i in regions:
        i.delete()

    for key, value in region_dict.items():
        region = Region(name=key, mpoly=value)
        region.save()
    if len(region_dict) == 41:
        logger.info('Database successfully modified!')
    else:
        logger.error('Some error has occurred')

def cities_to_wgs84_and_geographic():
    """
    Put all cities in geographic coordinates and wgs84
    """
    from map.models import City
    from django.contrib.gis.geos import MultiPolygon, Polygon
    cities = City.objects.all()
    for city in cities:
        coords = []
        for coord in city.mpoly.coords[0][0]:
            x = coord[0]
            y = coord[1]
            x, y = ed50_to_etrs89(x, y)
            x, y = to_latlon(x, y, 31, northern=True)
            coord = (y, x)
            coords.append(coord)
        poly = Polygon(tuple(coords))
        city.mpoly = MultiPolygon(poly)
        city.save()
        print(u'{0} Saved!'.format(city.name))

    logger.info('Transform success!')

def regions_to_geographic():
    """
    Put all regions in geographic coordinates
    """
    from map.models import Region
    from django.contrib.gis.geos import MultiPolygon, Polygon

    regions = Region.objects.all()
    for region in regions:
        coords = []
        for coord in region.mpoly.coords[0][0]:
            x = coord[0]
            y = coord[1]
            x, y = to_latlon(x, y, 31, northern=True)
            coord = (y, x)
            coords.append(coord)
        poly = Polygon(tuple(coords))
        region.mpoly = MultiPolygon(poly)
        region.save()
        print(u'{0} Saved!'.format(region.name))


def create_catalonia_provinces():
    """
    Create Catalonia provinces based on regions
    """
    from map.models import Province
    provinces = Province.objects.all()
    for province in provinces:
        if province.name == 'Barcelona' or province.name == 'Tarragona' or province.name == 'Lleida' or province.name == 'Girona':
            continue
        else:
            province.delete()









