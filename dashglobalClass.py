elif selected == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    
    # Introduction to the Application
    st.markdown("""
    Aplikasi ini bertujuan untuk memberikan analisis data siswa secara interaktif. 
    Dengan menggunakan teknologi modern, aplikasi ini memungkinkan pengguna untuk 
    mengunggah data siswa, menganalisis performa mereka, dan mendapatkan wawasan 
    yang berharga melalui visualisasi data yang menarik. 
    """)

    # Purpose of the Application
    st.subheader("🎯 Tujuan Aplikasi")
    st.markdown("""
    Tujuan utama dari aplikasi ini adalah:
    - **Analisis Data Siswa**: Memberikan analisis mendalam mengenai performa siswa 
      berdasarkan berbagai metrik, termasuk GSE (Grade Scale Equivalent), IQ, dan 
      kemampuan bahasa.
    - **Interaktivitas**: Memungkinkan pengguna untuk berinteraksi dengan data 
      melalui fitur-fitur seperti pemilihan siswa, filter data, dan visualisasi yang 
      mudah dipahami.
    - **Rekomendasi**: Menyediakan saran dan rekomendasi berdasarkan analisis 
      untuk membantu pengambilan keputusan yang lebih baik dalam pendidikan.
    """)

    # Features of the Application
    st.subheader("✨ Fitur Utama")
    st.markdown("""
    - **Unggah Data**: Pengguna dapat mengunggah file Excel yang berisi data siswa 
      untuk analisis.
    - **Dashboard Interaktif**: Menyediakan tampilan ringkasan dari metrik penting 
      yang menunjukkan performa siswa secara keseluruhan.
    - **Visualisasi Data**: Berbagai jenis grafik dan diagram untuk membantu 
      memahami data dengan lebih baik.
    - **Analisis Siswa Terpilih**: Memungkinkan pengguna untuk melihat rincian 
      performa siswa tertentu dan mendapatkan rekomendasi yang sesuai.
    - **Korelasi**: Menampilkan hubungan antara berbagai metrik untuk analisis 
      yang lebih mendalam.
    """)

    # Technical Information
    st.subheader("🔧 Informasi Teknis")
    st.markdown("""
    Aplikasi ini dibangun menggunakan:
    - **Streamlit**: Framework untuk membangun aplikasi web berbasis data dengan 
      Python.
    - **Pandas**: Library untuk manipulasi dan analisis data.
    - **Matplotlib dan Seaborn**: Library untuk visualisasi data.
    - **Scikit-learn**: Digunakan untuk algoritma pembelajaran mesin seperti 
      clustering.
    - **WordCloud**: Library untuk membuat visualisasi kata dari komentar siswa.
    """)

    # Copyright Information
    st.subheader("© Hak Cipta")
    st.markdown("""
    Aplikasi ini dilindungi oleh undang-undang hak cipta. 
    Semua hak dilindungi. Dilarang memperbanyak, mendistribusikan, atau 
    menggunakan bagian dari aplikasi ini tanpa izin tertulis dari pemilik hak cipta. 
    Penggunaan aplikasi ini sepenuhnya untuk tujuan pendidikan dan analisis data. 
    Jika Anda memiliki pertanyaan atau memerlukan izin, silakan hubungi [email@example.com].
    """)

    # Closing Remarks
    st.markdown("""
    Terima kasih telah menggunakan aplikasi analisis data siswa ini. 
    Kami berharap aplikasi ini dapat membantu Anda dalam memahami dan 
    meningkatkan performa siswa. 
    """)

