package fn

import (
	"unsafe"
)

// true 返回 1，false 返回 0
// 相比于 if，可以减少编译后的 branch
func bool2int(x bool) int {
	return int(*(*uint8)(unsafe.Pointer(&x)))
}
