#ifndef __INC_TYPES_H
#define __INC_TYPES_H
#include "types.h"
#endif
#ifndef __INC_STRUTILS_H
#define __INC_STRUTILS_H
#include "strutils.h"
#endif

#ifdef __TEST__
#define __TEST_STRUTILS_FUNC__ test_strutils

inline int test_strutils() {
	signed char str[11] =  {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\0'};
	reverse_string_nbytes(str, 10);
}

#endif