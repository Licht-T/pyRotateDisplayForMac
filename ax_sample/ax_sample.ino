/* ADXL335 Simple Test*/

static long xs,ys,zs;

void setup() {
  Serial.begin(9600);
}
     
void loop() {
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
  
  Serial.print("X:");
  Serial.print(x);
  Serial.print(",Y:");
  Serial.print(y);
  Serial.print(",Z:");
  Serial.println(z);
  delay(500);
}
