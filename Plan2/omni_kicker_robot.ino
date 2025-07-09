// === Motor Omni ===
#define M1_IN1 25
#define M1_IN2 26
#define M1_PWM 27
#define M1_CH 0

#define M2_IN1 32
#define M2_IN2 33
#define M2_PWM 14
#define M2_CH 1

#define M3_IN1 12
#define M3_IN2 13
#define M3_PWM 4
#define M3_CH 2

// === Kicker ===
#define KICK_IN1 2
#define KICK_IN2 15
#define KICK_PWM 5
#define KICK_CH 3

void setupMotorPin(int in1, int in2, int pwmPin, int ch) {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  ledcSetup(ch, 1000, 8);
  ledcAttachPin(pwmPin, ch);
}

void setMotor(int in1, int in2, int ch, int pwm) {
  pwm = constrain(pwm, -255, 255);
  if (pwm > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    ledcWrite(ch, pwm);
  } else if (pwm < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    ledcWrite(ch, -pwm);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    ledcWrite(ch, 0);
  }
}

void kick(int power) {
  digitalWrite(KICK_IN1, HIGH);
  digitalWrite(KICK_IN2, LOW);
  ledcWrite(KICK_CH, power);
}

void stopKick() {
  digitalWrite(KICK_IN1, LOW);
  digitalWrite(KICK_IN2, LOW);
  ledcWrite(KICK_CH, 0);
}

void setup() {
  Serial.begin(115200);

  setupMotorPin(M1_IN1, M1_IN2, M1_PWM, M1_CH);
  setupMotorPin(M2_IN1, M2_IN2, M2_PWM, M2_CH);
  setupMotorPin(M3_IN1, M3_IN2, M3_PWM, M3_CH);
  setupMotorPin(KICK_IN1, KICK_IN2, KICK_PWM, KICK_CH);
}

void loop() {
  static String input = "";

  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      if (input.startsWith("M")) {
        int s1, s2, s3;
        sscanf(input.c_str(), "M%d,%d,%d", &s1, &s2, &s3);
        setMotor(M1_IN1, M1_IN2, M1_CH, s1);
        setMotor(M2_IN1, M2_IN2, M2_CH, s2);
        setMotor(M3_IN1, M3_IN2, M3_CH, s3);
      } else if (input.startsWith("K")) {
        int state;
        sscanf(input.c_str(), "K%d", &state);
        if (state)
          kick(255);
        else
          stopKick();
      }
      input = "";
    } else {
      input += c;
    }
  }
}