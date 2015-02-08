// A $( document ).ready() block.
$(document).ready(function () {

    // Avoiding see the usual multiselect
    $('.selectpicker').on('done', function() {
        $("#loader").fadeOut("slow");
        $("#form").removeClass('hide');
    });
    $('.selectpicker').selectpicker();

    // Init data
    var overlaysMaps = {};
    var layers = [];

    // Get initial data to charge on map
    $.ajax({
        url: "/ajax/init/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.response == "error") {
                alert(errorMessage);
                return;
            }
            // Adding jobTypes
            addJobTypesToMap(data.jobType, layers, overlaysMaps);

            // Create map global variable
            map = L.map('map', {
                layers: layers
            }).setView([41.38378, 2.11369], 8);
            var tile = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '<a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors | ' +
                    '<a href="http://albertpalenzuela.com">Albert Palenzuela</a>',
                maxZoom: 20,
                minZoom: 7

            }).addTo(map);

            // sideBar options
            sideBar = L.control.sidebar('sidebar', {
                position: "left"
            });
            map.addControl(sideBar);

            // Adding elements to map
            addElementsToMap(map, overlaysMaps);

            //Adding points to map
            addCoordsToMap(data.jobs, sideBar, "", layers);

            // Touching map hide sideBar
            map.on('click', function(){
                sideBar.hide();
            })
        },
        error: function()
        {
            alert(errorMessage);

        }
    });
    $("#coord_title").click(function(){
        $("#coord").toggle();
    });
    $("#student_title").click(function(){
        $("#student").toggle();
    });
    $("#tutor_title").click(function(){
        $("#teachers").toggle();
    });
    $("#description_title").click(function(){
        $("#description").toggle();
    });
    $("#url_title").click(function(){
        $("#url").toggle();
    });

    $("#submit").submit(function(e){
        submitFunction(e, $(this), layers)
    })

});
/**
 * Add jobTypes to layers with its control variable
 * @param jobTypes
 * @param layers
 * @param overlaysMaps
 */
function addJobTypesToMap(jobTypes, layers, overlaysMaps) {
    var controlRegion = new L.LayerGroup();
    layers.push(controlRegion);
    jobTypes.forEach(function (jobType) {
        switch (jobType.var_name) {
            case "arch":
                arch = L.icon({
                    iconUrl: jobType.iconUrl,
                    shadowUrl: jobType.shadowUrl,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                controlArch = new L.LayerGroup();
                layers.push(controlArch);
                var htmlImageArch = "<img src='{0}' class='icon_legend'/> <span class='my-layer-item'>{1}</span>".format(jobType.iconUrl, jobType.name);
                overlaysMaps[htmlImageArch] = controlArch;

                break;
            case "gis":
                gis = L.icon({
                    iconUrl: jobType.iconUrl,
                    shadowUrl: jobType.shadowUrl,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                controlGis = new L.LayerGroup();
                layers.push(controlGis);
                var htmlImageGis = "<img src='{0}' class='icon_legend'/> <span class='my-layer-item'>{1}</span>".format(jobType.iconUrl, jobType.name);
                overlaysMaps[htmlImageGis] = controlGis;
                break;
            case "civil":
                civil = L.icon({
                    iconUrl: jobType.iconUrl,
                    shadowUrl: jobType.shadowUrl,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                controlCivil = new L.LayerGroup();
                layers.push(controlCivil);
                var htmlImageCivil = "<img src='{0}' class='icon_legend'/> <span class='my-layer-item'>{1}</span>".format(jobType.iconUrl, jobType.name);
                overlaysMaps[htmlImageCivil] = controlCivil;
                break;
            case "geodesy":
                geodesy = L.icon({
                    iconUrl: jobType.iconUrl,
                    shadowUrl: jobType.shadowUrl,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                controlGeodesy = new L.LayerGroup();
                layers.push(controlGeodesy);
                var htmlImageGeodesy = "<img src='{0}' class='icon_legend'/> <span class='my-layer-item'>{1}</span>".format(jobType.iconUrl, jobType.name);
                overlaysMaps[htmlImageGeodesy] = controlGeodesy;
                break;
            default:
                return
        }


    });
}
/**
 * Add jobs to map with its assigned jobType based on control variables, if regions all markers will be removed
 * @param jobs
 * @param sideBar
 * @param regions
 * @param layers
 */
function addCoordsToMap(jobs, sideBar, regions, layers) {
    var controlRegion = layers[0];
    if (regions)
    {   layers.forEach(function(layer){
            layer.clearLayers();
        });
        regions.forEach(function(region){
            L.geoJson(region, {
                pointToLayer: function (feature, latlng) {
                    return L.marker(latlng)
                }
            }).addTo(controlRegion);
        })
    }
    jobs.forEach(function (job) {
        L.geoJson(job, {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: eval(job.properties.jobType), alt: job.properties.id})
            }
        }).addTo(eval("control" + job.properties.jobType.capitalize())).on('click', function(){
            getJobProperties(job.properties.id, sideBar)
        })
    });

}

/**
 * Add coordinates layer, scale and legend
 * @param map
 * @param overlaysMaps
 */
function addElementsToMap(map, overlaysMaps) {
    L.control.coordinates({
        position: "topright",
        decimals: 4,
        decimalSeperator: ".",
        labelTemplateLat: "Latitude: {y}",
        labelTemplateLng: "Longitude: {x} | WGS84",
        enableUserInput: true,
        useDMS: false,
        useLatLngOrder: true
    }).addTo(map);

    L.control.layers(null, overlaysMaps, {
        collapsed: false,
        position: 'bottomright',
        autoZIndex: true
    }).addTo(map);

    L.control.scale().addTo(map);

}

/**
 * Gets the Job properties and shows it on a modal side.
 * @param jobID
 * @param sideBar
 */
function getJobProperties(jobID, sideBar) {
    if (jobID) {
        $.ajax({
            url: "/ajax/getJob/",
            type: "GET",
            dataType: "json",
            data: {'data':JSON.stringify({id:jobID})},
            success: function(data){
                if (data.response == 'error')
                {
                    alert(errorMessage);
                    return
                }

                var job = data.job;
                var oldTitle = $('#title').text();
                $('#title').text(job.title);
                $('#job_type').text(job.jobType);
                $('#coord').text('Latitude: {0}° Longitude: {1}° | WGS84'.format(job.latitude, job.longitude));
                var studenP = '{0} {1}'.format(job.student.name, job.student.lastName);
                if (job.studentB)
                {
                 studenP += '<br>{0} {1}'.format(job.studentB.name, job.studentB.lastName);
                }
                $('#student').html(studenP);
                var teacherP = '';
                job.teachers.forEach(function(teacher){
                   teacherP += '{0}<br>'.format(teacher)
                });
                $('#teachers').html(teacherP);
                var url = $('#url');
                url.text(job.url);
                url.attr('href', job.url);
                $('#description').text(job.description);
                if ($('#sidebar').hasClass('hide'))
                {
                    $('#sidebar').removeClass('hide');
                }
                if (job.image)
                {
                    $('#image').attr('src', job.image);
                    $('#image_title').removeClass('hide');
                }
                else
                {
                    $('#image').attr('src', '');
                    $('#image_title').addClass('hide');
                }
                if(job.title == oldTitle)
                {
                    sideBar.hide();
                }
                else
                {
                   sideBar.show();
                }

            }


        })
    }
}

/**
 * Manage the logic of the filter form
 * @param e
 * @param form
 * @param layers
 */
function submitFunction(e, form, layers){
    e.preventDefault();
    $.ajax({
        url: "/ajax/form/",
        type: "POST",
        dataType: "json",
        data: form.serialize(),
        success:function (data)
        {
            if (data.response == 'error')
            {
                alert(errorMessage);
                return;
            }
            addCoordsToMap(data.jobs, sideBar, data.regions, layers);

        },
        error:function ()
        {
            alert(errorMessage);
        }
    })
}

/**
 * Prototypes the first letter to Cap
 * @returns {string}
 */
String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
};
/**
 * Adds the parse string format like Python
 * @returns {string}
 */
String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};
var errorMessage = 'Some error occurred, please refresh the page or contact with the administrator if the problem persists.(albert.palenzuela@gmail.com)';