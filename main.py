#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "5g";        // WiFi ağ adı
const char* password = "12345678"; // WiFi şifresi
const int inputPin = D8;               // D8 pinini kullanıyoruz

WiFiClient client;  // WiFiClient nesnesi oluştur

bool messageSent = false; // Sunucuya mesajın gönderilip gönderilmediğini takip eden bayrak
unsigned long sure = 0;
void setup() {
  Serial.begin(115200);
  pinMode(inputPin, INPUT);            // D8 pini giriş olarak ayarlanıyor

  // WiFi'ye bağlan
  WiFi.begin(ssid, password);
  Serial.print("WiFi'ye bağlanılıyor");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi bağlantısı başarılı");
  Serial.print("IP Adresi: ");
  Serial.println(WiFi.localIP());
}

void dongu(){
  int pin_durum = digitalRead(inputPin);
  if (pin_durum ==0){Serial.println("D8 pini LOW okundu, sunucuya mesaj gönderiliyor...");

    if (WiFi.status() == WL_CONNECTED) { // WiFi'ye bağlı mı kontrol et
      HTTPClient http;
      String url = "http://your_url/makine-ekle?id=5&durum=0";
      
      // WiFiClient ve URL ile HTTP bağlantısını başlat
      http.begin(client, url);          

      int httpResponseCode = http.GET(); // GET isteği gönder

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);
        messageSent = true; // Mesaj başarılı bir şekilde gönderildi, bayrağı güncelle
      } else {
        Serial.print("HTTP GET Hatası: ");
        Serial.println(httpResponseCode);
      }

      http.end(); // HTTP bağlantısını kapat
    }
    
    
    }
    if (pin_durum ==1){Serial.println("D8 pini HIGH okundu, sunucuya mesaj gönderiliyor...");

    if (WiFi.status() == WL_CONNECTED) { // WiFi'ye bağlı mı kontrol et
      HTTPClient http;
      String url = "http://your_url/makine-ekle?id=5&durum=1";
      
      // WiFiClient ve URL ile HTTP bağlantısını başlat
      http.begin(client, url);          

      int httpResponseCode = http.GET(); // GET isteği gönder

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);
        messageSent = true; // Mesaj başarılı bir şekilde gönderildi, bayrağı güncelle
      } else {
        Serial.print("HTTP GET Hatası: ");
        Serial.println(httpResponseCode);
      }

      http.end(); // HTTP bağlantısını kapat
    }
    
    
    }
  
  
  }

void loop() {
  if (millis() - sure > 60000) {
    sure = millis();
    dongu();
  }
  int pinState = digitalRead(inputPin); // D8 pininden okunan değer

  if (pinState == 0 && !messageSent) {  // Eğer D8 pini LOW ve mesaj henüz gönderilmediyse
    Serial.println("D8 pini LOW okundu, sunucuya mesaj gönderiliyor...");

    if (WiFi.status() == WL_CONNECTED) { // WiFi'ye bağlı mı kontrol et
      HTTPClient http;
      String url = "http://your_url/makine-ekle?id=5&durum=0";
      
      // WiFiClient ve URL ile HTTP bağlantısını başlat
      http.begin(client, url);          

      int httpResponseCode = http.GET(); // GET isteği gönder

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);
        messageSent = true; // Mesaj başarılı bir şekilde gönderildi, bayrağı güncelle
        sure = millis();
      } else {
        Serial.print("HTTP GET Hatası: ");
        Serial.println(httpResponseCode);
      }

      http.end(); // HTTP bağlantısını kapat
    } else {
      Serial.println("WiFi bağlantısı yok.");
    }

  } else if (pinState == 1 && messageSent) {
    // Eğer pin HIGH olursa, bayrağı sıfırla
    Serial.println("D8 pini HIGH okundu, yeniden mesaj gönderilebilir.");
    if (WiFi.status() == WL_CONNECTED) { // WiFi'ye bağlı mı kontrol et
      HTTPClient http;
      String url1 = "http://your_url/makine-ekle?id=5&durum=1";
      
      // WiFiClient ve URL ile HTTP bağlantısını başlat
      http.begin(client, url1);          

      int httpResponseCode = http.GET(); // GET isteği gönder

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);
        messageSent = true; // Mesaj başarılı bir şekilde gönderildi, bayrağı güncelle
      } else {
        Serial.print("HTTP GET Hatası: ");
        Serial.println(httpResponseCode);
      }

      http.end(); // HTTP bağlantısını kapat
    }
    messageSent = false;  // Pin HIGH olduğunda tekrar gönderime izin ver
  }

  delay(100); // Döngü gecikmesi
}
