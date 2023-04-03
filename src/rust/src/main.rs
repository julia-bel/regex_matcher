use std::env;
use std::time::Instant;

extern crate serde_json;
use serde_json::json;

extern crate regex;
use regex::Regex;


fn main() {
    let args: Vec<String> = env::args().collect();
    let input = &args[1];
    let regex = &args[2];
    let pattern = "^".to_owned() + regex + "$";
    let mut result = json!({
        "input": &input,
        "regex": &regex,
        "language": "rust",
		"valid": false,
		"length": input.len(),
        "matched": false,
        "time": 0.0,
	});

    match Regex::new(&pattern) {
        Ok(re) => {
            result["valid"] = json!(true);
            let start = Instant::now();
            result["matched"] = json!(re.is_match(&input));
            result["time"] = json!(start.elapsed().as_secs_f64());
        }
        Err(_) => {}
    }
    println!("{}", result.to_string());
}