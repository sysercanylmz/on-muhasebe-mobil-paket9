from datetime import date

from app.helpers import money
from app.repositories import vergi_aylik_kdv_ozeti, vergi_gecici_donem_ozeti, vergi_yillik_kar_ozeti
from app.screens.base import RefreshableScreen
from app.tax import income_tax_2026_non_wage, kdv_result_label, month_name
from app.widgets import ACCENT_SOFT, DANGER_SOFT, SUCCESS_SOFT, WARNING_SOFT, card, label, metric_card, scroll_container, title_label


class VergiScreen(RefreshableScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = date.today().year
        self.scroll, self.content = scroll_container()
        self.add_widget(self.scroll)

    def on_pre_enter(self, *_args):
        self.reload()

    def reload(self):
        self.content.clear_widgets()
        self.content.add_widget(title_label("Vergi Tahmini"))
        self.content.add_widget(label(
            "Şahıs şirketi için ön tahmin ekranıdır. Resmî beyan yerine geçmez; mali müşavir kontrolü gerekir.",
            size=12,
            height=42,
            color=(0.40, 0.44, 0.53, 1),
        ))

        annual = vergi_yillik_kar_ozeti(self.year)
        kar = float(annual["kar"] or 0)
        tax = income_tax_2026_non_wage(kar)
        kdv_fark = float(annual["hesaplanan_kdv"] or 0) - float(annual["indirilecek_kdv"] or 0)

        self.content.add_widget(metric_card(
            "Yıllık Tahmini Kâr",
            money(kar),
            f"{self.year} gelir - gider matrahı",
            tone="dark",
        ))

        row = card(orientation="horizontal", padding=0, spacing=8, bg_color=(0, 0, 0, 0))
        row.add_widget(metric_card("Gelir Vergisi", money(tax.tax), tax.bracket_label, tone="orange"))
        row.add_widget(metric_card(kdv_result_label(kdv_fark), money(abs(kdv_fark)), "Yıllık KDV farkı", tone="green" if kdv_fark < 0 else "red" if kdv_fark > 0 else "blue"))
        self.content.add_widget(row)

        self._add_year_detail(annual, tax)
        self._add_kdv_months()
        self._add_quarters()

    def _add_year_detail(self, annual, tax):
        self.content.add_widget(title_label("Yıllık Özet"))
        box = card(padding=12, spacing=4)
        box.add_widget(label(f"Gelir Matrahı: [b]{money(annual['gelir_matrah'])}[/b]", size=13, height=24))
        box.add_widget(label(f"Gider Matrahı: [b]{money(annual['gider_matrah'])}[/b]", size=13, height=24))
        box.add_widget(label(f"Tahmini Vergiye Esas Kâr: [b]{money(tax.taxable_income)}[/b]", size=13, height=24))
        box.add_widget(label(f"Tahmini Gelir Vergisi: [b]{money(tax.tax)}[/b]", size=14, height=28))
        box.add_widget(label(f"Efektif Oran: %{tax.effective_rate:.2f}", size=12, height=22))
        box.add_widget(label("Not: Bağ-Kur, istisna, indirim, geçmiş zarar ve mali müşavir düzeltmeleri hesaba katılmaz.", size=11, height=42, color=(0.40, 0.44, 0.53, 1)))
        self.content.add_widget(box)

    def _add_kdv_months(self):
        self.content.add_widget(title_label("Aylık KDV Özeti"))
        rows = vergi_aylik_kdv_ozeti(self.year)
        if not rows:
            self.content.add_widget(label("Bu yıl için KDV hesaplanan gelir/gider kaydı yok.", size=14, height=32))
            return

        for row in rows:
            hesaplanan = float(row["hesaplanan_kdv"] or 0)
            indirilecek = float(row["indirilecek_kdv"] or 0)
            fark = hesaplanan - indirilecek
            tone_bg = DANGER_SOFT if fark > 0 else SUCCESS_SOFT if fark < 0 else ACCENT_SOFT
            box = card(padding=10, spacing=3, bg_color=tone_bg)
            box.add_widget(label(f"[b]{month_name(row['ay'])} {self.year}[/b]", size=14, height=25))
            box.add_widget(label(f"Hesaplanan KDV: {money(hesaplanan)}", size=12, height=22))
            box.add_widget(label(f"İndirilecek KDV: {money(indirilecek)}", size=12, height=22))
            box.add_widget(label(f"{kdv_result_label(fark)}: [b]{money(abs(fark))}[/b]", size=13, height=24))
            self.content.add_widget(box)

    def _add_quarters(self):
        self.content.add_widget(title_label("Geçici Vergi Dönemleri"))
        rows = vergi_gecici_donem_ozeti(self.year)
        for row in rows:
            kar = float(row["kar"] or 0)
            bg = WARNING_SOFT if kar > 0 else ACCENT_SOFT
            box = card(padding=10, spacing=3, bg_color=bg)
            box.add_widget(label(f"[b]{row['donem_adi']}[/b] • {row['aylar']}", size=14, height=26))
            box.add_widget(label(f"Dönem Geliri: {money(row['gelir_matrah'])}", size=12, height=22))
            box.add_widget(label(f"Dönem Gideri: {money(row['gider_matrah'])}", size=12, height=22))
            box.add_widget(label(f"Dönem Kârı: [b]{money(row['kar'])}[/b]", size=13, height=24))
            box.add_widget(label(f"Kümülatif Kâr: {money(row['kumulatif_kar'])}", size=12, height=22))
            box.add_widget(label(f"Bu Dönem Tahmini Geçici Vergi: [b]{money(row['donem_tahmini_vergi'])}[/b]", size=13, height=28))
            self.content.add_widget(box)
