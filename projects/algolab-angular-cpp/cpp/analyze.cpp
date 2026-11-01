#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
  if (argc != 2) {std::cerr << "Usage: analyze <csv-file>\n"; return 2;}
  std::ifstream file(argv[1]);
  if (!file) {std::cerr << "Cannot read input file\n"; return 2;}
  std::vector<double> values;
  std::string line, cell;
  while (std::getline(file,line)) {
    std::istringstream row(line);
    while(std::getline(row,cell,',')) {
      if (cell.find_first_not_of(" \t\r") == std::string::npos) continue;
      std::istringstream parser(cell); double n; char extra;
      if (!(parser >> n) || (parser >> extra) || !std::isfinite(n)) {std::cerr << "Invalid number in CSV\n";return 2;}
      if (values.size() >= 1000) {std::cerr << "Maximum 1000 values\n";return 2;}
      values.push_back(n);
    }
  }
  if(values.empty()) {std::cerr << "No numbers found\n";return 2;}
  std::sort(values.begin(),values.end());
  double sum=0; for(double v:values)sum+=v;
  const auto count=values.size();
  const double median=count%2 ? values[count/2] : (values[count/2-1]+values[count/2])/2;
  std::cout << std::setprecision(10) << "{\"count\":" << count << ",\"min\":" << values.front() << ",\"max\":" << values.back() << ",\"mean\":" << sum/count << ",\"median\":" << median << "}\n";
}