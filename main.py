import asyncio

from benchmark import pengujian
from report import simpan_csv, tampilkan_grafik_python


if __name__ == "__main__":
    try:
        hasil = asyncio.run(pengujian())
        simpan_csv(hasil)
        tampilkan_grafik_python()

        print("\n" + "=" * 45)
        print("SELURUH PENGUJIAN SELESAI!")
        print("=" * 45)

    except Exception as e:
        print("\nTERJADI KESALAHAN:")
        print(e)
