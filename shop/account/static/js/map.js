document.addEventListener("DOMContentLoaded", function () {

    const addressInput = document.getElementById("address");
    const currentLocationBtn = document.getElementById("currentLocationBtn");
    const locationCaptured = document.getElementById("locationCaptured");
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");

    /*
    |--------------------------------------------------------------------------
    | Default location
    |--------------------------------------------------------------------------
    | Kathmandu, Nepal
    */

    const defaultLat = 27.7172;
    const defaultLng = 85.3240;


    /*
    |--------------------------------------------------------------------------
    | Create Leaflet map
    |--------------------------------------------------------------------------
    */

    const map = L.map("locationMap").setView(
        [defaultLat, defaultLng],
        13
    );


    /*
    |--------------------------------------------------------------------------
    | OpenStreetMap tiles
    |--------------------------------------------------------------------------
    */

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);


    /*
    |--------------------------------------------------------------------------
    | Marker
    |--------------------------------------------------------------------------
    */

    let marker = null;


    /*
    |--------------------------------------------------------------------------
    | Select location
    |--------------------------------------------------------------------------
    */

    function selectLocation(lat, lng) {

        latitudeInput.value = lat;
        longitudeInput.value = lng;

        /*
        | Move map
        */

        map.setView([lat, lng], 17);


        /*
        | Create marker if it doesn't exist
        */

        if (marker) {

            marker.setLatLng([lat, lng]);

        } else {

            marker = L.marker([lat, lng], {
                draggable: true
            }).addTo(map);

            /*
            | If user drags marker
            */

            marker.on("dragend", function (event) {

                const position = event.target.getLatLng();

                selectLocation(
                    position.lat,
                    position.lng
                );

            });
        }


        /*
        | Reverse geocode
        */

        getAddressFromCoordinates(lat, lng);
    }


    /*
    |--------------------------------------------------------------------------
    | Reverse geocoding
    |--------------------------------------------------------------------------
    */

    async function getAddressFromCoordinates(lat, lng) {

        try {

            addressInput.placeholder = "Finding address...";

            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`,
                {
                    headers: {
                        "Accept": "application/json"
                    }
                }
            );


            if (!response.ok) {
                throw new Error("Unable to find address");
            }


            const data = await response.json();


            /*
            | Full formatted address
            */

            if (data.display_name) {

                addressInput.value = data.display_name;

            }


            addressInput.placeholder =
                "House no., street, area";


            /*
            | Show success
            */

            locationCaptured.style.display = "inline-flex";


        } catch (error) {

            console.error(
                "Reverse geocoding error:",
                error
            );

            addressInput.placeholder =
                "House no., street, area";

            locationCaptured.style.display = "inline-flex";
        }
    }


    /*
    |--------------------------------------------------------------------------
    | Click on map
    |--------------------------------------------------------------------------
    */

    map.on("click", function (event) {

        const lat = event.latlng.lat;
        const lng = event.latlng.lng;

        selectLocation(lat, lng);

    });


    /*
    |--------------------------------------------------------------------------
    | Use current location
    |--------------------------------------------------------------------------
    */

    currentLocationBtn.addEventListener(
        "click",
        function () {

            if (!navigator.geolocation) {

                alert(
                    "Your browser does not support location services."
                );

                return;
            }


            /*
            | Button loading state
            */

            currentLocationBtn.disabled = true;

            currentLocationBtn.innerHTML =
                `<span class="location-arrow">⌖</span>
                 Finding your location...`;


            /*
            | Browser GPS
            */

            navigator.geolocation.getCurrentPosition(

                function (position) {

                    const lat =
                        position.coords.latitude;

                    const lng =
                        position.coords.longitude;


                    selectLocation(lat, lng);


                    /*
                    | Restore button
                    */

                    currentLocationBtn.disabled = false;

                    currentLocationBtn.innerHTML =
                        `<span class="location-arrow">➤</span>
                         Use my current location`;

                },


                function (error) {

                    console.error(
                        "Location error:",
                        error
                    );


                    currentLocationBtn.disabled = false;

                    currentLocationBtn.innerHTML =
                        `<span class="location-arrow">➤</span>
                         Use my current location`;


                    if (error.code === 1) {

                        alert(
                            "Location permission was denied. Please allow location access in your browser."
                        );

                    } else if (error.code === 2) {

                        alert(
                            "Your location could not be determined. Please try again."
                        );

                    } else {

                        alert(
                            "Unable to get your current location. Please try again."
                        );
                    }

                },

                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        }
    );


    /*
    |--------------------------------------------------------------------------
    | Fix Leaflet rendering when map is inside dynamic layout
    |--------------------------------------------------------------------------
    */

    setTimeout(function () {

        map.invalidateSize();

    }, 300);

});