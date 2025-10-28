/** @file ysentry.c
 * 
 * @brief C interface for the C YumStudio API.
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#include <stdint.h>

#include "native_types.h"

ysnative g_ysnative = {};

const ysnative *ys_get_native(void) {
  return &g_ysnative;
}

/**
 * @brief This function is the entry point of each YumStudio C AND C++ APIs.
 * The C++ API is initialized after the C API.
 * Do not modify the source of these functions unless you need to modify how the C/C++ API works.
 * You also don't need to call these functions, and may not call them.
 */
extern void YumStudioModuleEntry(const ysnative *native) {
  g_ysnative = (*native);
}