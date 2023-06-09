package RegexQuery;

import java.io.Console;
import java.util.List;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;

import java.io.IOException;

public class QueryJava {
	public static void main(String[] args)
			throws IOException {
		if (args.length == 2) {
			String input = args[0];
			String regex = args[1];
			int length = input.length();
			Pattern pattern = null;
			boolean valid = false;
			boolean matched = false;
			double allTime = 0.0;
			try {
				pattern = Pattern.compile(regex);
				valid = true;
				Matcher matcher = pattern.matcher(input);
				long start = System.nanoTime();
				matched = matcher.matches();
				// matched = matcher.find();
				long end = System.nanoTime();
				allTime = (double)(end - start) / 1_000_000_000.0;
			} catch (Exception e) {
				valid = false;
				log("Exception compiling regex: " + e);
			}
			MatchResult matchResult = new MatchResult(valid, length, input, regex, matched, allTime);
			System.out.println(new Gson().toJson(matchResult));
		} else {
			System.out.println("Usage: query input regex");
			System.exit(-1);
		}
	}

	static void log(String msg) {
		System.err.println(msg);
	}
}

class MatchResult {
	private String input;
	private String regex;
	private String language = "java";
	private boolean valid;
	private int length;
	private boolean matched;
	private double time;
	
	

	public MatchResult(boolean valid, int length,
			String input, String regex, boolean matched, double time) {
		this.valid = valid;
		this.regex = regex;
		this.input = input;
		this.length = length;
		this.matched = matched;
		this.time = time;
	}
}
