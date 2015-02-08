import os
from django.contrib.gis.utils import LayerMapping
from models import Region, Province, City
import map


region_mapping = {
    'name': 'NOMCOM',
    'mpoly': 'MULTIPOLYGON',

}

region_shp = os.path.abspath(os.path.join(os.path.dirname(map.__file__), 'static/shp/cat_comarcas_31NETRS89.shp'))

def run_region(verbose=True):
    lm = LayerMapping(Region, region_shp, region_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

province_mapping = {
    'name': 'NAME_2',
    'mpoly': 'MULTIPOLYGON',

}

province_shp = os.path.abspath(os.path.join(os.path.dirname(map.__file__), 'static/shp/ESP_adm/ESP_adm2.shp'))

def run_province(verbose=True):
    lm = LayerMapping(Province, province_shp, province_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)

city_mapping = {
    'name': 'NOM_MUNI',
    'mpoly': 'MULTIPOLYGON',

}

city_shp = os.path.abspath(os.path.join(os.path.dirname(map.__file__), 'static/shp/cat_municipios.shp'))

def run_city(verbose=True):
    lm = LayerMapping(City, city_shp, city_mapping,
                      transform=False, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)


