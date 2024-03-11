#include <stdio.h>
#include <stdlib.h>

#include "shellfeck.h"
#include "shellfeck_instrs.h"

#define OUTPUT_SIZE_CHUNK 8

void main()
{
    sf_machine_state_t state;

    // Setup machine state
    state.instructions_size = shellfeck_instruction_array_size;
    state.instructions = shellfeck_instruction_array;
    state.data = (sf_data_array_node_t*) malloc(sizeof(sf_data_array_node_t));
    state.output_size = OUTPUT_SIZE_CHUNK;
    state.output = (char*) malloc(state.output_size * sizeof(char));

    while(state.instruction_pointer < state.instructions_size)
    {
        shellfeck_instruction_func[state.instructions[state.instruction_pointer]](&state);
    }

    return;
}

void sf_inc_dp(sf_machine_state_t* state)
{
    if(state->data->next == NULL)
    {
        state->data->next = (sf_data_array_node_t*) malloc(sizeof(sf_data_array_node_t));
    }
    state->data->next->prev = state->data;
    state->data = state->data->next;
    state->instruction_pointer++;
}
void sf_dec_dp(sf_machine_state_t* state)
{
    if(state->data->prev == NULL)
    {
        state->data->prev = (sf_data_array_node_t*) malloc(sizeof(sf_data_array_node_t));
    }
    state->data->prev->next = state->data;
    state->data = state->data->prev;
    state->instruction_pointer++;
}
void sf_inc_val(sf_machine_state_t* state)
{
    state->data->value++;
    state->instruction_pointer++;
}
void sf_dec_val(sf_machine_state_t* state)
{
    state->data->value--;
    state->instruction_pointer++;
}
void sf_output(sf_machine_state_t* state)
{
    state->output[state->output_i] = state->data->value;
    state->output_i++;
    state->instruction_pointer++;

    if(state->output_i >= state->output_size)
    {
        state->output_size += OUTPUT_SIZE_CHUNK;
        state->output = (char*) realloc(state->output, state->output_size);
    }
}
void sf_call(sf_machine_state_t* state)
{
    system(state->output);
    state->instruction_pointer++;
    free(state->output);
    state->output_size = OUTPUT_SIZE_CHUNK;
    state->output = (char*) malloc(state->output_size * sizeof(char));
}
void sf_if(sf_machine_state_t* state)
{
    if(state->data->value == 0)
    {
        int counter = 0;
        unsigned int instruction_seeker = state->instruction_pointer;
        while(1)
        {
            instruction_seeker++;
            if(shellfeck_instruction_func[state->instructions[instruction_seeker]] == sf_if)
            {
                counter++;
            }
            else if(shellfeck_instruction_func[state->instructions[instruction_seeker]] == sf_endif)
            {
                counter--;
                if(counter <= 0)
                {
                    state->instruction_pointer = instruction_seeker;
                    break;
                }
            }
        }
    }
    state->instruction_pointer++;
}
void sf_endif(sf_machine_state_t* state)
{
    if(state->data->value != 0)
    {
        int counter = 0;
        unsigned int instruction_seeker = state->instruction_pointer;
        while(1)
        {
            instruction_seeker--;
            if(shellfeck_instruction_func[state->instructions[instruction_seeker]] == sf_endif)
            {
                counter++;
            }
            else if(shellfeck_instruction_func[state->instructions[instruction_seeker]] == sf_if)
            {
                counter--;
                if(counter <= 0)
                {
                    state->instruction_pointer = instruction_seeker;
                    break;
                }
            }
        }
    }
    state->instruction_pointer++;
}