#include <iostream>
#include <string>
#include <regex>
#include "json.hpp"

using json = nlohmann::json;


int main(int argc, char* argv[])
{
    if (argc != 3) {
        std::cerr << "Usage: query-cpp input regex" << std::endl;
    }
    std::string input = argv[1];
    std::string regex = argv[2];
    
    json matchResult;
    matchResult["language"] = "cpp";
    matchResult["input"] = input;
    matchResult["regex"] = regex;
    matchResult["length"] = input.length();
    matchResult["valid"] = false;
    matchResult["matched"] = false;
    matchResult["time"] = 0.0;
    
    try {
        matchResult["valid"] = true;
        const std::regex pattern(regex);
        clock_t start = clock();
        matchResult["matched"] = std::regex_match(input, pattern);
        clock_t final = clock();
        matchResult["time"] = (float)(final - start) / CLOCKS_PER_SEC;
    } catch (...) {
        matchResult["valid"] = false;
    }
    
    std::cout << matchResult << std::endl;
}