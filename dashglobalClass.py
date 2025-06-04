import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from wordcloud import WordCloud
import numpy as np

# Set page configuration
st.set_page_config(page_title="Analisis Lengkap Data Siswa", layout="wide")

# Custom CSS to enhance the appearance
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f5;  /* Set background color */
    }
    .sidebar .sidebar-content {
        background: #ffffff;  /* Set sidebar background color */
    }
    .stButton>button {
        background-color: #4CAF50;  /* Button color */
        color: white;  /* Button text color */
        border: none;  /* Remove border */
        padding: 10px 20px;  /* Button padding */
        text-align: center;  /* Center text */
        text-decoration: none;  /* Remove underline */
        display: inline-block;  /* Display as inline block */
        font-size: 16px;  /* Font size */
        margin: 4px 2px;  /* Margin */
        cursor: pointer;  /* Pointer cursor on hover */
        border-radius: 5px;  /* Rounded corners */
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;  /* Input border color */
        border-radius: 5px;  /* Input rounded corners */
    }
    .stDataFrame {
        border: 1px solid #4CAF50;  /* DataFrame border color */
        border-radius: 5px;  /* DataFrame rounded corners */
    }
    .title {
        font-size: 2.5rem;  /* Title font size */
        font-weight: bold;  /* Title font weight */
        color: #333;  /* Title color */
    }
    </style>
    """,
    unsafe_allow_html=True  # Allow HTML in markdown
)

# Sidebar menu using streamlit-option-menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  # Title of the menu
        options=["Dashboard", "Data Upload", "Visualisasi", "Tentang"],  # Menu options
        icons=["house", "upload", "bar-chart", "info-circle"],  # Icons for each option
        menu_icon="cast",  # Icon for the menu
        default_index=0,  # Default selected option
        styles={
            "container": {"padding": "5!important", "background-color": "#ffffff"},  # Sidebar container styles
            "icon": {"color": "black", "font-size": "20px"},  # Icon styles
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "color": "black"},  # Nav link styles
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},  # Selected nav link styles
        }
    )

# Initialize a variable to store the DataFrame globally
if 'df' not in st.session_state:
    st.session_state.df = None  # Initialize session state for DataFrame

# Function to convert GSE ranges to numeric values
def convert_gse_to_numeric(gse_value):
    """Convert GSE string values to numeric values."""
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
    st.title("📊 Dashboard Analisis Siswa")  # Title for the dashboard
    st.markdown("Selamat datang di dashboard kami! Di sini Anda dapat melihat analisis data secara interaktif.")

    if st.session_state.df is not None:
        # Convert 'GSE' values to numeric
        st.session_state.df['GSE'] = st.session_state.df['GSE'].apply(convert_gse_to_numeric)

        # Ensure other numeric columns are converted
        st.session_state.df['Nilai_IQ'] = pd.to_numeric(st.session_state.df['Nilai_IQ'], errors='coerce')
        st.session_state.df['Listening'] = pd.to_numeric(st.session_state.df['Listening'], errors='coerce')
        st.session_state.df['Reading'] = pd.to_numeric(st.session_state.df['Reading'], errors='coerce')
        st.session_state.df['Speaking'] = pd.to_numeric(st.session_state.df['Speaking'], errors='coerce')
        st.session_state.df['Writing'] = pd.to_numeric(st.session_state.df['Writing'], errors='coerce')

        # Example metrics based on the uploaded data
        total_students = len(st.session_state.df)  # Total number of students
        passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Lulus'])  # Passed students
        not_passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] != 'Lulus'])  # Not passed
        waiting_list_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Waiting List'])  # Waiting list
        above_level_students = len(st.session_state.df[st.session_state.df['GSE'] > 3])  # Students above GSE level 3

        # Dashboard summary
        col1, col2, col3, col4 = st.columns(4)  # Create columns for metrics
        with col1:
            st.metric("Total Siswa", total_students)  # Display total students
        with col2:
            st.metric("Lulus", passed_students)  # Display passed students
        with col3:
            st.metric("Tidak Lulus", not_passed_students)  # Display not passed students
        with col4:
            st.metric("Waiting List", waiting_list_students)  # Display waiting list students

        st.markdown(f"**Jumlah di atas level GSE 3**: {above_level_students}")  # Display students above GSE level 3

        # Display counts for each category
        st.subheader("📊 Rincian Kategori")  # Subheader for category details
        unit_counts = st.session_state.df['Unit'].value_counts()  # Count of units
        kategori_counts = st.session_state.df['Kategori'].value_counts()  # Count of categories
        
        st.markdown("### Rincian Unit")  # Subheader for unit details
        for unit, count in unit_counts.items():
            st.markdown(f"- **{unit}**: {count} siswa")  # Display unit counts

        st.markdown("### Rincian Kategori")  # Subheader for category details
        for kategori, count in kategori_counts.items():
            st.markdown(f"- **{kategori}**: {count} siswa")  # Display category counts

        # Recommendations for intervention
        with st.expander("Rekomendasi Aksi / Intervensi"):  # Expandable section for recommendations
            remedial_students = st.session_state.df[(st.session_state.df['GSE'] < 3) & (st.session_state.df['Unit'] == 'A')]  # Filter for remedial students
            count_remedial = len(remedial_students)  # Count of remedial students
            if count_remedial > 0:
                st.markdown(f"**{count_remedial} siswa dari Unit A dengan GSE < 3 disarankan untuk mengikuti program remedial.**")  # Display recommendation
            else:
                st.markdown("Tidak ada siswa dari Unit A yang disarankan untuk program remedial.")  # No recommendations

    else:
        st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")  # Prompt to upload data

elif selected == "Data Upload":
    st.title("📤 Unggah Data")  # Title for data upload section
    uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])  # File uploader for Excel files
    if uploaded_file:
        try:
            # Read the uploaded Excel file
            st.session_state.df = pd.read_excel(uploaded_file)  # Load data into session state
            st.success("File berhasil dimuat!")  # Success message
            st.dataframe(st.session_state.df)  # Display the uploaded DataFrame
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca data: {e}")  # Error handling for file reading

elif selected == "Visualisasi":
    st.title("📈 Visualisasi Data")  # Title for visualization section
    st.markdown("Di sini Anda dapat melihat visualisasi data.")  # Description of the section
    
    if st.session_state.df is not None:
        # Convert 'GSE' values to numeric
        st.session_state.df['GSE'] = st.session_state.df['GSE'].apply(convert_gse_to_numeric)

        # Ensure other numeric columns are converted
        st.session_state.df['Nilai_IQ'] = pd.to_numeric(st.session_state.df['Nilai_IQ'], errors='coerce')
        st.session_state.df['Listening'] = pd.to_numeric(st.session_state.df['Listening'], errors='coerce')
        st.session_state.df['Reading'] = pd.to_numeric(st.session_state.df['Reading'], errors='coerce')
        st.session_state.df['Speaking'] = pd.to_numeric(st.session_state.df['Speaking'], errors='coerce')
        st.session_state.df['Writing'] = pd.to_numeric(st.session_state.df['Writing'], errors='coerce')

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

        st.subheader("📄 Data Tersaring")  # Subheader for filtered data
        st.dataframe(df_filtered.style.set_table_attributes('style="width: 100%; border-collapse: collapse;"'), use_container_width=True)  # Display filtered DataFrame

        # Visualisasi CEFR & GSE
        col1, col2 = st.columns(2)  # Create columns for visualizations
        with col1:
            st.markdown("#### 📘 Distribusi CEFR")  # Title for CEFR distribution
            fig1, ax1 = plt.subplots()  # Create a subplot
            sns.countplot(data=df_filtered, x='CEFR', order=df_filtered['CEFR'].value_counts().index, palette='Set2', ax=ax1)  # Count plot for CEFR
            ax1.set_title("Distribusi CEFR", fontsize=14)  # Title for the plot
            ax1.set_xlabel("CEFR", fontsize=12)  # X-axis label
            ax1.set_ylabel("Jumlah", fontsize=12)  # Y-axis label
            st.pyplot(fig1)  # Display the plot

            # Explanation for CEFR Distribution
            cefr_counts = df_filtered['CEFR'].value_counts()  # Count of CEFR levels
            st.markdown(f"**Jumlah Siswa per CEFR**: {cefr_counts.to_dict()}")  # Display counts

        with col2:
            st.markdown("#### 📗 Distribusi GSE")  # Title for GSE distribution
            fig2, ax2 = plt.subplots()  # Create a subplot
            sns.histplot(df_filtered['GSE'], bins=10, kde=True, color='green', ax=ax2)  # Histogram for GSE
            ax2.set_title("Distribusi GSE", fontsize=14)  # Title for the plot
            ax2.set_xlabel("GSE", fontsize=12)  # X-axis label
            ax2.set_ylabel("Frekuensi", fontsize=12)  # Y-axis label
            st.pyplot(fig2)  # Display the plot

            # Explanation for GSE Distribution
            st.markdown(f"**Rata-rata GSE**: {df_filtered['GSE'].mean():.2f}, **Nilai GSE Tertinggi**: {df_filtered['GSE'].max()}, **Nilai GSE Terendah**: {df_filtered['GSE'].min()}")  # Display GSE statistics

        # Kemampuan Bahasa
        st.markdown("#### 🗣️ Kemampuan Bahasa (Listening, Reading, Speaking, Writing)")  # Title for language skills
        skill_cols = ['Listening', 'Reading', 'Speaking', 'Writing']  # List of skill columns
        for col in skill_cols:
            st.markdown(f"##### {col}")  # Subheader for each skill
            fig, ax = plt.subplots()  # Create a subplot
            sns.countplot(data=df_filtered, x=col, palette='pastel', ax=ax)  # Count plot for each skill
            ax.set_title(f"Distribusi {col}", fontsize=14)  # Title for the plot
            ax.set_xlabel(col, fontsize=12)  # X-axis label
            ax.set_ylabel("Jumlah", fontsize=12)  # Y-axis label
            st.pyplot(fig)  # Display the plot

            # Explanation for Language Skills
            skill_counts = df_filtered[col].value_counts()  # Count of language skills
            st.markdown(f"**Jumlah Siswa per {col}**: {skill_counts.to_dict()}")  # Display counts

        # IQ & Kategori IQ
        st.markdown("#### 🧠 Distribusi IQ")  # Title for IQ distribution
        col3, col4 = st.columns(2)  # Create columns for visualizations
        with col3:
            fig3, ax3 = plt.subplots()  # Create a subplot
            sns.histplot(df_filtered['Nilai_IQ'], bins=10, kde=True, color='purple', ax=ax3)  # Histogram for IQ
            ax3.set_title("Distribusi IQ", fontsize=14)  # Title for the plot
            ax3.set_xlabel("Nilai IQ", fontsize=12)  # X-axis label
            ax3.set_ylabel("Frekuensi", fontsize=12)  # Y-axis label
            st.pyplot(fig3)  # Display the plot

            # Explanation for IQ Distribution
            st.markdown(f"**Rata-rata IQ**: {df_filtered['Nilai_IQ'].mean():.2f}, **IQ Tertinggi**: {df_filtered['Nilai_IQ'].max()}, **IQ Terendah**: {df_filtered['Nilai_IQ'].min()}")  # Display IQ statistics

        with col4:
            fig4, ax4 = plt.subplots()  # Create a subplot
            sns.countplot(data=df_filtered, x='Kategori', order=df_filtered['Kategori'].value_counts().index, palette='coolwarm', ax=ax4)  # Count plot for IQ categories
            ax4.set_title("Distribusi Kategori IQ", fontsize=14)  # Title for the plot
            ax4.set_xlabel("Kategori", fontsize=12)  # X-axis label
            ax4.set_ylabel("Jumlah", fontsize=12)  # Y-axis label
            st.pyplot(fig4)  # Display the plot

            # Explanation for IQ Categories
            kategori_counts = df_filtered['Kategori'].value_counts()  # Count of IQ categories
            st.markdown(f"**Jumlah Siswa per Kategori IQ**: {kategori_counts.to_dict()}")  # Display counts

        # Kemampuan Psikologis (T/ST)
        st.markdown("#### 🧩 Analisis Karakteristik Psikologis")  # Title for psychological characteristics
        char_cols = [col for col in st.session_state.df.columns if st.session_state.df[col].isin(['T', 'ST']).any()]  # Identify psychological characteristic columns
        if char_cols:
            psych_summary = df_filtered[char_cols].apply(lambda x: x.value_counts()).fillna(0).astype(int).T  # Summary of psychological characteristics
            psych_summary.columns = ['ST', 'T']  # Rename columns for clarity
            st.dataframe(psych_summary.style.set_table_attributes('style="width: 100%; border-collapse: collapse;"'))  # Display summary DataFrame

            fig5, ax5 = plt.subplots(figsize=(10, 6))  # Create a subplot
            psych_summary.plot(kind='barh', stacked=True, color=['#ffa07a', '#20b2aa'], ax=ax5)  # Stacked bar chart for psychological characteristics
            ax5.set_title("Distribusi T vs ST", fontsize=14)  # Title for the plot
            ax5.set_xlabel("Jumlah", fontsize=12)  # X-axis label
            ax5.set_ylabel("Karakteristik", fontsize=12)  # Y-axis label
            st.pyplot(fig5)  # Display the plot

            # Explanation for Psychological Characteristics
            st.markdown(f"**Jumlah Karakteristik Psikologis**: {psych_summary.to_dict(orient='records')}")  # Display characteristics summary

        # Detailed Student View
        st.subheader("🔍 Rincian Siswa")  # Subheader for detailed student view
        selected_students = st.multiselect("Pilih Siswa", df_filtered['Nama_Peserta'].unique())  # Multi-select for student names
        if selected_students:
            student_details = df_filtered[df_filtered['Nama_Peserta'].isin(selected_students)]  # Filter for selected students
            st.dataframe(student_details)  # Display selected student details

            # Visualizations for Selected Students
            st.subheader("📊 Visualisasi Siswa Terpilih")  # Subheader for selected students' visualizations
            for student in selected_students:
                student_data = df_filtered[df_filtered['Nama_Peserta'] == student]  # Filter data for the selected student

                # Calculate metrics for the selected student
                average_gse = student_data['GSE'].mean()  # Average GSE
                average_iq = student_data['Nilai_IQ'].mean()  # Average IQ
                average_listening = student_data['Listening'].mean()  # Average Listening score
                average_reading = student_data['Reading'].mean()  # Average Reading score
                average_speaking = student_data['Speaking'].mean()  # Average Speaking score
                average_writing = student_data['Writing'].mean()  # Average Writing score

                # Generate automated explanation
                explanation = f"### Analisis untuk {student}\n"  # Title for analysis
                explanation += f"1. **Rata-rata GSE**: {average_gse:.2f}\n"  # Display average GSE
                explanation += f"   - GSE adalah ukuran kemampuan siswa dalam skala 1 hingga 5. "
                explanation += f"Rata-rata GSE {average_gse:.2f} menunjukkan bahwa siswa ini berada pada "
                if average_gse < 3:
                    explanation += "kategorisasi 'Below Level', yang menunjukkan bahwa siswa mungkin memerlukan dukungan tambahan."
                elif 3 <= average_gse < 4:
                    explanation += "kategorisasi 'Level 1' hingga 'Level 2', yang menunjukkan bahwa siswa berada pada tingkat dasar dan perlu perhatian lebih."
                else:
                    explanation += "kategorisasi 'Level 3' hingga 'Above Level', yang menunjukkan bahwa siswa berada pada tingkat yang baik."

                explanation += f"\n2. **Rata-rata Nilai IQ**: {average_iq:.2f}\n"  # Display average IQ
                explanation += f"   - Nilai IQ rata-rata {average_iq:.2f} menunjukkan kemampuan kognitif siswa. "
                if average_iq < 85:
                    explanation += "Ini menunjukkan bahwa siswa mungkin memerlukan pendekatan pembelajaran yang lebih mendukung."
                elif 85 <= average_iq < 100:
                    explanation += "Ini menunjukkan bahwa siswa berada pada tingkat rata-rata dan dapat mengikuti pembelajaran dengan baik."
                else:
                    explanation += "Ini menunjukkan bahwa siswa memiliki kemampuan di atas rata-rata dan mungkin dapat mengambil tantangan lebih besar."

                # Add language skills analysis
                explanation += f"\n3. **Kemampuan Bahasa**:\n"  # Title for language skills analysis
                explanation += f"   - Listening: {average_listening:.2f}\n"  # Listening average
                explanation += f"   - Reading: {average_reading:.2f}\n"  # Reading average
                explanation += f"   - Speaking: {average_speaking:.2f}\n"  # Speaking average
                explanation += f"   - Writing: {average_writing:.2f}\n"  # Writing average
                
                # Recommendations based on performance
                explanation += "### Rekomendasi:\n"  # Title for recommendations
                if average_gse < 3:
                    explanation += "- Disarankan untuk mengikuti program remedial untuk meningkatkan pemahaman dasar.\n"  # Remedial recommendation
                elif average_gse < 4:
                    explanation += "- Siswa disarankan untuk berpartisipasi dalam kelompok belajar atau bimbingan tambahan.\n"  # Group study recommendation
                else:
                    explanation += "- Siswa dapat diberikan tantangan lebih lanjut, seperti proyek lanjutan atau kursus lanjutan.\n"  # Advanced challenges

                # Visualize CEFR and IQ for the selected student
                fig, ax = plt.subplots(1, 2, figsize=(14, 6))  # Create subplots for CEFR and IQ

                # CEFR Visualization
                sns.countplot(data=student_data, x='CEFR', ax=ax[0], palette='Set2')  # Count plot for CEFR
                ax[0].set_title(f"Distribusi CEFR untuk {student}", fontsize=14)  # Title for CEFR plot
                ax[0].set_xlabel("CEFR", fontsize=12)  # X-axis label
                ax[0].set_ylabel("Jumlah", fontsize=12)  # Y-axis label

                # IQ Visualization
                sns.histplot(student_data['Nilai_IQ'], bins=10, kde=True, color='green', ax=ax[1])  # Histogram for IQ
                ax[1].set_title(f"Distribusi IQ untuk {student}", fontsize=14)  # Title for IQ plot
                ax[1].set_xlabel("Nilai IQ", fontsize=12)  # X-axis label
                ax[1].set_ylabel("Frekuensi", fontsize=12)  # Y-axis label

                st.pyplot(fig)  # Display the plots

                # Display the explanation
                st.markdown(explanation)  # Show the generated explanation

        else:
            st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")  # Warning if no students are selected

else:
    st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")  # Warning if no data is uploaded

# Tentang Section
elif selected == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")  # Title for the About section
    
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

