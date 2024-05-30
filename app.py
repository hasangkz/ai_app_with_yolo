from flask import Flask, request, jsonify
from ultralytics import YOLO
import imutils
import cv2
import numpy as np

app = Flask(__name__)

model_path = "model.pt"
model = YOLO(model_path)
# Önceden eğittiğimiz yolo modelimizi "model.pt" dosyasından yüklüyoruz.

threshold = 0.1
# threshold değişkeni, nesne tespiti sırasında kabul edilebilir bir güven skoru eşiği belirlemek için kullanılıyor.

@app.route('/detect', methods=['POST'])
def detect_objects():
# "/detect" endpointi, gönderilen bir görüntü dosyasını alır, nesne tespiti yapar ve sonuçları JSON formatında geri döndürür.

    if 'file' not in request.files:
        return jsonify({"error": "No file part","status":bool(0)}),400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": 'No selected file',"status":bool(0)})

# Modelin tahmin edebileceği sınıf etiketlerini içerir. Türk Lirası banknotularını, değerlerine dönüştüren handleResult fonksiyonumuz.
    def handleResult(value):
        if value == 0:
            return "20"
        elif value == 1:
            return "5"
        elif value == 2:
            return "50"
        elif value == 4:
            return "100"
        elif value == 6:
            return "10"
        elif value == 7:
            return "200"
        else:
            return value 

    try:
        if file:
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            # cv2 dosyayı okur ve bu dosyayı bir görüntüye dönüştürür.
            img = imutils.resize(img, width=640)
            # görüntüyü belirli bir genişlikte yeniden boyutlandırır. Bu, modelimizin daha hızlı çalışması için yapılır.
            results = model(img)[0]
            # modeli kullanarak nesne tespiti yaparız ve sonuçları resultsa aktarırız.
            result = None

            # Bir döngü kullanarak, her bir tespit edilen nesne için aşağıdaki işlemler yapılır
            for result in results.boxes.data.tolist():
                # Nesnenin koordinatları alınır ve (x1, y1, x2, y2)'e aktarılır.
                # Nesnenin sınıf ID'si (class_id) ve güven skoru (score) alınır.
                x1, y1, x2, y2, score, class_id = result
                result = class_id

                # Eğer güven skoru, belirlenen eşikten büyükse (score > threshold), nesne için bir dikdörtgen çizilir. Bu, tespit edilen nesnenin belirlenen eşikten daha yüksek bir güvene sahip olduğu durumda görüntüye bir kutu çizilmesini sağlar.

                if score > threshold:
                    cv2.rectangle(img, (int(x1-120), int(y1)), (int(x2)+145, int(y2)), (0, 255, 0), 4)

                # img: Dikdörtgenin çizileceği görüntü.
                # (int(x1-120), int(y1)): Dikdörtgenin sol üst köşesinin koordinatları. x1-120 sol üst köşenin x koordinatını 120 piksel sola kaydırır.
                # (int(x2)+145, int(y2)): Dikdörtgenin sağ alt köşesinin koordinatları. x2+145 sağ alt köşenin x koordinatını 145 piksel sağa kaydırır.
                # (0, 255, 0): Dikdörtgenin rengi. Burada (B, G, R) formatında bir tuple kullanılır. Bu tupledaki her bir değer 0 ile 255 arasında olmalıdır. Burada (0, 255, 0) yeşil rengi temsil eder.
                # 4: Dikdörtgenin kalınlığı piksel cinsinden belirlenir. Bu durumda, dikdörtgenin çizgi kalınlığı 4 pikseldir.
                # Bu kod satırı, tespit edilen nesnelerin etrafına yeşil renkte dikdörtgenler çizer. x1, y1, x2, y2 koordinatları, nesnenin sol üst ve sağ alt köşelerinin piksel cinsinden konumlarını temsil eder. Bu koordinatlar, dikdörtgenin tam olarak nesneyi sarması için kullanılır. x1-120 ve x2+145 ifadeleri, dikdörtgenin nesne etrafında biraz daha fazla boşluk bırakacak şekilde çizilmesini sağlar.

          
            return jsonify({"result": handleResult(int(result)),"status":bool(1)}),200

    except Exception as e:
        return jsonify({"error": str(e),"status":bool(0)}), 400
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5090)
