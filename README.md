# shellfeck
A BrainF*ck Inspired Shell Obfuscation Proof-of-Concept

This is a proof-of-concept that combines a modified BrainF\*ck interpreter and shell command obfuscation. The instruction set used is the same as BrainF\*ck, with the exception that instead of `,` getting input, it calls `system()` with the output so far, and clears the output in doing so.

The purpose of this is to finally make a BrainF\*ck interpreter, which I don't think I've done before, and to combine it with obfuscation. Instead of having a payload of only 8 characters, which is discernable as BrainF\*ck characters and easy to write signatures for, it maps every possible value for 8 bits to one of the 8 BrainF*ck commands. The mapping is weighted based on how prevelant the particular command is in the generated payload (that is to say, if the `+` command comprises 90% of the generated payload, then ~90% of the 256 bytecodes will be mapped to the `+` command.

**TODO:** - Clean this up

## Usage

  - Run `.\generate_shellfeck_instructions.py --command <command>`
    - _Note: By default it will use a random algorithm. Recommend specifying `--algo sstelian` if you want a smaller instruction payload`_
  - Compile with `gcc shellfeck.c`
  - Run the compiled executable!

## Algorithms

  - **simple** - Super simple algorithm that only uses `+` and `>` to generate the output.
  - **simple-alternate** - Super simple algorithm that alternates between using `+>` and `->` for each letter of the output.
  - **simple-delta** - Super simple algorithm that generates the output by calculating the delta between the letter to be generated and the previously generated letter.
  - **simple-reverse** - Super simple algorithm that only uses `-` and `<` to generate the output.
  - **sstelian** _Recommended_ - Uses an algorithm almost entirely based on https://github.com/sstelian/Text-to-Brainfuck, is the only one that makes use of the `[` and `]` characters, so its payloads will be shorter than the other algorithm.s
