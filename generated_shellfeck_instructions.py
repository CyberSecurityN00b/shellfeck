#!/usr/bin/env python3
import argparse
import random

def generate_shellfeck(bf,header):
    inc_dp_cnt  = bf.count(">")
    dec_dp_cnt  = bf.count("<")
    inc_val_cnt = bf.count("+")
    dec_val_cnt = bf.count("-")
    output_cnt  = bf.count(".")
    call_cnt    = bf.count(",")
    if_cnt      = bf.count("[")
    endif_cnt   = bf.count("]")

    inc_dp_need  = int((inc_dp_cnt  / len(bf)) * 256)
    dec_dp_need  = int((dec_dp_cnt  / len(bf)) * 256)
    inc_val_need = int((inc_val_cnt / len(bf)) * 256)
    dec_val_need = int((dec_val_cnt / len(bf)) * 256)
    output_need  = int((output_cnt  / len(bf)) * 256)
    call_need    = int((call_cnt    / len(bf)) * 256)
    if_need      = int((if_cnt      / len(bf)) * 256)
    endif_need   = int((endif_cnt   / len(bf)) * 256)

    instr_string =  (">" * inc_dp_need)  + \
                    ("<" * dec_dp_need)  + \
                    ("+" * inc_val_need) + \
                    ("-" * dec_val_need) + \
                    ("." * output_need)  + \
                    ("," * call_need)    + \
                    ("[" * if_need)      + \
                    ("]" * endif_need)
    instr_string = ''.join(random.sample(instr_string,len(instr_string)))
    instr_string = ("><+-.,[]" + instr_string)[:256]
    instr_string = ''.join(random.sample(instr_string,len(instr_string)))

    inc_dp_list  = []
    dec_dp_list  = []
    inc_val_list = []
    dec_val_list = []
    output_list  = []
    call_list    = []
    if_list      = []
    endif_list   = []

    for i in range(256):
        c = instr_string[i]
        if c == ">": inc_dp_list.append(i)
        if c == "<": dec_dp_list.append(i)
        if c == "+": inc_val_list.append(i)
        if c == "-": dec_val_list.append(i)
        if c == ".": output_list.append(i)
        if c == ",": call_list.append(i)
        if c == "[": if_list.append(i)
        if c == "]": endif_list.append(i)

    instr_bytes_list = []

    for c in bf:
        if c == ">": instr_bytes_list.append(random.choice(inc_dp_list))
        if c == "<": instr_bytes_list.append(random.choice(dec_dp_list))
        if c == "+": instr_bytes_list.append(random.choice(inc_val_list))
        if c == "-": instr_bytes_list.append(random.choice(dec_val_list))
        if c == ".": instr_bytes_list.append(random.choice(output_list))
        if c == ",": instr_bytes_list.append(random.choice(call_list))
        if c == "[": instr_bytes_list.append(random.choice(if_list))
        if c == "]": instr_bytes_list.append(random.choice(endif_list))

    with open(header,"w") as f:
        f.write("#ifndef SHELLFECK_INSTRUCTIONS_HEADER\n")
        f.write("#define SHELLFECK_INSTRUCTIONS_HEADER\n")
        f.write("\n")
        f.write("#include \"shellfeck.h\"\n")
        f.write("\n")
        f.write(f"unsigned int shellfeck_instruction_array_size = {len(instr_bytes_list)};\n")
        f.write("\n")
        f.write("unsigned char shellfeck_instruction_array[] = {\n")

        for i in range(0, len(instr_bytes_list), 16):
            f.write(f"\t{', '.join([hex(x) for x in instr_bytes_list[i:i + 16]])},\n")

        f.write("};\n")
        f.write("\n")
        f.write("void (*shellfeck_instruction_func[256])(sf_machine_state_t* state) = {\n")

        for c in instr_string:
            if c == ">": f.write(f"\tsf_inc_dp,\n")
            if c == "<": f.write(f"\tsf_dec_dp,\n")
            if c == "+": f.write(f"\tsf_inc_val,\n")
            if c == "-": f.write(f"\tsf_dec_val,\n")
            if c == ".": f.write(f"\tsf_output,\n")
            if c == ",": f.write(f"\tsf_call,\n")
            if c == "[": f.write(f"\tsf_if,\n")
            if c == "]": f.write(f"\tsf_endif,\n")

        f.write("};\n")
        f.write("\n")
        f.write("#endif\n")

        print(f" - Generated header file with {len(instr_bytes_list)} instructions.")

def generate_bf_simple(cmd):
    result = ""

    for c in cmd:
        result += "+"*ord(c) + ".>"

    result += ","
    return result

def generate_bf_simple_reverse(cmd):
    result = ""

    for c in cmd:
        result += "-"*(256-ord(c)) + ".<"

    result += ","
    return result

def generate_bf_simple_delta(cmd):
    result = ""

    for i,c in enumerate(cmd):
        if i == 0:
            result += "+"*ord(c) + "."
        else:
            d = ord(cmd[i]) - ord(cmd[i-1])
            if d > 0:
                result += "+"*d + "."
            else:
                result += "-"*abs(d) + "."


    result += ","
    return result

def generate_bf_simple_alternate(cmd):
    result = ""

    for i,c in enumerate(cmd):
        if i == 0 or not i % 2:
            result += "+"*ord(c) + ".>"
        else:
            result += "-"*(256-ord(c)) + ".>"

    result += ","
    return result

def generate_bf_sstelian(cmd):
    # Based on https://github.com/sstelian/Text-to-Brainfuck
    def char_to_bf(c):
        buffer = "[-]>[-]<"
        for i in range(ord(c)//10):
            buffer += "+"
        buffer += "[>++++++++++<-]>"
        for i in range(ord(c)%10):
            buffer += "+"
        buffer += ".<"
        return buffer
    
    def delta_to_bf(d):
        buffer = ""
        for i in range(abs(d)//10):
            buffer += "+"
        if d > 0:
            buffer = buffer + "[>++++++++++<-]>"
        else:
            buffer = buffer + "[>----------<-]>"
        for i in range(abs(d)%10):
            if d > 0:
                buffer += "+"
            else:
                buffer += "-"
        buffer += ".<"
        return buffer
    
    result = ""

    for i,c in enumerate(cmd):
        if i == 0:
            result += char_to_bf(c)
        else:
            d = ord(cmd[i]) - ord(cmd[i-1])
            result += delta_to_bf(d)

    result += ","
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser("")
    parser.add_argument("--command",default="+[------->++<]>.---------.[--->+<]>---.-.+.+[->+++<]>++.--[--->+<]>-.[---->+<]>+++.--[-->+++<]>.--[----->+<]>+.----.-----------.+++++++++++++.++++++.+.")
    parser.add_argument("--header", default="shellfeck_instrs.h")
    parser.add_argument("--algo", choices={"random","simple","sstelian","simple-reverse","simple-delta","simple-alternate"}, default="random")
    args = parser.parse_args()

    algo = args.algo
    if algo == "random":
        algo = random.choice(["simple","sstelian","simple-reverse","simple-delta","simple-alternate"])

    if algo == "simple":
        bf = generate_bf_simple(args.command)
    elif algo == "sstelian":
        bf = generate_bf_sstelian(args.command)
    elif algo == "simple-reverse":
        bf = generate_bf_simple_reverse(args.command)
    elif algo == "simple-delta":
        bf = generate_bf_simple_delta(args.command)
    elif algo == "simple-alternate":
        bf = generate_bf_simple_alternate(args.command)
    else:
        bf = generate_bf_simple(args.command)
    print(f" - Generating with algorithm {algo}")
    generate_shellfeck(bf,args.header)
    print(f" - Generated instructions:")
    print(bf)