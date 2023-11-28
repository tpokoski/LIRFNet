    // Initialize the map and set its view to a given place and zoom
    const map = L.map('map').setView([40.4478, -104.6368], 18);

    // Add a tile layer to the map
    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    const info = L.control();

    info.onAdd = function(map) {
        this._div=L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    info.update = function(props) {
        const contents = props ? `<b>${props.Plot}</b><br />${props.irrigation} treatment` : 'Hover over a plot';
        this._div.innerHTML = `<h4>LIRF</h4>${contents}`;
    };

    info.addTo(map);
    





    var googleLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
    }).addTo(map);


    var imageryLayer = L.tileLayer.wms("http://ows.terrestris.de/osm/service?", {
        layers: 'OSM-WMS',
        format: 'image/png',
        transparent: true,
        attribution: "Terrestris"
    }).addTo(map);

    const lineast = L.geoJson(lirfgeo, {style:styleFunc, onEachFeature}).addTo(map);
   
    var baseLayers = {
        "Map": imageryLayer,
        "Satellite": googleLayer
    };
    var overlay = {
        "Linear East": lineast
    }
    L.control.layers(baseLayers,overlay).addTo(map);

 

    function getColor(d) {
        console.log(d)
        return d === 'FF' ? '#FFFF00' :
               d === "EL"  ? '#C65911' :
               d === "SF"  ? '#BF8F00' :
               d === "SL"  ? '#FCE4D6' :
               d === "DH"  ? '#00B0F0' :
               d === "DL"   ? '#B4C6E7' :
               d === "RH"   ? '#548235' :
               d === "RL"   ? '#A9D08E' :
                          '#FFEDA0';
    }
    function styleFunc(feature) {
        return {
            fillOpacity: 0.7,
            weight: 2,
            opacity: 0.5,
            color: '#666',
            dashArray: '3',
            fillColor: getColor(feature.properties.irrigation)
        };
    }


    function highlightFeature(e) {
		const layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#FFFFFF',
			dashArray: '',
			fillOpacity: 0.7
		});

		layer.bringToFront();
        info.update(layer.feature.properties);

	}

    function resetHighlight(e) {
		lineast.resetStyle(e.target);
        info.update();
	}

	function zoomToFeature(e) {
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}
   

