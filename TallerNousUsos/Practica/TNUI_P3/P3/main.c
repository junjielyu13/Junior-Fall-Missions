/******************************
 *
 * Practica_03_PAE Timers i interrupcions
 * UB, 03/2022.
 *
 *****************************/

#include <msp432p401r.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "lib_PAE.h"

#define LED_V_BIT BIT0
#define LED_RGB_R BIT0
#define LED_RGB_G BIT1
#define LED_RGB_B BIT2
#define BOOSTERPACK_LED_RGB_R BIT6
#define BOOSTERPACK_LED_RGB_G BIT4
#define BOOSTERPACK_LED_RGB_B BIT6

#define SW1_POS 1
#define SW2_POS 4
#define SW1_INT 0x04
#define SW2_INT 0x0A
#define JUP_INT 0x0C
#define JDOWN_INT 0x0A
#define JLEFT_INT 0x0C
#define JRIGHT_INT 0x10
#define JCENTER_INT 0x04
#define SW1_BIT BIT(SW1_POS)
#define SW2_BIT BIT(SW2_POS)

/********************************************************************************************************************
 *
 * ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!!
 *
 * Encontrarás en los siguientes metodos:                          codigo comentado.
 *                                      1 -- config_RGB_LEDS
 *                                      2 -- TA0_0_IRQHandler
 *                                      3 -- TA1_0_IRQHandler
 *
 * Esto se debe a que las luces RGB de boosterpack de nuestro robot de la clase de laboratorio están fundidos
 * y el RGB rojo no es brillante (Robot No. 01)
 *
 * Entonces usamos placa msp432 para hacer las pruebas de funcionamiento. El código comentado en los metodos indicados previamente estan dedicados a placa msp432.
 *
 *
 * Por otra parte, para enviar la practica, también escribimos código específicamente para boosterpack, que no se comenta a continuación.
 * (En situación que cuando la máquina está rota y no podamos realizar ningunas pruebas.)
 *
 *
 * Entonces, cuando descubras que el RGB de boosterpack no funciona como se esperaba, por favor, usas placa msp432.
 * También informamos este problema a nuestro profesor de práctica(Casas Bou Albert) y obtuvimos su consentimiento.
 *
 * ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!! ATENCION!!!!!
 *
********************************************************************************************************************/
typedef struct
{
    bool r, g, b;
    uint8_t time;
} color_t;

color_t color_sequence[] = { { .r = true, .g = false, .b = false, .time = 2 }, // Vermell 2 segons
                             { .r = true, .g = true, .b = false, .time = 1 },  // Groc 1 segons
                             { .r = false, .g = true, .b = false, .time = 3 },  // Verd 3 segons
                             { .r = false, .g = false, .b = true, .time = 2 },  // Blau 2 segons
                             { .r = true, .g = true, .b = true, .time = 1 },  // Blanc 1 segons
        };

int8_t color_sequence_Size = sizeof(color_sequence) / sizeof(color_sequence[0]);

/**************************************************************************
 * INICIALIZACI�N DEL CONTROLADOR DE INTERRUPCIONES (NVIC).
 *
 * Sin datos de entrada
 *
 * Sin datos de salida
 *
 **************************************************************************/
void init_interrupciones()
{
    // Configuracion al estilo MSP430 "clasico":
    // --> Enable Port 1 interrupt on the NVIC.
    // Segun el Datasheet (Tabla "6-39. NVIC Interrupts", apartado "6.7.2 Device-Level User Interrupts"),
    // la interrupcion del puerto 1 es la User ISR numero 35.
    // Segun el Technical Reference Manual, apartado "2.4.3 NVIC Registers",
    // hay 2 registros de habilitacion ISER0 y ISER1, cada uno para 32 interrupciones (0..31, y 32..63, resp.),
    // accesibles mediante la estructura NVIC->ISER[x], con x = 0 o x = 1.
    // Asimismo, hay 2 registros para deshabilitarlas: ICERx, y dos registros para limpiarlas: ICPRx.

    //Int. port 3 = 37 corresponde al bit 5 del segundo registro ISER1:
    NVIC->ICPR[1] |= BIT5; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[1] |= BIT5; //y habilito las interrupciones del puerto
    NVIC->ICPR[1] |= BIT6; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[1] |= BIT6; //y habilito las interrupciones del puerto
    NVIC->ICPR[1] |= BIT7; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[1] |= BIT7; //y habilito las interrupciones del puerto

    //TIMERA0
    NVIC->ICPR[0] |= BIT8; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[0] |= BIT8; //y habilito las interrupciones del puerto
    NVIC->ICPR[0] |= BIT9; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[0] |= BIT9; //y habilito las interrupciones del puerto

    //TIMERA1
    NVIC->ICPR[0] |= BITA; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[0] |= BITA; //y habilito las interrupciones del puerto
    NVIC->ICPR[0] |= BITB; //Primero, me aseguro de que no quede ninguna interrupcion residual pendiente para este puerto,
    NVIC->ISER[0] |= BITB; //y habilito las interrupciones del puerto

}

/**************************************************************************
 * INICIALIZACI�N DE LOS BOTONES & LEDS DEL BOOSTERPACK MK II.
 *
 * Sin datos de entrada
 *
 * Sin datos de salida
 *
 **************************************************************************/
void init_botons(void)
{
    //Configuramos botones
    P4SEL0 &= ~(BIT1 + BIT5 + BIT7 );    //Els polsadors son GPIOs
    P4SEL1 &= ~(BIT1 + BIT5 + BIT7 );    //Els polsadors son GPIOs
    P5SEL0 &= ~(BIT1 + BIT4 + BIT5 );    //Els polsadors son GPIOs
    P5SEL1 &= ~(BIT1 + BIT4 + BIT5 );    //Els polsadors son GPIOs
    P3SEL0 &= ~(BIT5 );                  //Els polsadors son GPIOs
    P3SEL1 &= ~(BIT5 );                  //Els polsadors son GPIOs

    //P4.1 Joystick Centre
    //P4.5 Joystick Esquerra
    //P4.7 Joystick Dreta
    P4DIR &= ~(BIT1 + BIT5 + BIT7 );    //Un polsador es una entrada
    P4REN |= (BIT1 + BIT5 + BIT7 );     //Pull-up/pull-down pel pulsador
    P4OUT |= (BIT1 + BIT5 + BIT7 );     //Donat que l'altra costat es GND, volem una pull-up
    P4IE |= (BIT1 + BIT5 + BIT7 );      //Interrupcions activades
    P4IES &= ~(BIT1 + BIT5 + BIT7 );    //amb transicio L->H
    P4IFG = 0;                          //Netegem les interrupcions anteriors

    //P5.1 Polsador S1
    //P5.4 Joystick Amunt
    //P5.5 Joystick Aval
    P5DIR &= ~(BIT1 + BIT4 + BIT5 );    //Un polsador es una entrada
    P5REN |= (BIT1 + BIT4 + BIT5 );     //Pull-up/pull-down pel pulsador
    P5OUT |= (BIT1 + BIT4 + BIT5 );     //Donat que l'altra costat es GND, volem una pull-up
    P5IE |= (BIT1 + BIT4 + BIT5 );      //Interrupcions activades
    P5IES &= ~(BIT1 + BIT4 + BIT5 );    //amb transicio L->H
    P5IFG = 0;                          //Netegem les interrupcions anteriors

    //P3.5 Polsador S2
    P3DIR &= ~(BIT5 );                  //Un polsador es una entrada
    P3REN |= (BIT5 );                   //Pull-up/pull-down pel pulsador
    P3OUT |= (BIT5 );                   //Donat que l'altra costat es GND, volem una pull-up
    P3IE |= (BIT5 );                    //Interrupcions activades
    P3IES &= ~(BIT5 );                  //amb transicio L->H
    P3IFG = 0;                          //Netegem les interrupcions anteriors
}

/*****************************************************************************
 * CONFIGURACI�N DE LOS LEDs DEL PUERTO 1. A REALIZAR POR EL ALUMNO
 *
 * Sin datos de entrada
 *
 * Sin datos de salida
 *
 ****************************************************************************/
void config_RGB_LEDS(void)
{
    //port.pin dels LEDs RGB als recursos del boosterpack:
    //LEDs RGB = P2.6, P2.4, P5.6
    P2SEL0 &= ~(BIT4 + BIT6 );    //P2.4, P2.6, son GPIOs
    P2SEL1 &= ~(BIT4 + BIT6 );    //P2.4, P2.6, son GPIOs
    P2DIR |= (BIT4 + BIT6 );      //Els LEDs son sortides
    P2OUT &= ~(BIT4 + BIT6 );     //El seu estat inicial sera apagat

    P5SEL0 &= ~(BIT6 );    //P5.6 son GPIOs
    P5SEL1 &= ~(BIT6 );    //P5.6 son GPIOs
    P5DIR |= (BIT6 );      //Els LEDs son sortides
    P5OUT &= ~(BIT6 );     //El seu estat inicial sera apagat

    //borrar tot a baix
    //**********************************************************************************************************
    //port.pin dels LEDs RGB als recursos de la placa msp432
    //
    //Si no se puede usar els RGB del boosterpack, use els RGB de la placa!!!!
    //
    //LED Rojo de placa sota
    /*
    P1SEL0 &= ~(BIT0 );    //P2.0, P2.1, P2.2 son GPIOs
    P1SEL1 &= ~(BIT0 );    //P2.0, P2.1, P2.2 son GPIOs
    P1DIR |= (BIT0 );      //Els LEDs son sortides
    P1OUT &= ~(BIT0 );     //El seu estat inicial sera apagat
    // /LED RGB de placa sota
    P2SEL0 &= ~(BIT0 + BIT1 + BIT2 );   // Los LEDs RGB son GPIOs
    P2SEL1 &= ~(BIT0 + BIT1 + BIT2 );   // Los LEDs RGB son GPIOs
    P2DIR |= (BIT0 + BIT1 + BIT2 );      // Un LED es una salida
    P2OUT &= ~(BIT0 + BIT1 + BIT2 ); // El estado inicial de los LEDs RGB es apagado
    */
    //***********************************************************************************************************

}

void init_timers(void)
{
    //Timer A0, used for red LED PWM
    //Divider = 1; CLK source is SMCLK; clear the counter; MODE is up TIMER_A_CTL_SSEL__SMCLK
    TIMER_A0->CTL = TIMER_A_CTL_ID__1 | TIMER_A_CTL_SSEL__SMCLK
            | TIMER_A_CTL_CLR | TIMER_A_CTL_MC__UP;
    TIMER_A0->CCR[0] = (2400) - 1;     // 1 ms (1 kHz)
    TIMER_A0->CCTL[0] |= TIMER_A_CCTLN_CCIE; //Interrupciones activadas en CCR0

    //Timer A1, used for RGB LEDs
    //Divider = 1; CLK source is ACLK; clear the counter; MODE is up
    TIMER_A1->CTL = TIMER_A_CTL_ID__1 | TIMER_A_CTL_SSEL__ACLK | TIMER_A_CTL_CLR
            | TIMER_A_CTL_MC__UP;
    TIMER_A1->CCR[0] = (1 << 15) - 1;     // 1 Hz
    TIMER_A1->CCTL[0] |= TIMER_A_CCTLN_CCIE; //Interrupciones activadas en CCR0

}

void main(void)
{
    WDTCTL = WDTPW + WDTHOLD;       // Stop watchdog timer

    //Inicializaciones:
    init_ucs_24MHz();
    init_botons();         //Configuramos botones y leds
    config_RGB_LEDS();
    init_interrupciones(); //Configurar y activar las interrupciones de los botones
    init_timers();

    __enable_interrupts();

    //Bucle principal (infinito):
    while (true)
    {
        ;
    }

}

volatile uint8_t limitador = 50;
volatile uint8_t step = 10;
#define CNT_MAX 100
volatile int8_t pwm_duty = 50;

void TA0_0_IRQHandler(void)
{
    static uint8_t cnt = 0;

    TA0CCTL0 &= ~TIMER_A_CCTLN_CCIE;  //Conviene inhabilitar la interrupción al principio
    TA0CCTL0 &= ~TIMER_A_CCTLN_CCIFG; //Clear interrupt flag



    //Si boosterpack no funciona, use este
    //Recuerde activar el código inferior en config_RGB_LEDS
    //este es sirve para controlar la luminosidad de la placa LED1 P1.0:
    /*
    if (cnt == CNT_MAX){
        //Encendemos el LED Rojo
        if(limitador != 0){ //Si el limitador es igual 0 es para mantener las luces apagadas
            P1OUT |= LED_V_BIT;
        }
        cnt = 0;
    }else if (cnt >= limitador){ //Mayor que limitador es significa apagar las luces
        //Apagamos el LED Rojo
        P1OUT &= ~LED_V_BIT;
    }else if (cnt < limitador){ //Menor que limitador es significa encendemos las luces
        //Encendemos el LED Rojo
        P1OUT |= LED_V_BIT;
    }
    */

    //este es sirve para controlar la luminosidad de la boosterpack RGB:
    ///*
    if (cnt == CNT_MAX){
        //Encendemos el LED rojo
        if(limitador != 0){ //Si el limitador es igual 0 es para mantener las luces apagadas
            P2OUT |= BOOSTERPACK_LED_RGB_R;
        }
        cnt = 0;
    }else if (cnt >= limitador){ //Mayor que limitador es significa apagar las luces
        //Apagamos el LED rojo
        P2OUT &= ~(BOOSTERPACK_LED_RGB_R);
    }else if (cnt < limitador){ //Menor que limitador es significa encendemos las luces
        //Encendemos el LED rojo
        P2OUT |= BOOSTERPACK_LED_RGB_R;
    }
    //*/

    cnt++;

    TA0CCTL0 |= TIMER_A_CCTLN_CCIE; //Se debe habilitar la interrupción antes de salir
}

int8_t INDEX = -1;  //estat inicial
uint8_t TIMEPS = 0; //temps inicial

void TA1_0_IRQHandler(void){

    TA1CCTL0 &= ~TIMER_A_CCTLN_CCIE;  //Conviene inhabilitar la interrupción al principio
    TA1CCTL0 &= ~TIMER_A_CCTLN_CCIFG; //Clear interrupt flag

    TIMEPS++;

    if (INDEX == -1 || TIMEPS == color_sequence[INDEX].time){ //Estado inicial o después de completar el último tiempo de luz
        INDEX++;

        if (INDEX == color_sequence_Size){ //Evitar overflow del color sequence
            INDEX = 0;
        }

        TIMEPS = 0;


        //Si boosterpack no funciona, use este
        //este es sirve para controlar la luminosidad de la placa LED1 P1.0:
        //Recuerde activar el código inferior en config_RGB_LEDS
        /*
        if (color_sequence[INDEX].r == true){   //Encendemos el RGB Rojo
            P2OUT |= LED_RGB_R;
        }else{                                  //Apagamos el RGB Rojo
            P2OUT &= ~(LED_RGB_R);
        }

        if (color_sequence[INDEX].g == true){   //Encendemos el RGB amarillo
            P2OUT |= LED_RGB_G;
        }else{                                  //Apagamos el RGB amarillo
            P2OUT &= ~(LED_RGB_G);
        }

        if (color_sequence[INDEX].b == true){   //Encendemos el RGB azul
            P2OUT |= LED_RGB_B;
        }else{                                  //Apagamos el RGB azul
            P2OUT &= ~(LED_RGB_B);
        }
        */



        //este es sirve para controlar la luminosidad de la boosterpack RGB:
        ///*
        if (color_sequence[INDEX].r == true){   //Encendemos el RGB Rojo
            P2OUT |= BOOSTERPACK_LED_RGB_R;
        }else{                                  //Apagamos el RGB Rojo
            P2OUT &= ~(BOOSTERPACK_LED_RGB_R);
        }

        if (color_sequence[INDEX].g == true){   //Encendemos el RGB amarillo
            P2OUT |= BOOSTERPACK_LED_RGB_G;
        }else{                                  //Apagamos el RGB amarillo
            P2OUT &= ~(BOOSTERPACK_LED_RGB_G);
        }

        if (color_sequence[INDEX].b == true){   //Encendemos el RGB azul
            P5OUT |= BOOSTERPACK_LED_RGB_B;
        }else{                                  //Apagamos el RGB azul
            P5OUT &= ~(BOOSTERPACK_LED_RGB_B);
        }
        //*/
    }

    TA1CCTL0 |= TIMER_A_CCTLN_CCIE; //Se debe habilitar la interrupción antes de salir
}

/**************************************************************************
 * RUTINAS DE GESTION DE LOS BOTONES:
 * Mediante estas rutinas, se detectar� qu� bot�n se ha pulsado
 *
 * Sin Datos de entrada
 *
 * Sin datos de salida
 *
 * Actualizar el valor de la variable global estado
 *
 **************************************************************************/

//ISR para las interrupciones del puerto 1:
void PORT3_IRQHandler(void)
{
    uint8_t flag = P3IV; //guardamos el vector de interrupciones. De paso, al acceder a este vector, se limpia automaticamente.
    P3IE &= ~(BIT5 );    //interrupciones del boton S2 en port 3 desactivadas
    //sense acció
    P3IE |= (BIT5 );     //interrupciones S2 en port 3 reactivadas
}

//ISR para las interrupciones del puerto 1:
void PORT4_IRQHandler(void)
{
    uint8_t flag = P4IV; //guardamos el vector de interrupciones. De paso, al acceder a este vector, se limpia automaticamente.
    P4IE &= ~(BIT1 + BIT5 + BIT7 ); //interrupciones del joystick dret, esquerra i centre en port 4 desactivadas

    switch (flag)
    {
    case JCENTER_INT:
        //sense acció
        break;
    case JRIGHT_INT:
        step += 5;      //Joystic dreta: la quantitat step és veu incrementada en 5.
        break;
    case JLEFT_INT:
        step -= 5;      //Joystick esquerra: la quantitat step és veu decrementada en 5.
        break;
    default:
        break;
    }

    P4IE |= (BIT1 + BIT5 + BIT7 );   //interrupciones del joystick dret, esquerra i centre en port 4 reactivades
}

//ISR para las interrupciones del puerto 1:
void PORT5_IRQHandler(void)
{
    uint8_t flag = P5IV; //guardamos el vector de interrupciones. De paso, al acceder a este vector, se limpia automaticamente.
    P5IE &= ~(BIT1 + BIT4 + BIT5 ); //interrupciones del joystick amunt, avall i el polsador S1  en port 5 desactivadas

    switch (flag)
    {
    case SW1_INT:
        //sense acció
        break;
    case JUP_INT:
        limitador += step;      //Joystick amunt: increment d’aquest valor en una quantitat step
        break;
    case JDOWN_INT:
        limitador -= step;      //Joystick avall: decrement d’aquest valor en una quantitat step
        break;
    default:
        break;
    }

    P5IE |= (BIT1 + BIT4 + BIT5 );   //interrupciones del joystick amunt, avall i el polsador S1  en port 5 reactivades
}
