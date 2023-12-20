from PIL import Image
import io
import streamlit as st
import numpy as np
import tensorflow as tf
# import hydralit_components as hc
from streamlit_option_menu import option_menu 
from solutions.art import *

st.set_page_config(
        page_title="Trashure.ai",
        # layout="wide",
        # initial_sidebar_state="expanded",
        )

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('source/model.h5')
    class_names = np.load('source/nama_kelas.npy') 
    return model, class_names

def beranda():
    st.title('Trashure.ai')

    st.image("source/logo.png", width=200)

    st.markdown('''
    Selamat datang di **Trashure.ai**. Web ini mengeksplorasi dunia klasifikasi sampah yang memadukan 
    kecerdasan buatan dengan kepedulian lingkungan. Mari bergabung dalam petualangan memahami dan merawat 
    bumi kita dengan cara yang inovatif dan berkelanjutan. Temukan keajaiban di setiap sudut informasi dan 
    jadilah bagian dari revolusi hijau untuk masa depan yang lebih bersih! 🌍✨
    
    ## Tahukah Kamu

    Indonesia memproduksi sampah 36 juta ton pada tahun 2022 dan sebenarnya kita bisa mengurangi itu.
    
    ''')

    st.image("source/data.png")

    st.markdown("""
    Sumber: [SIPSN 2022](https://sipsn.menlhk.go.id/sipsn/)
    
    
    Kamu bisa mengurangi atau bahkan menggunakan kembali sampah menjadi kerajinan. Kami memperkenalkan
    model kami yang bernama **Trashure.ai** untuk membantu kamu mengolah sampah.

    ## Trashure.ai


    **Trashure.ai** merupakan model yang bisa mendeteksi sampah dan membantu kamu mengolah sampah tersebut.
    Kamu bisa memfoto sampah kamu di menu **Klasifikasi Sampah** dan AI ini akan membantu memberi referensi
    pengolahan dari sampah yang kamu foto. Namun, perlu diketahui bahwa AI ini tidak 100% akurat dan tidak
    semua sampah bisa dideteksi menggunakan model ini. Kamu tidak perlu khawatir. Model ini dilatih untuk 
    mengenali sampah secara umum.
    """)

def klasifikasi(model, class_names):
    st.markdown("## Foto Sampahmu")

    st.session_state['my_img'] = None
    treshold = .6

    option = st.selectbox(
        "Pilih pengambilan gambar",
        ["Upload foto", "Ambil foto"],
    )

    if option == "Upload foto":
        uploaded_file = st.file_uploader('Upload gambar sampah', type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            pil_image = Image.open(io.BytesIO(file_bytes))
            pil_image = pil_image.convert('RGB')
            st.session_state['my_img'] = pil_image

            st.image(pil_image)

            pil_image = pil_image.resize((299, 299))
            pil_image = np.array(pil_image) / 255.

            prediction = model.predict(np.expand_dims(pil_image, axis=0))
            index = np.argmax(prediction)

            confidence = prediction[0][index]

            if confidence >= treshold:
                st.success(f"Prediksi: {class_names[index]} {prediction[0][index]*100 :.2f}% ")
                solution(class_names[index], class_names)

            else:
                st.warning("Sampah tidak ditemukan")
                st.info("Coba perbaiki sudut kamera atau model mungkin belum mengenali sampah tersebut.")


    if option == "Ambil foto":
        image_captured = st.camera_input('')

        if image_captured:
            st.session_state['my_img'] = image_captured

        if st.session_state['my_img']:
            img_byte_array = st.session_state['my_img'].getvalue()
            img_np_array = np.frombuffer(img_byte_array, np.uint8)
            img = Image.open(io.BytesIO(img_np_array))
            img = img.resize((299, 299))
            img = np.array(img) / 255.

            prediction = model.predict(np.expand_dims(img, axis=0))
            index = np.argmax(prediction)

            confidence = prediction[0][index]

            if confidence >= treshold:
                st.success(f"Prediksi: {class_names[index]} {prediction[0][index]*100 :.2f}% ")
                solution(class_names[index], class_names)

            else:
                st.warning("Sampah tidak ditemukan")
                st.info("Coba perbaiki sudut kamera atau model mungkin belum mengenali sampah tersebut.")

    
def solution(nama_kelas_index, nama_kelas):
    if nama_kelas_index == nama_kelas[0]:
        kardus()

    if nama_kelas_index == nama_kelas[1]:
        kaca()

    if nama_kelas_index == nama_kelas[2]:
        kaleng()

    if nama_kelas_index == nama_kelas[3]:
        organic_fresh()

    if nama_kelas_index == nama_kelas[4]: 
        organic_common()

    if nama_kelas_index == nama_kelas[5]:
        organic_rot()

    if nama_kelas_index == nama_kelas[6]:
        kertas()

    if nama_kelas_index == nama_kelas[7]:
        gelas()

    if nama_kelas_index == nama_kelas[8]:
        kantong()

    if nama_kelas_index == nama_kelas[9]:
        botol()

    if nama_kelas_index == nama_kelas[10]:
        alat_makan()

def main():
    model, class_names = load_model()

    selected = option_menu(None, ['Beranda', 'Klasifikasi Sampah', 'Informasi Pengolahan Sampah'],
        icons=['house', 'circle-half', 'globe'],
        menu_icon='cast', 
        default_index=0, 
        orientation='horizontal'
    )

    if selected == 'Beranda':
        beranda()

    if selected == 'Klasifikasi Sampah':
        klasifikasi(model, class_names)
        

if __name__ == "__main__":
    main()