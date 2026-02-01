"""
Interactive map generator for Leeghwaterplas (Almere).

Creates an HTML map with useful controls for exploring and tracing
walking paths around the lake.

Run:
	python IntMap.py

Output:
	leeghwaterplas_map.html
"""
from __future__ import annotations

from pathlib import Path
import folium
from folium.plugins import MeasureControl, Draw, LocateControl
import base64
import shutil
from PIL import Image
from io import BytesIO


def load_images_to_map(marker_images_paths):
	"""Load images from paths and return a map of base64 encoded strings."""
	image_map = {}
	for name, paths in marker_images_paths.items():
		img_srcs = []
		for img_path in paths:
			if img_path.exists():
				try:
					img = Image.open(img_path)
					img.thumbnail((400, 400))  # Resize
					buffer = BytesIO()
					format_type = 'JPEG' if img_path.suffix.lower() in ['.jpg', '.jpeg'] else 'PNG'
					img.save(buffer, format=format_type)
					encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
					img_srcs.append(f"data:image/{format_type.lower()};base64,{encoded}")
				except Exception as e:
					print(f"Failed to process {img_path}: {e}")
					img_srcs.append("https://via.placeholder.com/180x120.jpg")
			else:
				img_srcs.append("https://via.placeholder.com/180x120.jpg")
		image_map[name] = img_srcs
	return image_map


def build_map(output: str | Path = "leeghwaterplas_map.html") -> Path:
	# Center coordinates for Leeghwaterplas, Almere (approximate)
	center = (52.38317, 5.23377)

	m = folium.Map(location=center, zoom_start=15, control_scale=True)

	# Base layers
	folium.TileLayer(
		"OpenStreetMap",
		name="Street",
		attr="© OpenStreetMap contributors",
	).add_to(m)
	folium.TileLayer(
		"Stamen Terrain",
		name="Terrain",
		attr=(
			"Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors"
		),
	).add_to(m)
	folium.TileLayer(
		"Stamen Toner",
		name="Toner",
		attr=(
			"Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors"
		),
	).add_to(m)
	# Satellite (ESRI)
	folium.TileLayer(
		tiles=(
			"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
		),
		name="Satellite",
		attr="Tiles © Esri — Source: Esri, DigitalGlobe, Earthstar Geographics",
		control=True,
	).add_to(m)

	# Marker for lake center
	folium.Marker(
		location=center,
		popup=folium.Popup("Leeghwaterplas", max_width=250),
		icon=folium.Icon(color="blue", icon="info-sign"),
	).add_to(m)

	# Points of interest and recreational facilities around Leeghwaterplas
	# Format: (location, name, color)
	poi_markers = [
		((52.383042, 5.226031), "Potentieel skatepark", "purple", "Dit is een prachtige locatie om een skatepark te bouwen, dicht bij de Leeghwaterplas en omgeven door groen. Het zou een geweldige toevoeging zijn voor de lokale gemeenschap en skaters van alle niveaus aantrekken. Hieronder de AI-impressie van een skate- en sportpark! Als het skatepark gerealiseerd wordt, zou er ook een 'Wall of Fame' kunnen komen om legaal grafitti te doen! Dit zou de hangplek mogelijk ook netter achterlaten."),
		((52.385084372447785, 5.231053016061975), "Voetbalveldje 1", "green", "Een voetbalveldje waar niet veel liefde aan geschonken wordt. De hangplek ernaast maakt het juist aantrekkelijk om naartoe te gaan, omdat je spullen daar kwijt kan terwijl je een balletje trapt. Door dit veldje op te knappen en beter te onderhouden, kan het een leuke plek worden om samen te komen en te sporten."),
		((52.384948830666964, 5.230788086557764), "Hangplek", "red", "Er wordt aangegeven dat de jongeren die hier komen, hun afval netjes in zakken doen die te groot zijn voor de prullenbak ernaast. Hierdoor pikken de vogels de zakken open en ontstaat er vooralsnog rotzooi die niet opgeruimd wordt. Het zou helpen als er meer en grotere prullenbakken geplaatst worden, zodat het afval direct in de bak kan worden gegooid en niet op de grond terechtkomt. Daarnaast zou een lakje verf op de bankjes en tafels de plek een stuk gezelliger maken."),
		((52.38433374080158, 5.2265479223225775), "Voetbalveldje 2", "green", "Het voetbalveldje voor de jongere kinderen die nog niet zo ver kunnen trappen. Voor deze leeftijdsgroep is het leuk om dit voetbalveldje te behouden, maar dat vraagt wel naar meer onderhoud."),
		((52.38359793506318, 5.226425716425748), "Voetbalveldje 3", "green", "Ons meest populaire veld! Bij een interview is naar voren gekomen dat dit vroeger een basketbalveld en voetbalveld in één was! (Het staat op google maps bijv. ook als basketbalveld aangeduid). Als wij de basketbalringen weer terugkunnen krijgen op dit veld, zou het de jongeren een stuk meer aantrekken!"),
		((52.383354830748196, 5.226486407880928), "Mini ramp Waterwijk", "green", "Deze kleine ramp kan in onze ogen weg, als het skatepark gerealiseerd wordt. Wat er dan voor in de plaats komt? Misschien wat bankjes, de 'Wall of Fame' voor grafitti, of een plek om te rusten langs het water!"),
		((52.38321450500632, 5.22893373521717), "Derde waterbrug", "beige", "Derde waterbrug is een grote brug die de eilanden van Leeghwaterplas met elkaar verbindt. Vanaf de brug heb je een prachtig uitzicht!"),
		((52.38499231701249, 5.228897594059279), "Speeltuin Leeghwaterpad", "green", "Dit speeltuintje bestaat uit twee speel onderdelen, met veel sport apparatuur van de sport wandelroute die door Leeghwaterplas heen verspreid is."),
		((52.384585484880404, 5.226733398543588), "Speeltuin Lekstraat", "green", "Dit speeltuintje bestaat uit twee speel onderdelen, met veel sport apparatuur van de sport wandelroute die door Leeghwaterplas heen verspreid is."),
		((52.384828522088235, 5.241236654816445), "Jeugdland Almere-Stad", "green", "Jeugdland Almere-Stad is voor kinderen tussen de 2 en 14 jaar oud, dus helaas past onze doelgroep daar niet meer bij."),
		((52.38081268315322, 5.234542754595652), "Hannie Schaftpark", "darkgreen", "Hannie Schaftpark heeft verrschillende bosvakken, maar ook open gedeeltes met dieren van Stadsboerderij De Kemphaan!"),
		((52.38422690678109, 5.239685202707825), "Bos der Onverzettelijken", "darkgreen", " 'Het geven van invulling aan de uitvoering van de verantwoordelijkheden van de gemeente Almere, voortvloeiend uit het convenant van 29 april 1993 en tevens de rol overneemt van de in het convenant genoemde 'begeleidingscomissie' van de Stichting Samenwerkend Verzet.' "),
		((52.384226906789316, 5.225214172870135), "Buurtcentrum De Draaikolk", "beige", "Een plek om samen te komen, waar momenteel weinig tot geen activiteiten voor jongeren georganiseerd worden. Door bijvoorbeeld een moestuin aan te leggen naast het buurtcentrum (waar al ruimte voor vrijgemaakt is), meer activiteiten te organiseren door het jaar heen en de mogelijkheid aan te bieden om binnen te wandelen kan dit buurtcentrum een ontmoetingsplek worden voor jongeren! Zo blijven ze niet buiten de deur hangen."),
		((52.38317, 5.23377), "Leeghwaterplas", "blue", "Onze gekozen locatie om aantrekkelijk te maken voor jongeren tussen de 17 en 24 jaar!"),
		((52.38521877325971, 5.23229183072874), "Steiger Leeghwaterplas", "beige", "Een bootje aanleggen of het water inspringen? Vanaf de grootste steiger in Leeghwaterplas kan het! Er zijn meerdere steigers op deze locatie, maar dit is wel de meest aantrekkelijke!"),
	]

	# Marker images: name -> list of paths
	marker_image_paths = {
		"Buurtcentrum De Draaikolk": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\buurtcenrtum_resized.jpg"), Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\BC_binnen.jpg"), Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\BC_bar.jpg")],
		"Hannie Schaftpark": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\hannie-schaftpark.png")],
		"Jeugdland Almere-Stad": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Jeugdland.jpg")],
		"Bos der Onverzettelijken": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\bos_onverzettelijk_resized.jpg")],
		"Leeghwaterplas": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Leeghwaterplas.jpg")],
		"Steiger Leeghwaterplas": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Steiger.jpg"), Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\steiger_personen.jpg")],
		"Speeltuin Leeghwaterpad": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\speeltuintje.jpg")],
		"Speeltuin Lekstraat": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\bokspringen.jpg")],
		"Hangplek": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\hangplek.jpg")],
		"Voetbalveldje 1": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\voetbalveldje1.jpg")],
		"Voetbalveldje 2": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Voetbalveldje2.jpg")],
		"Voetbalveldje 3": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Voetbalveldje3.jpg")],
		"Mini ramp Waterwijk": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\mini_ramp.jpg")],
		"Derde waterbrug": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Derde_brug.jpg")],
		"Potentieel skatepark": [Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\Before_skatepark.jpg"), Path(r"C:\Users\Jermaine P\source\repos\Leeghwaterplas_Interactive_Map\Images_Leegh\skatepark_mini.jpg")],
	}

	# Load images into a map of base64 strings
	image_map = load_images_to_map(marker_image_paths)

	for (lat, lon), name, color, description in poi_markers:
		if name in image_map:
			img_srcs = image_map[name]
			html = f"<b>{name}</b><br><small>{description}</small><br>" + "<br>".join(f'<img src="{src}" width="280" alt="{name} image">' for src in img_srcs)
			iframe = folium.IFrame(html, width=300, height=300)
			popup = folium.Popup(iframe, max_width=350)
		else:
			html = f"<b>{name}</b><br><small>{description}</small>"
			iframe = folium.IFrame(html, width=300, height=200)
			popup = folium.Popup(iframe, max_width=350)
		folium.Marker(
			location=(lat, lon),
			popup=popup,
			icon=folium.Icon(color=color, icon="info-sign"),
		).add_to(m)

	# Useful plugins for walking-path exploration
	MeasureControl(position="topleft", primary_length_unit="meters").add_to(m)
	Draw(export=True, filename="drawn_paths.geojson", position="topleft").add_to(m)
	LocateControl().add_to(m)

	folium.LayerControl(collapsed=False).add_to(m)

	out_path = Path(output)
	m.save(out_path)
	return out_path


if __name__ == "__main__":
    out = build_map()
    print(f"Map saved to: {out}")

