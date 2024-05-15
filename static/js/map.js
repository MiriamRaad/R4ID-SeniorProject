
        // Initialize and add the map
        function initMap() {
            // Specify the latitude and longitude
            var myLatLng = {lat: 34.39078691, lng: 35.84897117};

            // Create a map centered at the specified location
            var map = new google.maps.Map(
                document.getElementById('map'), {zoom: 15, center: myLatLng});

            // Add a marker at the specified location
            var marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                title: 'Your Marker Title'
            });
        }

