import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import numpy as np
from wordcloud import WordCloud

# Set page configuration
st.set_page_config(page_title="Analisis Lengkap Data Siswa", layout="wide")

# Custom CSS to enhance the appearance
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f5;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    .stDataFrame {
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu using streamlit-option-menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Dashboard", "Data Upload", "Visualisasi", "Tentang"],
        icons=["house", "upload", "bar-chart", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#ffffff"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "color": "black"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

# Initialize a variable to store the DataFrame globally
if 'df' not in st.session_state:
    st.session_state.df = None

# Function to convert GSE ranges to numeric values
def convert_gse_to_numeric(gse_value):
    mapping = {
        "Below Level": 1,
        "Level 1": 2,
        "Level 2": 3,
        "Level 3": 4,
        "Above Level": 5
    }
    return mapping.get(gse_value, np.nan)  # Return NaN if value not found

# Main content based on selected menu option
if selected == "Dashboard":
    st.title("📊 Dashboard Analisis Siswa")
    st.markdown("Selamat datang di dashboard kami! Di sini Anda dapat melihat analisis data secara interaktif.")

    if st.session_state.df is not None:
        # Convert 'GSE' values to numeric
        st.session_state.df['GSE'] = st.session_state.df['GSE'].apply(convert_gse_to_numeric)

        # Ensure other numeric columns are converted
        numeric_columns = ['Nilai_IQ', 'Listening', 'Reading', 'Speaking', 'Writing']
        for col in numeric_columns:
            st.session_state.df[col] = pd.to_numeric(st.session_state.df[col], errors='coerce')

        # Example metrics based on the uploaded data
        total_students = len(st.session_state.df)
        passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Lulus'])
        not_passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] != 'Lulus'])
        waiting_list_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Waiting List'])
        above_level_students = len(st.session_state.df[st.session_state.df['GSE'] > 3])  # Example threshold for GSE

        # Dashboard summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Siswa", total_students)
        with col2:
            st.metric("Lulus", passed_students)
        with col3:
            st.metric("Tidak Lulus", not_passed_students)
        with col4:
            st.metric("Waiting List", waiting_list_students)

        st.markdown(f"**Jumlah di atas level GSE 3**: {above_level_students}")

        # Display counts for each category
        st.subheader("📊 Rincian Kategori")
        unit_counts = st.session_state.df['Unit'].value_counts()
        kategori_counts = st.session_state.df['Kategori'].value_counts()
        
        st.markdown("### Rincian Unit")
        for unit, count in unit_counts.items():
            st.markdown(f"- **{unit}**: {count} siswa")

        st.markdown("### Rincian Kategori")
        for kategori, count in kategori_counts.items():
            st.markdown(f"- **{kategori}**: {count} siswa")

        # Recommendations for intervention
        with st.expander("Rekomendasi Aksi / Intervensi"):
            remedial_students = st.session_state.df[(st.session_state.df['GSE'] < 3) & (st.session_state.df['Unit'] == 'A')]
            count_remedial = len(remedial_students)
            if count_remedial > 0:
                st.markdown(f"**{count_remedial} siswa dari Unit A dengan GSE < 3 disarankan untuk mengikuti program remedial.**")
            else:
                st.markdown("Tidak ada siswa dari Unit A yang disarankan untuk program remedial.")

    else:
        st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")

elif selected == "Data Upload":
    st.title("📤 Unggah Data")
    uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])
    if uploaded_file:
        try:
            # Read the uploaded Excel file
            st.session_state.df = pd.read_excel(uploaded_file)
            st.success("File berhasil dimuat!")
            st.dataframe(st.session_state.df)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca data: {e}")

elif selected == "Visualisasi":
    st.title("📈 Visualisasi Data")
    st.markdown("Di sini Anda dapat melihat visualisasi data.")
    
    if st.session_state.df is not None:
        # Convert 'GSE' values to numeric
        st.session_state.df['GSE'] = st.session_state.df['GSE'].apply(convert_gse_to_numeric)
        # Ensure other numeric columns are converted
        numeric_columns = ['Nilai_IQ', 'Listening', 'Reading', 'Speaking', 'Writing']
        for col in numeric_columns:
            st.session_state.df[col] = pd.to_numeric(st.session_state.df[col], errors='coerce')
            
        # Filter data
        with st.expander("🔍 Filter Data", expanded=True):
            unit_opt = st.multiselect("Pilih Unit", st.session_state.df['Unit'].unique(), default=list(st.session_state.df['Unit'].unique()))
            kategori_opt = st.multiselect("Pilih Kategori", st.session_state.df['Kategori'].unique(), default=list(st.session_state.df['Kategori'].unique()))
            keterangan_opt = st.multiselect("Keterangan", st.session_state.df['Keterangan'].unique(), default=list(st.session_state.df['Keterangan'].unique()))

            df_filtered = st.session_state.df[
                st.session_state.df['Unit'].isin(unit_opt) &
                st.session_state.df['Kategori'].isin(kategori_opt) &
                st.session_state.df['Keterangan'].isin(keterangan_opt)
            ]

        st.subheader("📄 Data Tersaring")
        st.dataframe(df_filtered.style.set_table_attributes('style="width: 100%; border-collapse: collapse;"'), use_container_width=True)

        # Visualisasi CEFR & GSE
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📘 Distribusi CEFR")
            fig1, ax1 = plt.subplots()
            sns.countplot(data=df_filtered, x='CEFR', order=df_filtered['CEFR'].value_counts().index, palette='Set2', ax=ax1)
            ax1.set_title("Distribusi CEFR", fontsize=14)
            ax1.set_xlabel("CEFR", fontsize=12)
            ax1.set_ylabel("Jumlah", fontsize=12)
            st.pyplot(fig1)

            # Explanation for CEFR Distribution
            cefr_counts = df_filtered['CEFR'].value_counts()
            st.markdown(f"**Jumlah Siswa per CEFR**: {cefr_counts.to_dict()}")

        with col2:
            st.markdown("#### 📗 Distribusi GSE")
            fig2, ax2 = plt.subplots()
            sns.histplot(df_filtered['GSE'], bins=10, kde=True, color='green', ax=ax2)
            ax2.set_title("Distribusi GSE", fontsize=14)
            ax2.set_xlabel("GSE", fontsize=12)
            ax2.set_ylabel("Frekuensi", fontsize=12)
            st.pyplot(fig2)

            # Explanation for GSE Distribution
            st.markdown(f"**Rata-rata GSE**: {df_filtered['GSE'].mean():.2f}, **Nilai GSE Tertinggi**: {df_filtered['GSE'].max()}, **Nilai GSE Terendah**: {df_filtered['GSE'].min()}")

        # Kemampuan Bahasa (Listening, Reading, Speaking, Writing)
        st.markdown("#### 🗣️ Kemampuan Bahasa (Listening, Reading, Speaking, Writing)")
        skill_cols = ['Listening', 'Reading', 'Speaking', 'Writing']
        for col in skill_cols:
            st.markdown(f"##### {col}")
            fig, ax = plt.subplots()
            # Use histogram for continuous numeric data visualization
            sns.histplot(data=df_filtered, x=col, kde=True, color='skyblue', ax=ax)
            ax.set_title(f"Distribusi {col}", fontsize=14)
            ax.set_xlabel(col, fontsize=12)
            ax.set_ylabel("Frekuensi", fontsize=12)
            st.pyplot(fig)
            # Explanation for Language Skills
            skill_stats = df_filtered[col].describe()
            st.markdown(f"**Statistik {col}**: Mean={skill_stats['mean']:.2f}, Median={skill_stats['50%']:.2f}, Min={skill_stats['min']}, Max={skill_stats['max']}")

        # IQ & Kategori IQ
        st.markdown("#### 🧠 Distribusi IQ")
        col3, col4 = st.columns(2)
        with col3:
            fig3, ax3 = plt.subplots()
            sns.histplot(df_filtered['Nilai_IQ'], bins=10, kde=True, color='purple', ax=ax3)
            ax3.set_title("Distribusi IQ", fontsize=14)
            ax3.set_xlabel("Nilai IQ", fontsize=12)
            ax3.set_ylabel("Frekuensi", fontsize=12)
            st.pyplot(fig3)

            # Explanation for IQ Distribution
            st.markdown(f"**Rata-rata IQ**: {df_filtered['Nilai_IQ'].mean():.2f}, **IQ Tertinggi**: {df_filtered['Nilai_IQ'].max()}, **IQ Terendah**: {df_filtered['Nilai_IQ'].min()}")

        with col4:
            fig4, ax4 = plt.subplots()
            sns.countplot(data=df_filtered, x='Kategori', order=df_filtered['Kategori'].value_counts().index, palette='coolwarm', ax=ax4)
            ax4.set_title("Distribusi Kategori IQ", fontsize=14)
            ax4.set_xlabel("Kategori", fontsize=12)
            ax4.set_ylabel("Jumlah", fontsize=12)
            st.pyplot(fig4)

            # Explanation for IQ Categories
            kategori_counts = df_filtered['Kategori'].value_counts()
            st.markdown(f"**Jumlah Siswa per Kategori IQ**: {kategori_counts.to_dict()}")

        # Kemampuan Psikologis (T/ST)
        st.markdown("#### 🧩 Analisis Karakteristik Psikologis")
        char_cols = [col for col in st.session_state.df.columns if st.session_state.df[col].isin(['T', 'ST']).any()]
        if char_cols:
            psych_summary = df_filtered[char_cols].apply(lambda x: x.value_counts()).fillna(0).astype(int).T
            psych_summary.columns = ['ST', 'T']
            st.dataframe(psych_summary.style.set_table_attributes('style="width: 100%; border-collapse: collapse;"'))

            fig5, ax5 = plt.subplots(figsize=(10, 6))
            psych_summary.plot(kind='barh', stacked=True, color=['#ffa07a', '#20b2aa'], ax=ax5)
            ax5.set_title("Distribusi T vs ST", fontsize=14)
            ax5.set_xlabel("Jumlah", fontsize=12)
            ax5.set_ylabel("Karakteristik", fontsize=12)
            st.pyplot(fig5)

            # Explanation for Psychological Characteristics
            st.markdown(f"**Jumlah Karakteristik Psikologis**: {psych_summary.to_dict(orient='records')}")

        # Detailed Student View
        st.subheader("🔍 Rincian Siswa")
        selected_students = st.multiselect("Pilih Siswa", df_filtered['Nama_Peserta'].unique())
        if selected_students:
            student_details = df_filtered[df_filtered['Nama_Peserta'].isin(selected_students)]
            st.dataframe(student_details)

            # Visualizations for Selected Students
            st.subheader("📊 Visualisasi Siswa Terpilih")
            for student in selected_students:
                student_data = df_filtered[df_filtered['Nama_Peserta'] == student]

                # Calculate metrics for the selected student
                average_gse = student_data['GSE'].mean()
                average_iq = student_data['Nilai_IQ'].mean()
                average_listening = student_data['Listening'].mean()
                average_reading = student_data['Reading'].mean()
                average_speaking = student_data['Speaking'].mean()
                average_writing = student_data['Writing'].mean()

                # Generate automated explanation
                explanation = f"### Analisis untuk {student}\n"
                explanation += f"1. **Rata-rata GSE**: {average_gse:.2f}\n"
                explanation += f"   - GSE adalah ukuran kemampuan siswa dalam skala 1 hingga 5. "
                explanation += f"Rata-rata GSE {average_gse:.2f} menunjukkan bahwa siswa ini berada pada "
                if average_gse < 3:
                    explanation += "kategorisasi 'Below Level', yang menunjukkan bahwa siswa mungkin memerlukan dukungan tambahan."
                elif 3 <= average_gse < 4:
                    explanation += "kategorisasi 'Level 1' hingga 'Level 2', yang menunjukkan bahwa siswa berada pada tingkat dasar dan perlu perhatian lebih."
                else:
                    explanation += "kategorisasi 'Level 3' hingga 'Above Level', yang menunjukkan bahwa siswa berada pada tingkat yang baik."

                explanation += f"\n2. **Rata-rata Nilai IQ**: {average_iq:.2f}\n"
                explanation += f"   - Nilai IQ rata-rata {average_iq:.2f} menunjukkan kemampuan kognitif siswa. "
                if average_iq < 85:
                    explanation += "Ini menunjukkan bahwa siswa mungkin memerlukan pendekatan pembelajaran yang lebih mendukung."
                elif 85 <= average_iq < 100:
                    explanation += "Ini menunjukkan bahwa siswa berada pada tingkat rata-rata dan dapat mengikuti pembelajaran dengan baik."
                else:
                    explanation += "Ini menunjukkan bahwa siswa memiliki kemampuan di atas rata-rata dan mungkin dapat mengambil tantangan lebih besar."

                # Add language skills analysis
                explanation += f"\n3. **Kemampuan Bahasa**:\n"
                explanation += f"   - Listening: {average_listening:.2f}\n"
                explanation += f"   - Reading: {average_reading:.2f}\n"
                explanation += f"   - Speaking: {average_speaking:.2f}\n"
                explanation += f"   - Writing: {average_writing:.2f}\n"
                
                # Recommendations based on performance
                explanation += "### Rekomendasi:\n"
                if average_gse < 3:
                    explanation += "- Disarankan untuk mengikuti program remedial untuk meningkatkan pemahaman dasar.\n"
                elif average_gse < 4:
                    explanation += "- Siswa disarankan untuk berpartisipasi dalam kelompok belajar atau bimbingan tambahan.\n"
                else:
                    explanation += "- Siswa dapat diberikan tantangan lebih lanjut, seperti proyek lanjutan atau kursus lanjutan.\n"

                # Visualize CEFR and IQ for the selected student
                fig, ax = plt.subplots(1, 2, figsize=(14, 6))

                # CEFR Visualization
                sns.countplot(data=student_data, x='CEFR', ax=ax[0], palette='Set2')
                ax[0].set_title(f"Distribusi CEFR untuk {student}", fontsize=14)
                ax[0].set_xlabel("CEFR", fontsize=12)
                ax[0].set_ylabel("Jumlah", fontsize=12)

                # IQ Visualization
                sns.histplot(student_data['Nilai_IQ'], bins=10, kde=True, color='green', ax=ax[1])
                ax[1].set_title(f"Distribusi IQ untuk {student}", fontsize=14)
                ax[1].set_xlabel("Nilai IQ", fontsize=12)
                ax[1].set_ylabel("Frekuensi", fontsize=12)

                st.pyplot(fig)

                # Display the explanation
                st.markdown(explanation)

        else:
            st.warning("Silakan pilih siswa untuk melihat rincian.")

        # Additional Features
        st.subheader("📊 Fitur Visualisasi Tambahan")

        # Heatmap Korelasi
        st.markdown("🌡️ Heatmap Korelasi")
        corr = df_filtered[['GSE', 'Nilai_IQ', 'Listening', 'Reading', 'Speaking', 'Writing']].corr()
        fig_corr, ax_corr = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax_corr)  # Fixed cmap string and ax param
        ax_corr.set_title("Korelasi antara GSE, IQ, dan Kemampuan Bahasa")
        st.pyplot(fig_corr)

        # Word Cloud
        if 'Komentar' in df_filtered.columns:
            st.markdown("🌬️ Word Cloud Komentar Siswa")
            comments = ' '.join(df_filtered['Komentar'].dropna())
            wordcloud = WordCloud(width=800, height=400).generate(comments)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

        # Radar Chart for Skills
        st.markdown("🛡️ Radar Chart Profil Kemampuan Siswa")
        for student in selected_students:
            student_data = df_filtered[df_filtered['Nama_Peserta'] == student][['Listening', 'Reading', 'Speaking', 'Writing']].mean()
            values = student_data.values
            values = np.concatenate((values, [values[0]]))  # Close the circle
            angles = np.linspace(0, 2 * np.pi, len(student_data), endpoint=False).tolist()
            angles += angles[:1]

            fig_radar, ax_radar = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax_radar.fill(angles, values, color='red', alpha=0.25)
            ax_radar.set_yticklabels([])
            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(student_data.index)
            ax_radar.set_title(f"Profil Kemampuan: {student}")
            st.pyplot(fig_radar)

    else:
        st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")

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
    Jika Anda memiliki pertanyaan atau memerlukan izin, silakan hubungi [kreatif.appmobile@gmail.com].
    """)

    # Closing Remarks
    st.markdown("""
    Terima kasih telah menggunakan aplikasi analisis data siswa ini. 
    Kami berharap aplikasi ini dapat membantu Anda dalam memahami dan 
    meningkatkan performa siswa. 
    """)
