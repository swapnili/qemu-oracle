/*
 * Integrate with muser framework
 *
 * Copyright 2020, Oracle and/or its affiliates.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "qemu/osdep.h"
#include "qemu-common.h"

#include "remote/muser.h"

static size_t bar_access_write(void *opaque, char * const buf, size_t count,
                               loff_t offset, MemoryRegionOps *ops)
{
    uint64_t val;
    uint8_t *ptr = (uint8_t *)&val;
    size_t i = 0;

    switch (count) {
        case 8:
            val = le64_to_cpu(*((uint64_t *)buf));
            break;
        case 4:
            val = le32_to_cpu(*((uint32_t *)buf));
            break;
        case 2:
            val = le16_to_cpu(*((uint16_t *)buf));
            break;
        case 1:
            val = *((uint8_t *)buf);
            break;
        default:
            assert(0);
    }

    for (i = 0; i < count; i++) {
        ops->write(opaque, (offset + i), ptr[i], 1);
    }

    return count;
}

static size_t bar_access_read(void *opaque, char * const buf, size_t count,
                              loff_t offset, MemoryRegionOps *ops)
{
    uint64_t val;
    uint8_t *ptr = (uint8_t *)&val;
    size_t i = 0;

    for (i = 0; i < count; i++) {
        ptr[i] = ops->read(opaque, (offset + i), 1);
    }

    switch (count) {
        case 8:
            *((uint64_t *)buf) = cpu_to_le64(val);
            break;
        case 4:
            *((uint32_t *)buf) = cpu_to_le32((uint32_t)val);
            break;
        case 2:
            *((uint16_t *)buf) = cpu_to_le16((uint16_t)val);
            break;
        case 1:
            *((uint8_t *)buf) = (uint8_t)val;
            break;
        default:
            assert(0);
    }

    return count;
}

static inline size_t bar_access(void *opaque, const bool is_write,
                                char * const buf, size_t count, loff_t offset,
                                MemoryRegionOps *ops)
{
    if (is_write) {
        return bar_access_write(opaque, buf, count, offset, ops);
    } else {
        return bar_access_read(opaque, buf, count, offset, ops);
    }

    return 0;
}

#define DEFINE_BAR_ACCESS(idx)                                          \
ssize_t bar##idx##_access(void *pvt, char * const buf, size_t count,    \
                               loff_t offset, const bool is_write)      \
{                                                                       \
    muser_pod_t *pod = (muser_pod_t *)pvt;                              \
                                                                        \
    return bar_access(pod->opaque[idx], is_write, buf, count, offset,   \
                      pod->bar_access[idx]);                            \
}                                                                       \

DEFINE_BAR_ACCESS(0);
DEFINE_BAR_ACCESS(1);
DEFINE_BAR_ACCESS(2);
DEFINE_BAR_ACCESS(3);
DEFINE_BAR_ACCESS(4);
DEFINE_BAR_ACCESS(5);
