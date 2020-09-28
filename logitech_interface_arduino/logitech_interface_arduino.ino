#define HS_XAXIS_12        400
#define HS_XAXIS_56        500
#define HS_YAXIS_135       800
#define HS_YAXIS_246       300

int b[16];
// Digital inputs definitions
#define DI_REVERSE         1
#define DI_MODE            3
#define DI_RED_CENTERRIGHT 4
#define DI_RED_CENTERLEFT  5
#define DI_RED_RIGHT       6
#define DI_RED_LEFT        7
#define DI_BLACK_TOP       8
#define DI_BLACK_RIGHT     9
#define DI_BLACK_LEFT      10
#define DI_BLACK_BOTTOM    11
#define DI_DPAD_RIGHT      12
#define DI_DPAD_LEFT       13
#define DI_DPAD_BOTTOM     14
#define DI_DPAD_TOP        15
 int _gear_ = 0;
 int embrayage = 1023;

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);   // X axis
  pinMode(A2, INPUT);   // Y axis
  pinMode(A7, INPUT);   // Y axis

  pinMode(2, INPUT); 
   for(int i=0; i<16; i++) b[i] = 0;
    b[DI_MODE] =0;
 

}

void loop() {
  int x=analogRead(0);                 // X axis
  int y=analogRead(2);                 // Y axis
  int _isreverse = digitalRead(2);
  int last_embrayage = embrayage;
  embrayage = analogRead(7);
  
  int last_gear = _gear_;
  _gear_ = 0;
  if( _isreverse == 1 ){

      _gear_ = 8;
      b[DI_REVERSE]= 1;

  }else{ 
    if(b[DI_MODE]==0)                    // H-shifter mode?
    {
      if(x<400)                  // Shifter on the left?
      {
        if(y>800) _gear_=1;       // 1st gear
        if(y<300) _gear_=2;       // 2nd gear
      }
      else if(x>650)             // Shifter on the right?
      {
        if(y>800) _gear_=5;       // 5th gear
         if(y<300) _gear_=6;       // 6th gear
       
      }
      
      else if(x<600)                             // Shifter is in the middle
      {
        if(y>800) _gear_=3;       // 3rd gear
        if(y<300) _gear_=4;       // 4th gear
      }
     
    }
  }
   

  if(last_gear != _gear_){
       Serial.println(_gear_);
  }
  if(last_embrayage != embrayage){
       Serial.print("e :");
       Serial.print(embrayage);
       Serial.print("\n");
  }

  //Serial.print("x:");
  //Serial.print(x);
  //Serial.print("|");
  //Serial.print("y:");
  //Serial.print(y);
  //Serial.print("|");
  //Serial.print("_gear_:");
  //Serial.print(_gear_);
  //Serial.print("\n");


    
  delay(50);

}
