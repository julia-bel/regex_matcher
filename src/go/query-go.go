package main

import (
    "fmt"
    "os"
    "encoding/json"
    "regexp"
    "time"
)

type MatchResult struct {
    Input string               `json:"input"`
    Regex string               `json:"regex"`
    Language string            `json:"language"`
    Valid bool                 `json:"valid"`
    Length int                 `json:"length"`
    Matched bool               `json:"matched"`
    Time float64               `json:"time"`
}

func myLog(str string) {
    fmt.Fprintln(os.Stderr, str)
}

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func main() {
    if len(os.Args) <= 1 {
        fmt.Printf("Usage: query-go input regex\n")
        os.Exit(1)
    }

    var matchResult MatchResult
    matchResult.Language = "go"
    matchResult.Input = os.Args[1]
    matchResult.Regex = os.Args[2]
    matchResult.Length = len(matchResult.Input)
    matchResult.Valid = false
    matchResult.Matched = false
    matchResult.Time = 0

    re, err := regexp.Compile("^" + matchResult.Regex + "$")
    if err == nil {
        matchResult.Valid = true
        start := time.Now()
        matchResult.Matched = re.Match([]byte(matchResult.Input))
        // matches := re.FindSubmatch([]byte(matchResult.Input))
        matchResult.Time = time.Since(start).Seconds()
    }

    str, _ := json.Marshal(matchResult)
    fmt.Println(string(str))
}
