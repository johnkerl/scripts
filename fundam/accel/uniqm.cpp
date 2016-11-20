#include <iostream>
#include <set>
using namespace std;
int main() {
  set<string> lines_seen;
  string line;
  while (true) {
    getline(cin, line);
    if (line == "")
      break;
    if (lines_seen.count(line) == 0)
      cout << line << endl;
    lines_seen.insert(line);
  }
  return 0;
}
