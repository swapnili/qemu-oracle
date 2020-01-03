/*
 * MUSER Interface for Multi-Process QEMU
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

#ifndef REMOTE_MUSER_H
#define REMOTE_MUSER_H

#include "qemu/osdep.h"
#include "qemu-common.h"
#include "hw/pci/pci.h"

#include <muser/muser.h>

// This structure is indexed by id for now
typedef struct MUserDevices {
    PCIDevice *pci_dev;
    char *uuid;
    lm_dev_info_t *dev_info;
} MUserDevices;

typedef struct {
    void *opaque[LM_DEV_NUM_REGS];
    MemoryRegionOps *bar_access[PCI_NUM_REGIONS];
} muser_pod_t;

PCIDevice *get_mdev_by_id(unsigned int id);

ssize_t bar0_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);
ssize_t bar1_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);
ssize_t bar2_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);
ssize_t bar3_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);
ssize_t bar4_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);
ssize_t bar5_access(void *pvt, char * const buf, size_t count, loff_t offset,
                    const bool is_write);

void handle_region_notice(int fd, void *pvt, dma_addr_t dma_addr, size_t size,
                          off_t offset, bool is_add);

#endif
