/*
 * Copyright (c) 2019-2021, 2023 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#ifdef __aarch64__

template<>
void interleave_block<8, 1, VLType::None, true>(
  uint16_t * &out_ptr, const uint16_t * const * in, size_t width, size_t height,
  size_t row_offset, bool first
)
{
  __asm__ __volatile__(
      "ldr x28, [%x[in], #0x0]\n"
      "ldr x27, [%x[in], #0x8]\n"
      "cmp %x[height], #0x8\n"
      "mov x20, #0x0\n"
      "ldr x26, [%x[in], #0x10]\n"
      "ldr x25, [%x[in], #0x18]\n"
      "movi v2.8h, #0x0\n"
      "movi v1.4s, #0x0\n"
      "ldr x24, [%x[in], #0x20]\n"
      "ldr x23, [%x[in], #0x28]\n"
      "movi v0.4s, #0x0\n"
      "add x28, x28, %x[row_offset], LSL #1\n"
      "ldr x22, [%x[in], #0x30]\n"
      "ldr x21, [%x[in], #0x38]\n"
      "add x27, x27, %x[row_offset], LSL #1\n"
      "add x26, x26, %x[row_offset], LSL #1\n"
      "add x25, x25, %x[row_offset], LSL #1\n"
      "add x24, x24, %x[row_offset], LSL #1\n"
      "add x23, x23, %x[row_offset], LSL #1\n"
      "add x22, x22, %x[row_offset], LSL #1\n"
      "add x21, x21, %x[row_offset], LSL #1\n"
      "beq 1f\n"
      "cmp %x[height], #0x2\n"
      "csel x27, x27, x28, GE\n"
      "csel x26, x26, x28, GT\n"
      "cmp %x[height], #0x4\n"
      "csel x25, x25, x28, GE\n"
      "csel x24, x24, x28, GT\n"
      "cmp %x[height], #0x6\n"
      "mov x21, x28\n"
      "csel x23, x23, x28, GE\n"
      "csel x22, x22, x28, GT\n"
      "1:"  // no_pointer_adj
      "prfm pldl1keep, [x28, #0x0]\n"
      "prfm pldl1keep, [x27, #0x0]\n"
      "prfm pldl1keep, [x26, #0x0]\n"
      "prfm pldl1keep, [x25, #0x0]\n"
      "prfm pldl1keep, [x24, #0x0]\n"
      "prfm pldl1keep, [x23, #0x0]\n"
      "prfm pldl1keep, [x22, #0x0]\n"
      "prfm pldl1keep, [x21, #0x0]\n"
      "prfm pldl1keep, [x28, #0x40]\n"
      "prfm pldl1keep, [x27, #0x40]\n"
      "prfm pldl1keep, [x26, #0x40]\n"
      "prfm pldl1keep, [x25, #0x40]\n"
      "prfm pldl1keep, [x24, #0x40]\n"
      "prfm pldl1keep, [x23, #0x40]\n"
      "prfm pldl1keep, [x22, #0x40]\n"
      "prfm pldl1keep, [x21, #0x40]\n"
      "cbnz %w[first], 2f\n"
      "sub %x[out_ptr], %x[out_ptr], #0x20\n"
      "ld1 { v1.4s }, [%x[out_ptr]]\n"
      "ldr q0, [%x[out_ptr], #0x10]\n"
      "2:"  // first_pass
      "cmp %x[width], #0x8\n"
      "blt 5f\n"
      "3:"  // Main loop head
      "cmp x20, #0xe\n"
      "ble 4f\n"
      "uaddw v1.4s, v1.4s, v2.4h\n"
      "uaddw2 v0.4s, v0.4s, v2.8h\n"
      "mov x20, #0x0\n"
      "movi v2.8h, #0x0\n"
      "4:"  // no_accumulate_16
      "ldr q31, [x28], #0x10\n"
      "ldr q30, [x27], #0x10\n"
      "subs %x[width], %x[width], #0x8\n"
      "cmp %x[width], #0x8\n"
      "ldr q29, [x26], #0x10\n"
      "ldr q28, [x25], #0x10\n"
      "add x20, x20, #0x1\n"
      "ldr q27, [x24], #0x10\n"
      "ldr q26, [x23], #0x10\n"
      "zip1 v25.8h, v31.8h, v27.8h\n"
      "zip1 v22.8h, v30.8h, v26.8h\n"
      "ldr q24, [x22], #0x10\n"
      "ldr q23, [x21], #0x10\n"
      "zip1 v18.8h, v29.8h, v24.8h\n"
      "zip1 v21.8h, v28.8h, v23.8h\n"
      "zip1 v17.8h, v25.8h, v18.8h\n"
      "zip1 v16.8h, v22.8h, v21.8h\n"
      "prfm pldl1keep, [x28, #0x70]\n"
      "prfm pldl1keep, [x27, #0x70]\n"
      "zip1 v20.8h, v17.8h, v16.8h\n"
      "add v2.8h, v2.8h, v20.8h\n"
      "prfm pldl1keep, [x26, #0x70]\n"
      "prfm pldl1keep, [x25, #0x70]\n"
      "zip2 v19.8h, v17.8h, v16.8h\n"
      "zip2 v18.8h, v25.8h, v18.8h\n"
      "prfm pldl1keep, [x24, #0x70]\n"
      "prfm pldl1keep, [x23, #0x70]\n"
      "zip2 v17.8h, v22.8h, v21.8h\n"
      "add v2.8h, v2.8h, v19.8h\n"
      "prfm pldl1keep, [x22, #0x70]\n"
      "prfm pldl1keep, [x21, #0x70]\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "zip2 v22.8h, v31.8h, v27.8h\n"
      "str q20, [%x[out_ptr], #0x0]\n"
      "zip2 v21.8h, v29.8h, v24.8h\n"
      "zip2 v20.8h, v30.8h, v26.8h\n"
      "str q19, [%x[out_ptr], #0x10]\n"
      "zip2 v19.8h, v28.8h, v23.8h\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "str q16, [%x[out_ptr], #0x20]\n"
      "zip2 v16.8h, v18.8h, v17.8h\n"
      "zip1 v18.8h, v22.8h, v21.8h\n"
      "str q16, [%x[out_ptr], #0x30]\n"
      "zip1 v17.8h, v20.8h, v19.8h\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "str q16, [%x[out_ptr], #0x40]\n"
      "zip2 v16.8h, v18.8h, v17.8h\n"
      "zip2 v18.8h, v22.8h, v21.8h\n"
      "str q16, [%x[out_ptr], #0x50]\n"
      "zip2 v17.8h, v20.8h, v19.8h\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "str q16, [%x[out_ptr], #0x60]\n"
      "zip2 v16.8h, v18.8h, v17.8h\n"
      "str q16, [%x[out_ptr], #0x70]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x80\n"
      "bge 3b\n"
      "5:"  // Main loop skip
      "cbz %x[width], 10f\n"
      "tbz %x[width], #2, 7f\n"
      "ldr d31, [x28], #0x8\n"
      "ldr d30, [x27], #0x8\n"
      "ldr d29, [x26], #0x8\n"
      "ldr d28, [x25], #0x8\n"
      "ldr d27, [x24], #0x8\n"
      "ldr d26, [x23], #0x8\n"
      "ldr d24, [x22], #0x8\n"
      "ldr d23, [x21], #0x8\n"
      "tbz %x[width], #1, 6f\n"
      "ld1 { v31.s }[2], [x28], #0x4\n"
      "ld1 { v30.s }[2], [x27], #0x4\n"
      "mov x20, #0x6\n"
      "ld1 { v29.s }[2], [x26], #0x4\n"
      "ld1 { v28.s }[2], [x25], #0x4\n"
      "ld1 { v27.s }[2], [x24], #0x4\n"
      "ld1 { v26.s }[2], [x23], #0x4\n"
      "ld1 { v24.s }[2], [x22], #0x4\n"
      "ld1 { v23.s }[2], [x21], #0x4\n"
      "tbz %x[width], #0, 9f\n"
      "ld1 { v31.h }[6], [x28]\n"
      "ld1 { v30.h }[6], [x27]\n"
      "mov x20, #0x7\n"
      "ld1 { v29.h }[6], [x26]\n"
      "ld1 { v28.h }[6], [x25]\n"
      "ld1 { v27.h }[6], [x24]\n"
      "ld1 { v26.h }[6], [x23]\n"
      "ld1 { v24.h }[6], [x22]\n"
      "ld1 { v23.h }[6], [x21]\n"
      "b 9f\n"
      "6:"  // odd_loads_1_4
      "mov x20, #0x4\n"
      "tbz %x[width], #0, 9f\n"
      "ld1 { v31.h }[4], [x28]\n"
      "ld1 { v30.h }[4], [x27]\n"
      "mov x20, #0x5\n"
      "ld1 { v29.h }[4], [x26]\n"
      "ld1 { v28.h }[4], [x25]\n"
      "ld1 { v27.h }[4], [x24]\n"
      "ld1 { v26.h }[4], [x23]\n"
      "ld1 { v24.h }[4], [x22]\n"
      "ld1 { v23.h }[4], [x21]\n"
      "b 9f\n"
      "7:"  // odd_loads_2_0
      "tbz %x[width], #1, 8f\n"
      "ldr s31, [x28], #0x4\n"
      "ldr s30, [x27], #0x4\n"
      "mov x20, #0x2\n"
      "ldr s29, [x26], #0x4\n"
      "ldr s28, [x25], #0x4\n"
      "ldr s27, [x24], #0x4\n"
      "ldr s26, [x23], #0x4\n"
      "ldr s24, [x22], #0x4\n"
      "ldr s23, [x21], #0x4\n"
      "tbz %x[width], #0, 9f\n"
      "ld1 { v31.h }[2], [x28]\n"
      "ld1 { v30.h }[2], [x27]\n"
      "mov x20, #0x3\n"
      "ld1 { v29.h }[2], [x26]\n"
      "ld1 { v28.h }[2], [x25]\n"
      "ld1 { v27.h }[2], [x24]\n"
      "ld1 { v26.h }[2], [x23]\n"
      "ld1 { v24.h }[2], [x22]\n"
      "ld1 { v23.h }[2], [x21]\n"
      "b 9f\n"
      "8:"  // odd_loads_1_0
      "ldr h31, [x28, #0x0]\n"
      "ldr h30, [x27, #0x0]\n"
      "mov x20, #0x1\n"
      "ldr h29, [x26, #0x0]\n"
      "ldr h28, [x25, #0x0]\n"
      "ldr h27, [x24, #0x0]\n"
      "ldr h26, [x23, #0x0]\n"
      "ldr h24, [x22, #0x0]\n"
      "ldr h23, [x21, #0x0]\n"
      "9:"  // Odd load end
      "zip1 v25.8h, v31.8h, v27.8h\n"
      "zip1 v18.8h, v29.8h, v24.8h\n"
      "subs x20, x20, #0x1\n"
      "zip1 v22.8h, v30.8h, v26.8h\n"
      "zip1 v21.8h, v28.8h, v23.8h\n"
      "zip1 v17.8h, v25.8h, v18.8h\n"
      "zip1 v16.8h, v22.8h, v21.8h\n"
      "zip1 v20.8h, v17.8h, v16.8h\n"
      "str q20, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v20.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v19.8h, v17.8h, v16.8h\n"
      "subs x20, x20, #0x1\n"
      "str q19, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v19.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v18.8h, v25.8h, v18.8h\n"
      "zip2 v17.8h, v22.8h, v21.8h\n"
      "subs x20, x20, #0x1\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "str q16, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v16.8h, v18.8h, v17.8h\n"
      "subs x20, x20, #0x1\n"
      "str q16, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v22.8h, v31.8h, v27.8h\n"
      "zip2 v21.8h, v29.8h, v24.8h\n"
      "subs x20, x20, #0x1\n"
      "zip2 v20.8h, v30.8h, v26.8h\n"
      "zip2 v19.8h, v28.8h, v23.8h\n"
      "zip1 v18.8h, v22.8h, v21.8h\n"
      "zip1 v17.8h, v20.8h, v19.8h\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "str q16, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v16.8h, v18.8h, v17.8h\n"
      "subs x20, x20, #0x1\n"
      "str q16, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "beq 10f\n"
      "zip2 v18.8h, v22.8h, v21.8h\n"
      "zip2 v17.8h, v20.8h, v19.8h\n"
      "zip1 v16.8h, v18.8h, v17.8h\n"
      "str q16, [%x[out_ptr], #0x0]\n"
      "add v2.8h, v2.8h, v16.8h\n"
      "add %x[out_ptr], %x[out_ptr], #0x10\n"
      "10:"  // Odds skip
      "uaddw v1.4s, v1.4s, v2.4h\n"
      "uaddw2 v0.4s, v0.4s, v2.8h\n"
      "str q1, [%x[out_ptr], #0x0]\n"
      "str q0, [%x[out_ptr], #0x10]\n"
      "add %x[out_ptr], %x[out_ptr], #0x20\n"
      : [out_ptr] "+&r" (out_ptr), [width] "+&r" (width)
      : [first] "r" (first), [height] "r" (height), [in] "r" (in), [row_offset] "r" (row_offset)
      : "cc", "memory", "v0", "v1", "v2", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28"
    );
}


#endif // __aarch64__
