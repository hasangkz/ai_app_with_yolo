# Resmi Python imajını ana imaj olarak kullanır.
FROM python:3.9-slim

# Docker konteynerindeki çalışma dizini /app olarak ayarlanır. Bu, uygulama kodunun ve diğer dosyaların konteyner içinde nerede bulunacağını belirtir.
WORKDIR /app

# Bağımlılıkların listesini içeren requirements.txt dosyası, konteyner içindeki çalışma dizinine kopyalanır ve ardından bu bağımlılıklar Docker'daki Python ortamına yüklenir.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Geri kalan uygulama kodu ve dosyaları (app.py gibi) konteynerin çalışma dizinine kopyalanır.
COPY . .

# Uygulamanın çalışacağı port numarası belirtilir. Burada 5070 portu açılır.
EXPOSE 5090

# Flask uygulamasının başlangıç dosyasının (app.py) adını belirten bir ortam değişkeni tanımlanır.
ENV FLASK_APP app.py

# Docker konteyneri başlatıldığında, Flask uygulamasını başlatmak için kullanılacak komut belirtilir. Bu komut, Flask uygulamasını belirtilen host ve portta başlatır.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5090"]
