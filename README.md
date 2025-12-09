# Hand Control System

Sistem antarmuka berbasis computer vision yang mengubah gestur tangan menjadi perintah sistem operasi secara real-time. Proyek ini memanfaatkan OpenCV dan MediaPipe untuk menciptakan mouse virtual dan pengenalan gestur presisi tinggi, memungkinkan pengguna mengontrol komputer tanpa perangkat periferal fisik.

Teknologi:![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-red)

## Ringkasan

Perangkat lunak ini memetakan landmark tangan ke koordinat layar menggunakan logika "Safe Zone" terinterpolasi. Pendekatan ini memastikan ergonomi penggunaan, memungkinkan kursor menjangkau seluruh sudut layar monitor tanpa perlu merentangkan tangan secara berlebihan di depan kamera. Sistem ini memisahkan navigasi (pergerakan kursor) dari eksekusi perintah (membuka aplikasi) untuk mencegah kesalahan input.

## Fitur Utama

* **Mouse Virtual Presisi:** Kontrol kursor yang halus dengan algoritma smoothing untuk mengurangi getaran.
* **Interaksi Tanpa Sentuh:** Klik kiri, klik kanan, klik ganda, dan drag-and-drop menggunakan gestur jari natural.
* **Pintasan Gestur:** Membuka aplikasi (Notepad, Keyboard Virtual, Explorer) menggunakan sapuan tangan (swipe) terarah.
* **Safe Zone Ergonomis:** Area aktif yang dapat disesuaikan untuk meminimalkan pergerakan fisik tangan.
* **Dukungan Dua Tangan:** Logika adaptif yang otomatis menyesuaikan deteksi untuk pengguna tangan kiri atau kanan.
* **Simulasi Web:** Menyertakan versi HTML/JS untuk demonstrasi berbasis browser.

## Instalasi

### Prasyarat

Pastikan Python telah terinstal di sistem Anda. Proyek ini bergantung pada pustaka berikut:

* opencv-python
* mediapipe
* pyautogui
* numpy

### Langkah Pemasangan

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/ExtremeBoyGG/LiveCam-Agent
    cd LiveCam-Agent
    ```

2.  **Instal Dependensi**
    Jalankan perintah berikut di terminal:
    ```bash
    pip install opencv-python mediapipe pyautogui numpy
    ```

3.  **Jalankan Aplikasi**
    ```bash
    python main.py
    ```

## Panduan Penggunaan

Sistem mendeteksi jumlah jari aktif dan pose tangan spesifik untuk memicu aksi. Pastikan tangan terlihat jelas di depan kamera.

### Navigasi & Klik

| Gestur | Aksi | Deskripsi |
| :--- | :--- | :--- |
| **1 Jari (Telunjuk)** | **Gerak Kursor** | Menggerakkan pointer mouse. Gunakan area tengah kamera untuk menjangkau seluruh layar. |
| **Cubit (Jempol + Telunjuk)** | **Klik Kiri / Drag** | Cubit cepat untuk klik. Cubit dan tahan sambil bergerak untuk drag file atau jendela. |
| **2 Jari (Membentuk V)** | **Klik Kanan** | Memicu menu konteks klik kanan sekali. |
| **4 Jari** | **None** | None |
| **5 Jari (Telapak Terbuka)** | **Mode Scroll** | Gerakkan tangan ke atas atau bawah untuk menggulir halaman web/dokumen. |

### Pintasan Aplikasi (Mode 3 Jari)

Aktifkan mode ini dengan mengangkat **3 jari**. Kursor akan berhenti sementara menunggu arah sapuan tangan (swipe).

| Arah Swipe | Aksi | Perintah Sistem |
| :--- | :--- | :--- |
| **Geser ke ATAS** | **Buka Notepad** | Menjalankan `notepad.exe` |
| **Geser ke BAWAH** | **Membuka Kalkulator** | Menjalankan `calc.exe` |
| **Geser ke KIRI** | **File Explorer** | Menjalankan pintasan `Win + E` |
| **Geser ke KANAN** | **Screenshot** | Mengambil tangkapan layar dan menyimpannya secara lokal |

## Bantu Kami Menyempurnakan

Kritik dan saran kami terima di link google form berikut ![Form](https://docs.google.com/forms/d/e/1FAIpQLSfxCYz_74nT5xzEwZIKl5b9MtB-HnaELzpU8oYeds_fc1wvtQ/viewform?usp=publish-editor)
Made with ❤️ By Group 7
