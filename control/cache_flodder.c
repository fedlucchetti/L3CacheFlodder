#include<stdint.h>

#define KB 1024

void flush_icache() {
asm volatile (
".rept (32*1024)\n\t"
"mov %%rax, %%rax\n\t"
".endr\n\t" ::: "memory");
}

unsigned int volatile flood_area[32*KB*KB];

void flush_data() {
	for (int i = 0; i < 32*KB*KB; i++)
		flood_area[i] = i;
}

void main() {
	flush_data();
	flush_icache();
}