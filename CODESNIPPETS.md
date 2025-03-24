---
## Function Definitions
```
int add(int a, int b) { return a + b; }
```
```
int main() { int x; x = 10; return x; }
```
```
float pi = 3.14f;
```
```
void check(int num) { if (num > 0) { return; } }
```
```
int sum() {
    int total = 0;
    for (int i = 0; i < 5; i = i + 1) {
        total = total + i;
    }
    return total;
}
```
```
int decrement(int n) {
    while (n > 0) {
        n = n - 1;
    }
    return n;
}
```
```
int process() { int a = 5; int b = 10; return a * b; }
```
```
bool compare(int x, float y) { return x > y; }
```
```
int main() {
    int count = 0;
    for (int j = 0; j < 3; j = j + 1) {
        if (j > 1) { count = count + 1; }
    }
    return count;
}
```
---
## Semantic Errors
```
int main() { int y = 5; return y; }
```
```
int main() { int z = true; return z; }
```
```
double average(int a, float b) { return (a + b) / 2.0; }
```
```
char initial = 'A';
bool flag = false;
```
```
int main() { int a = 10; int b = a + 5; return b; }
```
```
float area(float radius) { return 3.14f * radius * radius; }
```
```
void print_value(int val) { return; }
```
```
int factorial(int n) {
    if (n <= 1) { return 1; }
    else { return n * factorial(n - 1); }
}
```
```
int main() {
    int i = 0;
    while (i < 10) { i = i + 1; }
    return i;
}
```
```
bool is_even(int num) { return (num % 2 == 0); }
```
```
int main() { int x = 5; x = 7; return x; }
```
---
## Block Scope Tests
```
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
```
int main() {
    for (int i = 0; i < 2; i = i + 1) {
        int local = i * 2;
    }
    return 0;
}
```
---
## Arithmetic and Logical Operations
```
int main() { int x = 10; int y = x / 2; return y; }
```
```
int main() { int a = 5; int b = a * (3 + 2); return b; }
```
```
bool check_range(int val) { return val > 0 && val < 10; }
```
```
int main() { int x = 5; bool result = (x == 5); return result; }
```
```
int main() { int a = 10; int b = 5; bool res = (a != b); return res; }
```
```
int main() { float f = 2.5f; double d = 3.7; return (int)d; }
```
```
int main() { double val = 10; float res = (float)val; return 0; }
```
```
int main() { char c = 65; return c; }
```
```
int main() { bool b = (bool)1; return b; }
```
```
int main() { int x = 10; if (x) { return 1; } else { return 0; } }
```
```
int main() { bool flag = true; if (flag) { return 5; } return 0; }
```
---
## Function and Control Flow
```
void do_nothing() { }
```
```
int main() { int a = 5; a = a + 1; return a; }
```
```
int main() { int x = -5; return x; }
```
```
int main() { return 1 + 2 * 3 - 4 / 2; }
```
```
bool logical_op(bool a, bool b) { return a && !b; }
```
```
int main() { int a = 5; return (a > 3) && (a < 10); }
```
```
int main() {
    int x = 0;
    while (x < 3) {
        x = x + 1;
        int inner = x * 2;
    }
    return x;
}
```
```
int main() {
    for (int i = 0; i < 2; i = i + 1) {
        if (i > 0) { return 1; }
    }
    return 0;
}
```
```
int identity(int k) { return k; }
```
```
int main() { int val = identity(10); return val; }
```
---
## Error Cases
```
int main() { return; }
```
```
void main() { return 0; }
```
```
int func() { int a = 10; return; }
```
```
int main(int argc) { return 0; }
```
```
int main() { int x = 5; int x = 10; return x; }
```
```
int main() { return unknown_var; }
```
```
int main() { int a = 5; return a + true; }
```
```
void setValue(int val) { int x = val; }
```
```
int main() { return 10 + 5 * (3 - 1) / 2; }
```