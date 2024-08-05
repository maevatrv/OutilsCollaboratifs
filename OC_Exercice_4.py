import streamlit as st
from PIL import Image, PngImagePlugin
import piexif
import io

st.title("Editeur de métadonnées")

image_path = "photo_m.jpg"
photo = Image.open(image_path)

st.image(photo)

def get_data(photo):
    exif_dict= piexif.load(photo.info["exif"])
    return exif_dict

def update(photo, exif_data):
    exif_bytes = piexif.dump(exif_data)
    byte_io = io.BytesIO()
    photo.save(byte_io, format='JPEG', exif=exif_bytes)
    return byte_io.getvalue()

width, height = photo.size
caption = photo.info.get('caption')

new_caption = st.text_input("Titre", caption)
new_width = st.number_input("Largeur", value=width)
new_height = st.number_input("Hauteur", value=height)

info = PngImagePlugin.PngInfo()
if new_caption:   
    info.add_text("caption", new_caption)
if new_width or new_height:
    photo = photo.resize((new_width, new_height))
    
exif_data = get_data(photo)

artist = exif_data["0th"].get(piexif.ImageIFD.Artist)
artist = artist.decode('utf-8') if artist else ""
new_artist = st.text_input("Artiste", artist)
exif_data["0th"][piexif.ImageIFD.Artist] = new_artist.encode('utf-8')

make = exif_data["0th"].get(piexif.ImageIFD.Make)
make = make.decode('utf-8') if make else ""
new_make = st.text_input("Fabricant", make)
exif_data["0th"][piexif.ImageIFD.Make] = new_make.encode('utf-8')

model = exif_data["0th"].get(piexif.ImageIFD.Model)
model = model.decode('utf-8') if model else ""
new_model = st.text_input("Modèle", model)
exif_data["0th"][piexif.ImageIFD.Model] = new_model.encode('utf-8')

datetime_original = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
datetime_original = datetime_original.decode('utf-8') if datetime_original else ""
new_datetime_original = st.text_input("Date", datetime_original)
exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_datetime_original.encode('utf-8')

if st.button("Mettre à jour"):
    updated_data = update(photo, exif_data)
    st.download_button(
        label="Télécharger l'image",
        data=updated_data,
        file_name="photo_m_update.jpg",
        mime="image/jpeg"
    )