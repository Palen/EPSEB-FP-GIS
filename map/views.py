from django.shortcuts import render_to_response, HttpResponse
from django.template.context import RequestContext
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import JobForm, FilterForm
from .models import Job, JobType
import json


def home(request):
    """
    Main view, If request = get show all objects, else filter by form.
    """
    jobs = Job.objects.all()
    jobs_list = [json.dumps({"id": job.pk, "type": "Point", "coordinates": list(job.to_wgs84.coords)}) for job in jobs]
    filter_form = FilterForm()

    context = {
        'jobs_list': jobs_list,
        'filter_form': filter_form
    }

    return render_to_response('index.html', context, RequestContext(request))


@login_required()
def add(request):
    """
    Add new object to DB, only for staff
    """
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            day = '-01'
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            s_first_name = form.cleaned_data['s_first_name']
            s_last_name = form.cleaned_data['s_last_name']
            desc = form.cleaned_data['desc']
            url = form.cleaned_data['url']
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            teachers = form.cleaned_data['teachers']
            srid = form.cleaned_data['srid']
            job_type = form.cleaned_data['job_type']
            date = form.cleaned_data['date'] + day
            x = form.cleaned_data['longitude']
            y = form.cleaned_data['latitude']

            # if transform is True we will transform to geographic from utm
            transform = True if 100000 <= x < 10000000 and 0 <= y <= 10000000 else False

            point = 'POINT({0} {1})'.format(x, y)
            point = GEOSGeometry(point, srid=int(srid))
            new_job = Job(first_name=first_name, last_name=last_name, s_first_name=s_first_name,
                          s_last_name=s_last_name, title=title, desc=desc,
                          url=url, point=point, srid=str(srid), image=image, job_type=job_type, date_time=date)
            new_job.save()
            new_job.teacher.add(*teachers)

            if transform:
                new_job.point.transform(4326)
                new_job.srid = '4326'
                new_job.save()

            return render_to_response('exito.html', context_instance=RequestContext(request))
        else:
            return render_to_response('add.html', {'form': form}, context_instance=RequestContext(request))

    else:
        form = JobForm()
        return render_to_response('add.html', {'form': form}, context_instance=RequestContext(request))


def ajax_get_initial_data(request):
    """
    Get initial data through ajax
    :param request:
    :return: Json Response
    """

    if request.method == 'GET':

        jobs = Job.objects.all()
        jobs_list = []
        for job in jobs:
            jobs_list.append(
                {
                    "type": "Feature",
                    "properties": {
                        "jobType": job.job_type.var_name,
                        "id": str(job.pk),

                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": list(job.point.coords),

                    }

                }
            )

        job_types = JobType.objects.all()
        job_types_list = []
        for job_type in job_types:
            job_types_list.append(
                {
                    "var_name": job_type.var_name,
                    "name": job_type.name,
                    "iconUrl": job_type.icon_url,
                    "shadowUrl": job_type.shadow_url,
                    "iconSize": job_type.icon_size,
                    "iconAnchor": job_type.icon_anchor,
                    "popupAnchor": job_type.popup_anchor,
                    "shadowSize": job_type.shadow_size,
                    "used": True if job_type.job_set.all() else False
                })
        context = {"jobs": jobs_list, "jobType": job_types_list, "response": "OK"}
    else:
        context = {"response": "error", "message": "Only allowed GET method"}

    return HttpResponse(json.dumps(context), content_type="application/json")


def ajax_get_job_properties(request):
    """
    Returns job data to ajax function
    :param request:
    :return: Json response with Job data
    """
    context = {}
    if request.method == 'GET' and request.GET.get('data', None):
        data = json.loads(request.GET['data'])
        job_id = data['id']
        try:
            job = Job.objects.get(pk=int(job_id))
            context['job'] = {
                'title': job.title,
                'jobType': job.job_type.name,
                'latitude': str(job.to_wgs84.y),
                'longitude': str(job.to_wgs84.x),
                'url': job.url,
                'description': job.desc,
                'image': job.image.url if job.image else None,
                'student': {'name': job.first_name, 'lastName': job.last_name},
                'studentB': {'name': job.s_first_name, 'lastName': job.s_last_name} if job.s_first_name else None,
                'teachers': [teacher.first_name + ' ' + teacher.last_name for teacher in job.teacher.all()]
            }
            context['response'] = 'OK'
        except ObjectDoesNotExist:
            context['response'] = 'error'
            context['message'] = 'Impossible to find the job'
    else:
        context['response'] = 'error'
        context['message'] = 'Only allowed GET method'
    return HttpResponse(json.dumps(context), content_type="application/json")


def ajax_get_form_data(request):
    filtered_jobs = []
    jobs = Job.objects.all()
    if request.method == 'POST':

        filter_form = FilterForm(request.POST)

        if filter_form.is_valid():

            region_poly = filter_form.cleaned_data.get('region_name', None)
            city_poly = filter_form.cleaned_data.get('city_name', None)
            province_poly = filter_form.cleaned_data.get('province_name', None)

            if region_poly:
                for region in region_poly:
                    [filtered_jobs.append(x) for x in jobs.filter(point__intersects=region.mpoly)]
            if city_poly:
                for city in city_poly:
                    [filtered_jobs.append(x) for x in jobs.filter(point__intersects=city.mpoly)]
            if province_poly:
                for province in province_poly:
                    [filtered_jobs.append(x) for x in jobs.filter(point__intersects=province.mpoly)]

            jobs = list(set(filtered_jobs)) if filtered_jobs else []
            region_poly = list(region_poly)
            city_poly = list(city_poly)
            province_poly = list(province_poly)
            jobs_list = []
            for job in jobs:
                jobs_list.append(
                    {
                        "type": "Feature",
                        "properties": {
                            "jobType": job.job_type.var_name,
                            "id": str(job.pk),

                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": list(job.point.coords),

                        }

                    }
                )
            region_list = []
            for region in region_poly + city_poly + province_poly:
                region_list.append({
                    "type": "Feature",
                    "properties": {
                        "type": region.__class__.__name__
                    },
                    "geometry": json.loads(region.mpoly.geojson)
                })

            context = {'jobs': jobs_list,
                       'regions': region_list,
                       'response': 'OK'
            }
        else:
            context = {'response': 'error', 'message': 'Form is not valid'}
    else:
        context = {'response': 'error', 'message': 'Only allowed GET method'}

    return HttpResponse(json.dumps(context), content_type="application/json")
