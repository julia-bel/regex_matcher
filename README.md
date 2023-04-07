# Regex Matcher
Matching regular expressions with words or groups of pumping words in Java, Python, Javascript, C++, Go, Rust and measuring time consuming.

## Installing
1. Install packages
```
sudo apt-get install make default-jdk maven nodejs cargo golang-go python3-pip g++
```
2. Set the environment variable `REGEX_MATCHER_ROOT={path}/regex_matcher`
3. Configure files
```
# go
cd $REGEX_MATCHER_ROOT/src/go
make

# java
cd $REGEX_MATCHER_ROOT/src/java
mvn clean compile; mvn clean package

# rust
cd $REGEX_MATCHER_ROOT/src/rust
make

# c++
cd $REGEX_MATCHER_ROOT/src/cpp
make
```
3. Install requirements `pip install -r requirements.txt`

## Matching
```
python3 main.py filename.json
```

filename.json
```
{
    'regex': str, (target_file regex)
    'word': str,  (optional, input to match)
    'attack_group': Dict[str, Any], (optional, dictionary of the format
        {
            'prefix': str,
            'pump': str,
            'suffix': str,
            'steps': List[int], ([start, end, step], interval: [start, end))
        })
    'languages': List[str], (optional, languages to use, None means all)
    'target_file': str, (optional, file to save matching results)
    'visual_file': str, (optional, file to save visualization results)
    'encoding': str, (optional, global encoding, defaults to 'utf-8')
}
```

## Example
```
python3 main.py test/test.json
```
<p align="center">
    <img src="test/visual.png"/>
</p>