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

