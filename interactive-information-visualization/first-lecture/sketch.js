// Canvas dimensions
var canvas_width = 1000;
var canvas_height = 4600; // I can make it bigger now

// Font settings
var font_type = 'Arial';
var font_height = 14;
var font_color = 'white';
var font_weight = 0.5;

// Spacings:
var line_spacing = 10;
var space_name_line = 10;

// BMI values F and M
var female_bmi = [-1];
var male_bmi = [-1];

// BMI points appearence
var bmi_color_female;
var bmi_color_male;
var bmi_point_weight = 10;
var bmi_line_weight = 5;

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

// Useful to map the x values of lines and points
var round_min = -1;
var round_max = -1;

// grid appearence
var line_weight = 2;
var line_color = "white";


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

// c1, c2 -> color of x1 and color of x2
function setGradient(x1, x2, y, c1, c2, weight) {
  var min_x = min(x1,x2);
  var max_x = max(x1,x2);
  // Draws a sequence of points between the given two
  for (let i = min_x; i <= max_x; i++) {
    var inter = map(i, x1, x2, 0, 1);
    var c = lerpColor(c1,c2,inter);
    stroke(c);
    strokeWeight(weight);
    point(i,y);
  }
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
  female_bmi = data.getColumn("Female mean BMI (kg/m2)").map(Number);
  male_bmi   = data.getColumn("Male mean BMI (kg/m2)").map(Number);

  // Min and max values for tickmaps
  min_bmi = min(min(female_bmi), min(male_bmi));
  max_bmi = max(max(female_bmi), max(male_bmi));

  // Useful to map the x values of lines and points
  round_min = floor(min_bmi);
  round_max = ceil(max_bmi);


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
    // Grid
    stroke(line_color);
    strokeWeight(line_weight);
    // noStroke();
    line(line_x_left,  line_y,
         line_x_right, line_y);

    // Text
    fill(font_color);
    stroke(font_color);
    // noStroke();
    strokeWeight(font_weight);
    text_x = left_margin + longest_name_length - textWidth(countries[i]);
    textAlign(LEFT);
    text(countries[i], text_x, text_y);

    // Drawing points (BMI female and BMI male per country)
    strokeWeight(bmi_point_weight);
    // the colors are set later
    var current_female_bmi = female_bmi[i];
    var current_male_bmi = male_bmi[i];

    bmi_female_x = map(current_female_bmi, round_min, round_max, 
                                           line_x_left, line_x_right);
    
    bmi_male_x = map(current_male_bmi, round_min, round_max,
                                       line_x_left, line_x_right);

    bmi_color_female = color(255,0,232); // pink
    bmi_color_male   = color(0,185,255); // blue

    // female
    stroke(bmi_color_female);
    point(bmi_female_x, line_y);
    //male
    stroke(bmi_color_male);
    point(bmi_male_x, line_y);

    // Draw the colored line between points
    setGradient(bmi_female_x, bmi_male_x, line_y, bmi_color_female, bmi_color_male, bmi_line_weight);

    // Updating values for the next iteration
    text_y += font_height + line_spacing;
    line_y = text_y - font_height/2;
  }

  // Draw vertical lines
  for(var i = round_min; i <= round_max; i++) {
    stroke(line_color);
    strokeWeight(line_weight);
    var vertical_line_x = map(i, round_min,   round_max, 
                              line_x_left, line_x_right);

    line(vertical_line_x, vertical_line_y_top, 
         vertical_line_x, vertical_line_y_bottom);

    // Draw tickmaps
    stroke(font_color);
    strokeWeight(font_weight);
    var scale = 0.3;
    textAlign(CENTER); // The ascissa will be at the center of the text,
    // textAlign(RIGHT); // <vertical_line_x> will be at the rightmost letter of the text;
    text(i, vertical_line_x, vertical_line_y_top - font_height*scale);
  }
}
