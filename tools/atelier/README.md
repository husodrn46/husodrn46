# Atölye görselleri

`python3 tools/build_atelier.py` açık ve koyu temalı PNG başlıkları yeniden üretir. Python 3 ve Pillow gerekir. Varsayılan font macOS Arial'dir; diğer sistemlerde `--font /path/regular.ttf --bold /path/bold.ttf` kullanılabilir. Font dosyaları dağıtılmaz.

- `lumen-demo.png`: Lumen yerel QA çıktısındaki `siparis-detay-sonra-1440.png`. Örnek Züccaciye, Lumen'in `demo/sql/02_demo_veri.sql` dosyasında bulunan sentetik müşteridir. Gerçek şirket kaydı içermez.
- `windows-stats.png`: https://github.com/husodrn46/windows-stats/blob/main/docs/images/strip.png adresindeki gerçek uygulama görüntüsü. Sayaçlar canlı profil verisi değildir.

PNG kullanımı, GitHub'ın SVG içindeki raster görseller ve harici fontlarla ilgili sınırlamalarından kaçınır. README metni ve bağlantıları gerçek metin olarak kalır.

Tasarım yöntemi: Unslop, Damir Sokolovsky (https://x.com/heydamir), CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), ve Frontend Design yönergeleri. Önceki profil görselleri arşiv olarak korunmuştur; yeni README onları kullanmaz.
