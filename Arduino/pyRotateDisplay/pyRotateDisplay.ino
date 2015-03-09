static const String hs_str = "foobar";


static boolean hs;

void setup()
{
  hs=false;
  Serial.begin(9600);
}

void loop()
{
  if(hs){
    if (Serial.available() > 0) {
      int incomingByte = Serial.read();
      if(incomingByte==50){
        hs=false;
      }
    }
      int i;
  long x,y,z;
  x=y=z=0;
        
  for(i=1; i<=100; i++){
    x+=analogRead(0);
    y+=analogRead(1);
    z+=analogRead(2);
  }
  x/=100;
  y/=100;
  z/=100;
  
  Serial.print("{");
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.print(z);
  Serial.println("}");
    delay(1000);
  }
  else{
    if (Serial.available() > 0) {
    // read the incoming byte:
      int incomingByte = Serial.read();
      if(incomingByte==48){
        Serial.println(hs_str);
        delay(1000);
      }
      else if(incomingByte==49){
        Serial.println("ok");
        hs=true;
        delay(1000);
      }
    }
  }
}

