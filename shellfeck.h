#ifndef SHELLFECK_HEADER_FILE
#define SHELLFECK_HEADER_FILE

#include <stdint.h>

typedef struct sf_data_array_node
{
    struct sf_data_array_node* prev;
    uint8_t value;
    struct sf_data_array_node* next;
} sf_data_array_node_t;

typedef struct sf_machine_state
{
    unsigned char* instructions;
    unsigned int instructions_size;
    unsigned int instruction_pointer;
    sf_data_array_node_t* data;
    char* output;
    unsigned int output_i;
    unsigned int output_size;
} sf_machine_state_t;

void sf_inc_dp(sf_machine_state_t* state);
void sf_dec_dp(sf_machine_state_t* state);
void sf_inc_val(sf_machine_state_t* state);
void sf_dec_val(sf_machine_state_t* state);
void sf_output(sf_machine_state_t* state);
void sf_call(sf_machine_state_t* state);
void sf_if(sf_machine_state_t* state);
void sf_endif(sf_machine_state_t* state);

#endif