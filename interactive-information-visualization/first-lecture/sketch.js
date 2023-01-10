// Canvas dimensions
var canvas_width = 1000;
var canvas_height = 4600; // I can make it bigger now

// Font settings
var font_type = 'Arial';
var font_height = 14;
var font_color = 'whilte';

// Spacings:
var line_spacing = 10;
var space_name_line = 10;

// Margins
var left_margin = 50; 
var right_margin = 50;
var top_margin = 20;
var bottom_margin = 20;

// To adjust the text on the right
var longest_name_length = 0;

// Minimum and maximum values of BMI
// to draw tickmaps
var min_bmi = -1;
var max_bmi = -1;


// var space_name


function getLongestNameLength(names){
  var max = -1;
  for (var i = 0; i < names.length; i++) {
    current = textWidth(names[i]);
    if (current > max)
      max = current;
  }
  return max;
}

function preload(){
  data = loadTable("Countries-BMI-Data.csv", "csv", "header");
}

function setup() {
  // put setup code here
  createCanvas(canvas_width, canvas_height);

  // console.log(data.getRowCount() + " total rows in table");
  // console.log(data.getColumnCount() + " total columns in table");

  countries = data.getColumn("Country");
  // console.log("Countries length: " + countries.length);

  // Setting the font
  textFont(font_type);
  textSize(font_height);

  // Needed to align right
  longest_name_length = getLongestNameLength(countries);

  // Getting values to put the tickmaps
  var female_bmi = data.getColumn("Female mean BMI (kg/m2)").map(Number);
  var male_bmi   = data.getColumn("Male mean BMI (kg/m2)").map(Number);

  // Min and max values for tickmaps
  min_bmi = min(min(female_bmi), min(male_bmi));
  max_bmi = max(max(female_bmi), max(male_bmi));



}

function draw() {
  // put drawing code here
  background(0,0,0);

  // text_y = font_height; // because the zero starts below the 
                        // title, so the font height

  // text_x = 0; // left align

  // Grid lines position
  line_x_left = left_margin + longest_name_length + space_name_line; // | [left_margin] <longest_name..> [space_name_line] ------
  line_x_right = canvas_width - right_margin;
  line_y = font_height/2 + top_margin; // only the first one,
                                       // the line is at half the height of the text
  vertical_line_y_top = top_margin;
  vertical_line_y_bottom = top_margin + (font_height+line_spacing) * countries.length; // + font_height;

  text_y = font_height + top_margin;

  for(var i = countries.length-1; i >= 0; i--) {
    fill(font_color);
    noStroke();

    // Grid
    stroke(font_color);
    line(line_x_left,  line_y,
         line_x_right, line_y);

    // Text
    text_x = left_margin + longest_name_length - textWidth(countries[i]);
    textAlign(LEFT);
    text(countries[i], text_x, text_y);

    // Updating values for the next iteration
    text_y += font_height + line_spacing;
    line_y = text_y - font_height/2;
  }

  // Draw vertical lines
  var round_min = floor(min_bmi);
  var round_max = floor(max_bmi);
  for(var i = round_min; i <= round_max; i++) {
    var vertical_line_x = map(i, round_min,   round_max, 
                              line_x_left, line_x_right);
    stroke(font_color);
    line(vertical_line_x, vertical_line_y_top, 
         vertical_line_x, vertical_line_y_bottom);

    // Draw tickmaps
    var scale = 0.3;
    fill(font_color);
    noStroke();
    textAlign(CENTER); // The ascissa will be at the center of the text,
    // textAlign(RIGHT); // <vertical_line_x> will be at the rightmost letter of the text;
    text(i, vertical_line_x, vertical_line_y_top - font_height*scale);
  }

  // ADD TICKMAPS AND LABELS
}
