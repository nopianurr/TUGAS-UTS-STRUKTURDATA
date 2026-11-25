import csv
import matplotlib.pyplot as plt


def simpan_csv(hasil, nama_csv="Hasil_Pengujian.csv"):
    with open(nama_csv, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Jumlah Data",
            "Waktu Linked Queue (detik)",
            "Waktu asyncio.Queue (detik)",
            "Memori Linked Queue (KB)",
            "Memori asyncio.Queue (KB)"
        ])

        for baris in hasil:
            writer.writerow([
                baris[0],
                f"{baris[1]:.6f}",
                f"{baris[2]:.6f}",
                f"{baris[3]:.2f}",
                f"{baris[4]:.2f}"
            ])

    print(f"\nFile CSV berhasil dibuat: {nama_csv}")


def tampilkan_grafik_python(
    nama_csv="Hasil_Pengujian.csv",
    nama_gambar="grafik_pengujian.png"
):
    jumlah = []
    waktu_linked = []
    waktu_asyncio = []
    memori_linked = []
    memori_asyncio = []
    isi_tabel = []

    with open(nama_csv, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            jml = int(row["Jumlah Data"])
            w_l = float(row["Waktu Linked Queue (detik)"])
            w_a = float(row["Waktu asyncio.Queue (detik)"])
            m_l = float(row["Memori Linked Queue (KB)"])
            m_a = float(row["Memori asyncio.Queue (KB)"])

            jumlah.append(jml)
            waktu_linked.append(w_l)
            waktu_asyncio.append(w_a)
            memori_linked.append(m_l)
            memori_asyncio.append(m_a)

            isi_tabel.append([
                f"{jml:,}".replace(",", "."),
                f"{w_l:.6f}",
                f"{w_a:.6f}",
                f"{m_l:.2f}",
                f"{m_a:.2f}"
            ])

    if not jumlah:
        raise ValueError("File CSV tidak memiliki data pengujian.")

    fig = plt.figure(figsize=(19, 8), facecolor="white")
    gs = fig.add_gridspec(
        1, 3, width_ratios=[1.5, 1, 1], wspace=0.28
    )

    ax_tabel = fig.add_subplot(gs[0, 0])
    ax_tabel.axis("off")
    ax_tabel.set_title(
        "Tabel Data Hasil Pengujian",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    header = [
        "Jumlah\nData",
        "Waktu Linked\nQueue (detik)",
        "Waktu asyncio\nQueue (detik)",
        "Memori Linked\nQueue (KB)",
        "Memori asyncio\nQueue (KB)"
    ]

    tabel = ax_tabel.table(
        cellText=isi_tabel,
        colLabels=header,
        loc="center",
        cellLoc="center"
    )

    tabel.auto_set_font_size(False)
    tabel.set_fontsize(7)
    tabel.scale(1.0, 1.8)

    for (r, c), cell in tabel.get_celld().items():
        cell.set_edgecolor("#BFBFBF")
        if r == 0:
            cell.set_facecolor("#2F5597")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif r % 2:
            cell.set_facecolor("#F2F5F9")
        else:
            cell.set_facecolor("white")

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.plot(jumlah, waktu_linked, marker="o",
             linewidth=2, label="Linked Queue")
    ax1.plot(jumlah, waktu_asyncio, marker="o",
             linewidth=2, label="asyncio.Queue")
    ax1.set_title("Perbandingan Waktu Eksekusi",
                  fontsize=12, fontweight="bold")
    ax1.set_xlabel("Jumlah Data")
    ax1.set_ylabel("Waktu Eksekusi (detik)")
    ax1.set_xscale("log")
    ax1.set_xticks(jumlah)
    ax1.set_xticklabels(
        [f"{x:,}".replace(",", ".") for x in jumlah],
        rotation=45, ha="right", fontsize=7
    )
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(fontsize=8)

    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(jumlah, memori_linked, marker="o",
             linewidth=2, label="Linked Queue")
    ax2.plot(jumlah, memori_asyncio, marker="o",
             linewidth=2, label="asyncio.Queue")
    ax2.set_title("Perbandingan Penggunaan Memori",
                  fontsize=12, fontweight="bold")
    ax2.set_xlabel("Jumlah Data")
    ax2.set_ylabel("Penggunaan Memori (KB)")
    ax2.set_xscale("log")
    ax2.set_xticks(jumlah)
    ax2.set_xticklabels(
        [f"{x:,}".replace(",", ".") for x in jumlah],
        rotation=45, ha="right", fontsize=7
    )
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(fontsize=8)

    fig.subplots_adjust(
        left=0.03, right=0.98, top=0.88, bottom=0.22
    )

    plt.savefig(nama_gambar, dpi=180, bbox_inches="tight")
    print(f"\nGrafik berhasil disimpan: {nama_gambar}")
    plt.show()
    plt.close(fig)