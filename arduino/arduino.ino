const byte inputPin = 2;
const byte powerPin = 3;
long start;

boolean on = false;
long finish;

void count_ISR(){
  long c = millis();
  Serial.print("COUNT ");
  Serial.print(c);
  Serial.println("");
}

void start_collection(int collection_length){
  on = true;
  digitalWrite(powerPin, HIGH);
  Serial.println("DURATION "+collection_length);
  delay(500);
  start = millis();
  finish = start + (1000 * collection_length);
  Serial.print("START ");
  Serial.print(start);
  Serial.println("");  
}
void finish_collection(){
  Serial.print("END ");
  Serial.print(finish);
  Serial.println("");
  on = false;
}
void setup() {
  Serial.begin(9600);

  pinMode(inputPin, INPUT);
  interrupts();
  attachInterrupt(digitalPinToInterrupt(inputPin), count_ISR, FALLING);

}

void loop() {
  if (on && millis() >= finish){
    finish_collection();
  }
  if (Serial.available()){
    String in = Serial.readString();

    if (in.indexOf("COLLECT")>=0){
      String num = in.substring(8);
      num.trim();
      int collection_length;
      if (num.length() == 0){
        // collect indefinitely
        collection_length = 0;
      }
      else{ 
        collection_length = num.toInt();
      }
      start_collection(collection_length);
    }

  }
  
  digitalWrite(powerPin, on ? HIGH : LOW);
}
