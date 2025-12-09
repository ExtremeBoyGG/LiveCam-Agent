import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math
import os

lbr_layar_cam,tng_layar_cam=1280,720
kotak_area_main=150
tingkat_kehalusan=7
koor_x_skrg,koor_y_skrg=0,0
koor_x_lalu,koor_y_lalu=0,0

status_tahan_klik=False
kunci_klik_kanan=False

mode_swipe_aktif=False
titik_awal_swipe_x=0
titik_awal_swipe_y=0
batas_jarak_swipe=100

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,lbr_layar_cam)
cap.set(4,tng_layar_cam)

otak_tangan=mp.solutions.hands.Hands(max_num_hands=1,min_detection_confidence=0.7,min_tracking_confidence=0.5)
pensil_lukis=mp.solutions.drawing_utils
resolusi_lebar,resolusi_tinggi=pyautogui.size()

def deteksi_jari_sakti(tanda_tangan,jenis_tangan):
    puncak_jari=[4,8,12,16,20]
    status_jari=[]
    if jenis_tangan=="Right":
        if tanda_tangan.landmark[puncak_jari[0]].x<tanda_tangan.landmark[puncak_jari[0]-1].x:
            status_jari.append(1)
        else:
            status_jari.append(0)
    else:
        if tanda_tangan.landmark[puncak_jari[0]].x>tanda_tangan.landmark[puncak_jari[0]-1].x:
            status_jari.append(1)
        else:
            status_jari.append(0)
    for idx in range(1,5):
        if tanda_tangan.landmark[puncak_jari[idx]].y<tanda_tangan.landmark[puncak_jari[idx]-2].y:
            status_jari.append(1)
        else:
            status_jari.append(0)
    return status_jari

while True:
    berhasil,bingkai=cap.read()
    if not berhasil:
        break
    bingkai=cv2.flip(bingkai,1)
    bingkai_rgb=cv2.cvtColor(bingkai,cv2.COLOR_BGR2RGB)
    hasil_proses=otak_tangan.process(bingkai_rgb)
    cv2.rectangle(bingkai,(kotak_area_main,kotak_area_main),(lbr_layar_cam-kotak_area_main,tng_layar_cam-kotak_area_main),(0,255,255),2)
    if hasil_proses.multi_hand_landmarks:
        data_tangan=hasil_proses.multi_hand_landmarks[0]
        info_tangan=hasil_proses.multi_handedness[0].classification[0].label
        pensil_lukis.draw_landmarks(bingkai,data_tangan,mp.solutions.hands.HAND_CONNECTIONS)
        konfigurasi_jari=deteksi_jari_sakti(data_tangan,info_tangan)
        jumlah_jari_bangun=sum(konfigurasi_jari)
        x_telunjuk=data_tangan.landmark[8].x*lbr_layar_cam
        y_telunjuk=data_tangan.landmark[8].y*tng_layar_cam
        if konfigurasi_jari[1]==1 and konfigurasi_jari[2]==0 and konfigurasi_jari[3]==0 and konfigurasi_jari[4]==0:
            kunci_klik_kanan=False
            mode_swipe_aktif=False
            x_layar=np.interp(x_telunjuk,(kotak_area_main,lbr_layar_cam-kotak_area_main),(0,resolusi_lebar))
            y_layar=np.interp(y_telunjuk,(kotak_area_main,tng_layar_cam-kotak_area_main),(0,resolusi_tinggi))
            koor_x_skrg=koor_x_lalu+(x_layar-koor_x_lalu)/tingkat_kehalusan
            koor_y_skrg=koor_y_lalu+(y_layar-koor_y_lalu)/tingkat_kehalusan
            pyautogui.moveTo(koor_x_skrg,koor_y_skrg)
            cv2.circle(bingkai,(int(x_telunjuk),int(y_telunjuk)),15,(255,0,255),cv2.FILLED)
            koor_x_lalu,koor_y_lalu=koor_x_skrg,koor_y_skrg
            x_jempol=data_tangan.landmark[4].x*lbr_layar_cam
            y_jempol=data_tangan.landmark[4].y*tng_layar_cam
            jarak_asmara=math.hypot(x_jempol-x_telunjuk,y_jempol-y_telunjuk)
            if jarak_asmara<40:
                cv2.circle(bingkai,(int(x_telunjuk),int(y_telunjuk)),15,(0,255,0),cv2.FILLED)
                if not status_tahan_klik:
                    pyautogui.mouseDown()
                    status_tahan_klik=True
            else:
                if status_tahan_klik:
                    pyautogui.mouseUp()
                    status_tahan_klik=False
        elif konfigurasi_jari[1]==1 and konfigurasi_jari[2]==1 and konfigurasi_jari[3]==0:
            mode_swipe_aktif=False
            if status_tahan_klik:
                pyautogui.mouseUp()
                status_tahan_klik=False
            if not kunci_klik_kanan:
                jarak_jari_tengah=math.hypot((data_tangan.landmark[12].x*lbr_layar_cam)-x_telunjuk,(data_tangan.landmark[12].y*tng_layar_cam)-y_telunjuk)
                if jarak_jari_tengah>40:
                    pyautogui.click(button='right')
                    kunci_klik_kanan=True
                    cv2.putText(bingkai,"KLIK KANAN",(int(x_telunjuk),int(y_telunjuk)),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        elif jumlah_jari_bangun==3:
            status_tahan_klik=False
            kunci_klik_kanan=False
            if not mode_swipe_aktif:
                titik_awal_swipe_x=x_telunjuk
                titik_awal_swipe_y=y_telunjuk
                mode_swipe_aktif=True
                cv2.putText(bingkai,"MODE GESTURE: GESER TANGAN",(50,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
            else:
                selisih_x=x_telunjuk-titik_awal_swipe_x
                selisih_y=y_telunjuk-titik_awal_swipe_y
                aksi_terjadi=""
                if selisih_y<-batas_jarak_swipe:
                    os.startfile("notepad.exe")
                    aksi_terjadi="BUKA NOTEPAD"
                    mode_swipe_aktif=False
                elif selisih_y>batas_jarak_swipe:
                    os.startfile("calc.exe")
                    aksi_terjadi="BUKA KALKULATOR"
                    mode_swipe_aktif=False
                elif selisih_x<-batas_jarak_swipe:
                    pyautogui.hotkey('win','e')
                    aksi_terjadi="BUKA EXPLORER"
                    mode_swipe_aktif=False
                elif selisih_x>batas_jarak_swipe:
                    pyautogui.screenshot("screenshot_tangan.png")
                    aksi_terjadi="CEKREK LAYAR"
                    mode_swipe_aktif=False
                if aksi_terjadi!="":
                    cv2.putText(bingkai,aksi_terjadi,(200,200),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
                    time.sleep(0.5)
        elif jumlah_jari_bangun==5:
            status_tahan_klik=False
            kunci_klik_kanan=False
            mode_swipe_aktif=False
            cv2.putText(bingkai,"SCROLLING...",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
            if y_telunjuk<tng_layar_cam/2-50:
                pyautogui.scroll(30)
            elif y_telunjuk>tng_layar_cam/2+50:
                pyautogui.scroll(-30)
        else:
            if status_tahan_klik:
                pyautogui.mouseUp()
                status_tahan_klik=False
            kunci_klik_kanan=False
            mode_swipe_aktif=False
    cv2.imshow("PENGENDALI ELEMEN",bingkai)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()