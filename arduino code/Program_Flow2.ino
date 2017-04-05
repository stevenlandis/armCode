#include <Servo.h>
#include <Stepper.h>

Servo servo;

Stepper step1(200, 2, 3, 4, 5);
Stepper step2(200, 6, 7, 8, 9);

const int stepperSpeed = 5;
const int moveSpeed = 20;

bool penDown = false;

float currentA1 = 0;
float currentA2 = 0;

bool debug = false;

//number of instructions
int n_instr;

//dynamic array for the instructions
int* inst;

//dynamic array for the instruction arguments
float* data;

//reads in a floating point number from the serial bus
float readFloat() {
  unsigned int A = Serial.read();
  unsigned int B = Serial.read();
  float angle = ((double)(B+(A<<8)))/16-2048;
  return angle;
}

//reads in a two byte integer from serial
unsigned int readLongInt() {
  unsigned int A = Serial.read();
  unsigned int B = Serial.read();
  return B+(A<<8);
}

//reads a byte integer from the serial bus
int readInt() {
  return Serial.read();
}

//returns the difference between two angles
//finds the shortest difference between two angles
//prevents the arm from moving all the way around when moving from 599 to 1
float dAngle(float init, float fin) {
  float d = fin - init;
  if (d > 300) {
    return d - 600;
  }
  if (d < -300) {
    return d + 600;
  }
  return d;
}

//gives the sign of n
//there may be a better way to do this...
float sign(float n) {
  if (n < 0) {
    return -1;
  }
  return 1;
}

//lifts the pen up
void penup() {
  servo.write(0);
  delay(1000);
  penDown = false;
}

//lowers the pen
void pendown() {
  servo.write(180);
  delay(1000);
  penDown = true;
}

//moves the pen to the angles using the shortest path
void movePen(float a1, float a2) {
  if (penDown) {
    step1.setSpeed(stepperSpeed);
    step2.setSpeed(stepperSpeed);
  } else {
    step1.setSpeed(moveSpeed);
    step2.setSpeed(moveSpeed);
  }
  
  float start1 = currentA1;
  float start2 = currentA2;
  float DA1 = dAngle(currentA1, a1);
  float DA2 = dAngle(currentA2, a2);
  if (debug) {
    Serial.println("Moving:");
    Serial.print("\tFrom: ");
    Serial.print(currentA1);
    Serial.print(", ");
    Serial.println(currentA2);
    Serial.print("\tTo: ");
    Serial.print(a1);
    Serial.print(", ");
    Serial.println(a2);
    Serial.print("\tChange: ");
    Serial.print(DA1);
    Serial.print(", ");
    Serial.println(DA2);
  }
  if (fabs(DA1) > fabs(DA2)) {
    //a1 moves more so limit it
    if (debug) {
      Serial.println("\tLimiting: a1");
    }
    int steps = floor(fabs(DA1));
    for (int i = 0; i < steps; i++) {
      if (DA1 > 0) {
        step1.step(1);
        currentA1++;
      } else {
        step1.step(-1);
        currentA1--;
      }
      float correspondingA2 = start2 + DA2 * (currentA1 - start1) / DA1;
      if (fabs(dAngle(correspondingA2, currentA2)) > 1) {
        if (DA2 > 0) {
          step2.step(1);
          currentA2++;
        } else {
          step2.step(-1);
          currentA2--;
        }
      }
    }
  } else {
    //a2 moves more than a1
    if (debug) {
      Serial.println("\tLimiting: a2");
    }
    int steps = floor(fabs(DA2));
    for (int i = 0; i < steps; i++) {
      if (DA2 > 0) {
        step2.step(1);
        currentA2++;
      } else {
        step2.step(-1);
        currentA2--;
      }
      float correspondingA1 = start1 + DA1 * (currentA2 - start2) / DA2;
      if (fabs(dAngle(correspondingA1, currentA1)) > 1) {
        if (DA1 > 0) {
          step1.step(1);
          currentA1++;
        } else {
          step1.step(-1);
          currentA1--;
        }
      }
    }
  }
}

//executes instruction I with arguments a1 and a2
void execute(int I, float a1, float a2) {
  if (I == 2) {
    penup();
  } else if (I == 3) {
    pendown();
  } else if (I == 4) {
    movePen(a1, a2);
  }
}

void setup() {
  servo.attach(10);
  penup();

  step1.setSpeed(stepperSpeed);
  step2.setSpeed(stepperSpeed);
  
  Serial.begin(9600);

  //used to end the following while loops
  bool received = false;

  //waiting for the start instruction
  while (!received) {
    if (Serial.available() > 0) {
      int message = readInt();
      //1 is the start instruction
      if (message == 1) {
        //echo the start instruction so the computer knows to start
        Serial.println(message);
        received = true;
      }
    }
  }

  //waiting for the number of instructions
  received = false;
  while (!received) {
    if (Serial.available() > 1) {
      n_instr = readLongInt();

      //echo the number of instructions to check with the computer
      Serial.println(n_instr);
      received = true;
    }
  }

  //allocate the arrays to store the instructions
  inst = (int*) malloc(n_instr * sizeof(int));
  data = (float*) malloc(2 * n_instr * sizeof(float));

  //for every instruction...
  for (int i = 0; i < n_instr; i++) {

    //read the instruction code
    received = false;
    while (!received) {
      if (Serial.available() > 0) {
        inst[i] = readInt();
        received = true;
      }
    }

    //read the first argument
    received = false;
    while (!received) {
      if (Serial.available() > 1) {
        data[2*i] = readFloat();
        received = true;
      }
    }

    //read the second argument
    received = false;
    while (!received) {
      if (Serial.available() > 1) {
        data[2*i+1] = readFloat();
        received = true;
      }
    }
  }

  //echo the instructions for debugging
  if (debug) {
    for (int i = 0; i < n_instr; i++) {
      Serial.print(inst[i], DEC);
      Serial.print(": ");
      Serial.print(data[2*i], DEC);
      Serial.print(", ");
      Serial.println(data[2*i+1], DEC);
    }
  }

  //execute the isntructions
  for (int i = 0; i < n_instr; i++) {
    execute(inst[i], data[2*i], data[2*i+1]);
  }

  //lift the pen up at the end
  penup();
  movePen(0, 0);

  Serial.println("Finished drawing!");
}

//we don't need the loop!
void loop() {
  
}
