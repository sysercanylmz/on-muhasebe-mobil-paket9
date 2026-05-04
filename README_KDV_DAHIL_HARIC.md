# Paket 8 - KDV Dahil / KDV Hariç Giriş

Bu sürümde işlem formlarına KDV hesaplama desteği eklendi.

## Eklenenler

- Tutar giriş şekli: KDV Dahil / KDV Hariç
- KDV oranı artık elle yazılabilir. Örnek: 0, 1, 8, 10, 18, 20
- KDV önizleme alanı eklendi.
- Gider ve gelir kayıtlarında matrah, KDV ve genel toplam ayrı hesaplanır.
- Tahsilat ve ödeme kayıtlarında KDV otomatik 0 kabul edilir.
- İşlem detayında matrah, KDV tutarı, genel toplam ve KDV giriş şekli görünür.
- Raporlar ekranına KDV Özeti eklendi.

## Hesaplama mantığı

KDV Dahil seçilirse girilen tutar genel toplam kabul edilir.

Örnek:
- Tutar: 1200
- KDV: %20
- Matrah: 1000
- KDV: 200
- Genel Toplam: 1200

KDV Hariç seçilirse girilen tutar matrah kabul edilir.

Örnek:
- Tutar: 1000
- KDV: %20
- Matrah: 1000
- KDV: 200
- Genel Toplam: 1200

## Güncellenen ana dosyalar

- app/helpers.py
- app/database.py
- app/repositories.py
- app/screens/islemler_screen.py
- app/screens/raporlar_screen.py
