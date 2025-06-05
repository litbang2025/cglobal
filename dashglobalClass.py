import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

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

# Main content based on selected menu option
if selected == "Dashboard":
    st.title("📊 Dashboard Analisis Siswa")
    st.markdown("Selamat datang di dashboard kami! Di sini Anda dapat melihat analisis data secara interaktif.")

    if st.session_state.df is not None:
        # Ensure 'GSE' is numeric
        st.session_state.df['GSE'] = pd.to_numeric(st.session_state.df['GSE'], errors='coerce')
        
        # Example metrics based on the uploaded data
        total_students = len(st.session_state.df)
        passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Lulus'])
        not_passed_students = len(st.session_state.df[st.session_state.df['Keterangan'] != 'Lulus'])
        waiting_list_students = len(st.session_state.df[st.session_state.df['Keterangan'] == 'Waiting List'])
        above_level_students = len(st.session_state.df[st.session_state.df['GSE'] > 5])  # Example threshold for GSE

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

        st.markdown(f"**Jumlah di atas level GSE 5**: {above_level_students}")

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
        # Ensure 'GSE' is numeric
        st.session_state.df['GSE'] = pd.to_numeric(st.session_state.df['GSE'], errors='coerce')

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

        # Kemampuan Bahasa
        st.markdown("#### 🗣️ Kemampuan Bahasa (Listening, Reading, Speaking, Writing)")
        skill_cols = ['Listening', 'Reading', 'Speaking', 'Writing']
        for col in skill_cols:
            st.markdown(f"##### {col}")
            fig, ax = plt.subplots()
            sns.countplot(data=df_filtered, x=col, palette='pastel', ax=ax)
            ax.set_title(f"Distribusi {col}", fontsize=14)
            ax.set_xlabel(col, fontsize=12)
            ax.set_ylabel("Jumlah", fontsize=12)
            st.pyplot(fig)

            # Explanation for Language Skills
            skill_counts = df_filtered[col].value_counts()
            st.markdown(f"**Jumlah Siswa per {col}**: {skill_counts.to_dict()}")

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

        # Karakteristik Psikologis (T/ST)
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

    else:
        st.warning("Silakan unggah data terlebih dahulu di menu 'Data Upload'.")


elif selected == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("Aplikasi ini bertujuan untuk memberikan analisis data siswa secara interaktif.")
