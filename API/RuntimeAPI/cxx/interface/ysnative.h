#ifndef YSGUARD_YSNATIVE_H
#define YSGUARD_YSNATIVE_H

#include "native_types.h"

#ifdef __cplusplus
extern "C" {
#endif

extern const ysnative *ys_get_native(void);

extern ysnative g_ysnative;

#ifdef __cplusplus
}
#endif

#endif // YSGUARD_YSNATIVE_H