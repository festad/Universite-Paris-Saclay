var canvas_width = 1000;
var canvas_height = 3300;

var font_type = 'Arial';
var font_height = 14;
var font_color = 'whilte';



function preload(){
  data = loadTable("Countries-BMI-Data.csv", "csv", "header");
}

function setup() {
  // put setup code here
  createCanvas(canvas_width, canvas_height);

  console.log(data.getRowCount() + " total rows in table");
  console.log(data.getColumnCount() + " total columns in table");

  countries = data.getColumn("Country");

  textFont(font_type);
  textSize(font_height);

}

function draw() {
  // put drawing code here
  background(0,0,0);

  text_y = font_height; // because the zero starts below the 
                        // title, so the font height
  text_x = 0;

  for(var i = countries.length - 1; i>=0; i--) {
    // no text
    fill(font_color);
    noStroke();
    text(countries[i], text_x, text_y);
    text_y = text_y + font_height;
  }

}
