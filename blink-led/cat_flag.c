#include<stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

// compile on pi gcc test-blink.c  -o blinkme -lwiringPi

#define LedPin 5

int main() {
   FILE *fp;
   char s;

   char path[1035];

   if(wiringPiSetup() == -1) { //when initialize wiringPi failed, print message to screen
        printf("setup wiringPi failed !\n");
        return -1;
   }
   pinMode(LedPin, OUTPUT);
   delay(1000);
   digitalWrite(LedPin, HIGH);



  /* Open the command for reading. */
  fp = popen("/bin/cat /flag", "r");
  if (fp == NULL) {
    printf("Failed to run command\n" );
    exit(1);
  }

  /* Read the output a line at a time - output it. */
  while (fgets(path, sizeof(path)-1, fp) != NULL) {
    printf("%s", path);
  }

  /* close */
  pclose(fp);


   printf("\n");
   return 0;
}
