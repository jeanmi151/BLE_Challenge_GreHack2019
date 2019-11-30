#include <wiringPi.h>
#include <stdio.h>
#include <string.h>

// compile on pi gcc test-blink.c  -o blinkme -lwiringPi

#define LedPin 5

void print_long(void){	
	digitalWrite(LedPin, HIGH);  //led on
	delay(2000);
    digitalWrite(LedPin, LOW);  //led off
}

void print_short(void){	
	digitalWrite(LedPin, HIGH);  //led on
	delay(1000);
    digitalWrite(LedPin, LOW);  //led off
}

void decode_int(int n) {
    // array to store binary number
    int binaryNum[6];

    // counter for binary array
    int i = 0;
    while (n > 0) {
        // storing remainder in binary array
        binaryNum[i] = n % 2;
        n = n / 2;
        i++;
    }
    // printing binary array in reverse order
    for (int j = i - 1; j >= 0; j--) {
        //printf("%i", binaryNum[j]);
        if(binaryNum[j] == 0){ //printf(" aaaa 0\n");
            print_short();
        } else{ //printf(" aaaa 1\n");
            print_long();
        }
        delay(1000);
    }
    //printf("\n");
}
void decode_binstr(char sstring){
    //printf("%i\n", sizeof(sstring));
    //fprintf("%x\n", sstring);
    //printf("%c\n", sstring);
    if(sstring == '0'){ print_short(); //printf("str 0\n");
    }
    else{ print_long();//        printf("str 1 \n");
    }
}
int main(void) {
	int i = 0, d = 0;
	//char flagstr[][5] = {" ", "0000", "01111", " ", " ", "01", " ", "001", "0", " ", "0", "000", " ", " "};
	//int flagint[] = {6, -1, -1, 30, 22, -1, 13, -1, -1, 1, -1, -1, 1, 45};

    char flagstr[][5] = { "", "0000", "01111", "", "", "", "0", "", "", "", "0", "", "", "010", "000", "00011", "0010", "01111", "010", "", "011", "00001", "010", "00011", ""};

    int flagint[] =  { 6, -1, -1, 30, 22, 4, -1, 10, 31, 4, -1, 3, 31, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 45 };

	if(wiringPiSetup() == -1) { //when initialize wiringPi failed, print message to screen
        printf("setup wiringPi failed !\n");
        return -1;
    }

    pinMode(LedPin, OUTPUT);
	/*
	printf("%s\n", flagstr[0]);
	printf("%s\n",flagstr[1]);
	printf("%s\n",flagstr[2]);
	printf("%i\n",flagint[0]);
	printf("%i\n",flagint[1]);*/

	// startup of the firmware
	digitalWrite(LedPin, HIGH);
	printf("HIGH for 3sec\n");
	delay(3000);
	digitalWrite(LedPin, LOW);
	printf("LOW for 3sec\n");
	delay(3000);
	digitalWrite(LedPin, HIGH);
	printf("HIGH for 3sec\n");
	delay(3000);
	digitalWrite(LedPin, LOW);
	printf("LOW for 3sec\n");
	delay(6000);

	for(i=0; i<sizeof(flagint); i++){
		// if flagint[-1] == -1 mean need to use flagstr
		if(flagint[i] != -1){ decode_int(flagint[i]); }
		else{
		    //printf("first char is : %c \n", flagstr[i][0]);
		    //printf("strlen : %i \n", strlen(flagstr[i]));

		    for(d=0; d<strlen(flagstr[i]); d++){
		        //printf("will send %c\n", flagstr[i][d]);
			    decode_binstr(flagstr[i][d]);
			    delay(1000);
			}
			//printf("Not implemented yet\n");
		}
	}
    delay(5000);

    while(i<10) {
        digitalWrite(LedPin, LOW);   //led on
        printf("led on\n");
        delay(1000);			     // wait 1 sec
        digitalWrite(LedPin, HIGH);  //led off
        printf("led off\n");
        delay(1000);                 // wait 1 sec
        i++;
    }
    digitalWrite(LedPin, LOW);   //led on
    return 0;
}
