Table data;
int angleY = 0;
int angleZ = 0;
int range = 10;
int low = 18;
boolean held;
void setup() {
  size(600, 600, P3D);
  translate(width/2,height/2,0);
  camera(height, 0, 0, 0, 0, 0, 0, 0, 1);
  data = loadTable("therm.csv");
  strokeWeight(5);
  //if(data.getRowCount()!=360 || data.getColumnCount()!=180){
  //  println("Invalid file, must be 360x180 (theta,phi)");
  //}
  
}

void draw() {
  background(255);
  if(keyPressed){
    if (key == CODED) {
      if (keyCode == UP) {
        angleY++;
      } else if (keyCode == DOWN) {
        angleY--;
      } else if (keyCode == RIGHT) {
        angleZ++;
      } else if (keyCode == LEFT) {
        angleZ--;
      }
    }
  }
  rotateY(radians(angleY));
  rotateZ(radians(angleZ));
  
  for(int i=0;i<26880;i++){
     float x = cos(radians(data.getFloat(0,i)))*sin(radians(data.getFloat(1,i)));
     float y = sin(radians(data.getFloat(0,i)))*sin(radians(data.getFloat(1,i)));
     float z = -cos(radians(data.getFloat(1,i)));
     setStroke(data.getFloat(2,i));
     int scale = 200;
     point(x*scale,y*scale,z*scale);
  }
  
  //for(int i = 0; i < 360; i++){
  // for(int j = 0; j < 180; j++){
  //   float x = cos(radians(i))*sin(radians(j));
  //   float y = sin(radians(i))*sin(radians(j));
  //   float z = -cos(radians(j));
  //   setStroke(data.getFloat(i,j));
  //   int scale = 200;
  //   point(x*scale,y*scale,z*scale);
     
  // }
  //}
}

void setStroke(float temp){
  int r, b;
  //if (temp >= 35) {
  //    r = 255;
  //    g = (int) (255 * (temp - 35) / 15);
  //    b = 0;
  //}else if (temp >=20) {
  //    r = (int)(255*(temp-20)/15);
  //    g = 255;
  //    b = 0;
  //} else if (temp >= 5){
  //    r = 0;
  //    g = 255;
  //    b = (int)(255 - 255 * (temp-5)/15);
  //} else {
  //    r = 0;
  //    g= (int) (255 * (temp+10) / 15);
  //    b = 255;
  //}
  //if (r < 0) r = 0;
  //if (r > 255) r = 255;
  //if (b < 0) b = 0;
  //if ( b > 255) b = 255;
  //if(g<0) g=0;
  //if(g>255)g=255;
  
  if (temp >= low+range/2) {
      r = 255;
      b = (int) (255 - 255 * (temp - (low+range/2)) / (range/2));
  } else {
      b = 255;
      r = (int) (255 * (temp - low) / (range/2));
  }
  if (r < 0) r = 0;
  if (b < 0) b = 0;
  stroke(r, 0, b);
}
