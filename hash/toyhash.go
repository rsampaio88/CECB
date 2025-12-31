// ToyHash CLI (intentionally weak) — find a collision!
// Build: go build -o toyhash .
// Usage: ./toyhash "your input"
package main

import (
    "fmt"
    "os"
)

// Extremely weak 32-bit rolling hash (not cryptographic!).
func ToyHash(data []byte) uint32 {
    var h uint32 = 0x9747b28c
    for _, b := range data {
        h ^= uint32(b)
        h *= 0x45d9f3b
        h = (h << 13) | (h >> 19)
        h ^= 0x27100001
    }
    return h
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("usage: toyhash \"some input\"")
        return
    }
    in := []byte(os.Args[1])
    fmt.Printf("ToyHash=0x%08x\n", ToyHash(in))
}