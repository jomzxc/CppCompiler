## Valid Samples
```c
int add(int a, int b) { return a + b; }
```
```c
int main() { int x; x = 10; return x; }
```
```c
float pi = 3.14f;
```
```c
void check(int num) { if (num > 0) { return; } }
```
```c
int sum() {
    int total = 0;
    for (int i = 0; i < 5; i = i + 1) {
        total = total + i;
    }
    return total;
}
```
```c
int decrement(int n) {
    while (n > 0) {
        n = n - 1;
    }
    return n;
}
```
```c
int process() { int a = 5; int b = 10; return a * b; }
```
```c
bool compare(int x, float y) { return x > y; }
```
```c
int main() {
    int count = 0;
    for (int j = 0; j < 3; j = j + 1) {
        if (j > 1) { count = count + 1; }
    }
    return count;
}
```
```c
int main() {
    int a;
    a = 10;
    if (a > 5) {
        int b = 20;
        return b;
    }
    return 0;
}
```
```c
int main() {
    for (int i = 0; i < 2; i = i + 1) {
        int local = i * 2;
    }
    return 0;
}
```
```c
int main() { int x = 10; int y = x / 2; return y; }
```
```c
int main() { int a = 5; int b = a * (3 + 2); return b; }
```
```c
bool check_range(int val) { return val > 0 && val < 10; }
```
```c
int main() { int x = 5; bool result = (x == 5); return result; }
```
```c
int main() { int a = 10; int b = 5; bool res = (a != b); return res; }
```
```c
int main() { char c = 65; return c; }
```
```c
int main() { bool flag = true; if (flag) { return 5; } return 0; }
```
```c
void do_nothing() { }
```
```c
int main() { int a = 5; a = a + 1; return a; }
```
```c
int main() { int x = -5; return x; }
```
```c
int main() { return 1 + 2 * 3 - 4 / 2; }
```
```c
bool logical_op(bool a, bool b) { return a && !b; }
```
```c
int main() { int a = 5; return (a > 3) && (a < 10); }
```
```c
int main() {
    int x = 0;
    while (x < 3) {
        x = x + 1;
        int inner = x * 2;
    }
    return x;
}
```
```c
int main() {
    for (int i = 0; i < 2; i = i + 1) {
        if (i > 0) { return 1; }
    }
    return 0;
}
```
```c
int identity(int k) { return k; }
```
```c
int main() { int val = identity(10); return val; }
```
---
## Error Cases
```c
void main() { return 0; }
```
```c
int func() { int a = 10; return; }
```
```c
int main(int argc) { return 0; }
```
```c
int main() { int x = 5; int x = 10; return x; }
```
```c
int main() { return unknown_var; }
```
```c
int main() { int a = 5; return a + true; }
```
```c
void setValue(int val) { x = val; }
```

