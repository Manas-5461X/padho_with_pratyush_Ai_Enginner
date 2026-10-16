// Coding agent ki practice file. Isme bug daalo, phir `uv run main.py` chalao.
// main() har result ke saath expected answer bhi print karta hai,
// taaki output dekh ke turant pata chale kya toota hai.


#include <bits/stdc++.h>


#define ll long long


using namespace std;


ll sum_array(vector<ll> &a)
{
    // {2,3,3} 8
    ll total=accumulate(a.begin(),a.end(),0LL);
    // 0 int
    return total;
}
int add(int a, int b) {
    return a + b;
}

int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result = result * i;
    }
    return result;
}

bool isPrime(int n) {
    if (n < 2) {
        return false;
    }
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

int findMax(const vector<int>& nums) {
    int best = nums[0];
    for (int i = 1; i < (int)nums.size(); i++) {
        if (nums[i] > best) {
            best = nums[i];
        }
    }
    return best;
}

double average(const vector<int>& nums) {
    int sum = 0;
    for (int x : nums) {
        sum += x;
    }
    return (double)sum / nums.size();
}

string reverseString(const string& s) {
    string reversed = "";
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        reversed += s[i];
    }
    return reversed;
}

int countVowels(const string& s) {
    int count = 0;
    for (char c : s) {
        c = tolower(c);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
    }
    return count;
}

int main() {
    vector<int> marks = {72, 95, 60, 88, 45};
    vector<ll> a={1,2,3};
    cout<<"sum_array result is "<<sum_array(a)<<endl;

    cout << "add(2, 3)              = " << add(2, 3) << "     (expected 5)" << endl;
    cout << "factorial(5)           = " << factorial(5) << "   (expected 120)" << endl;
    cout << "isPrime(7)             = " << isPrime(-7) << "     (expected 1)" << endl;
    cout << "isPrime(10)            = " << isPrime(10) << "     (expected 0)" << endl;
    cout << "findMax(marks)         = " << findMax(marks) << "    (expected 95)" << endl;
    cout << "average(marks)         = " << average(marks) << "    (expected 72)" << endl;
    cout << "reverseString(hello)   = " << reverseString("hello") << " (expected olleh)" << endl;
    cout << "countVowels(Education) = " << countVowels("Education") << "     (expected 5)" << endl;
    return 0;
}
