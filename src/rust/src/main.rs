use std::env;
use std::time::Instant;

extern crate serde;
#[macro_use]
extern crate serde_json;

extern crate serde_derive;

extern crate regex;
use regex::Regex;

fn main() {
    let args: Vec<String> = env::args().collect();
    let input = &args[1];
    let regex = &args[2];
    let pattern = "^".to_owned() + regex + "$";
    let mut result: serde_json::Value = json!({
        "input": &input,
        "language": "rust",
		"regex": &regex,
		"length": input.len(),
        "valid": false,
        "matched": false,
        "time": 0,
	});

    match Regex::new(&pattern) {
        Ok(re) => {
            result["valid"] = json!(true);
            let start = Instant::now();
            result["matched"] = json!(re.is_match(&input));
            result["time"] = json!(start.elapsed().as_secs());
        }
        Err(error) => {}
    }
    println!("{}", result.to_string());
}