const byte inputPin = 2;
const byte powerPin = 3;
unsigned long start;

boolean on = false;
unsigned long finish;  

void count_ISR(){
  unsigned long c = millis();

  if (c >= finish && finish != 0){
    finish_collection();
  }
  Serial.print("COUNT ");
  Serial.print(c);
  Serial.println("");
}

void start_collection(long collection_length){
  on = true;
  digitalWrite(powerPin, HIGH);
  delay(1000);
  Serial.print("DURATION ");
  Serial.print(collection_length);
  Serial.println("");

  start = millis();
  finish = (start + (1000 * collection_length));
  Serial.print("WILLFINISH ");
  Serial.print(finish);
  Serial.println("");
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
  digitalWrite(powerPin, on ? HIGH : LOW);
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
        collection_length = (unsigned long)num.toInt();
      }
      start_collection(collection_length);
    }

  }
  

}
