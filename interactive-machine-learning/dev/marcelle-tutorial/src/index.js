import '@marcellejs/core/dist/marcelle.css';
import * as marcelle from '@marcellejs/core';

// const most = require('most');

const input = marcelle.webcam();
const featureExtractor = marcelle.mobileNet();

const label = marcelle.textInput();
label.title = 'New facial gesture';

const capture = marcelle.button('Click to record an instance');
capture.title = 'Capture instances to the training set';
capture.innerHTML = "Hello World!";

// const $instances = capture.$click
//   .sample(input.$images)
//   .map(async (img) => ({
//     x: await featureExtractor.process(img),
//     y: label.$value.get(),
//     thumbnail: input.$thumbnails.get(),
//   }))
//   .awaitPromises();

const store = marcelle.dataStore('localStorage');
const trainingSet = marcelle.dataset('TrainingSet', store);

// $instances.subscribe(trainingSet.create);

const trainingSetBrowser = marcelle.datasetBrowser(trainingSet);
trainingSetBrowser.title = 'Training set';

const classifier = marcelle.mlpClassifier({ layers: [32, 32], epochs: 20 });
const trainingButton = marcelle.button('Train');
trainingButton.title = 'Train the classifier';  

trainingButton.$click.subscribe(() => {
  classifier.train(trainingSet);
});

const plotTraining = marcelle.trainingPlot(classifier);

const $predictions = input.$images
  .map(async (img) => {
    const features = await featureExtractor.process(img);
    return classifier.predict(features);
  })
  .awaitPromises();

const predViz = marcelle.confidencePlot($predictions);

// FACIAL GESTURES
const facial_gestures_ids = ['Call mom', 'Pain in the ass', 'I\'m hungry'];

// FACIAL GESTURES BUTTONS
const facial_gesture_btns = [];
facial_gestures_ids.forEach(id => {
  let btn = marcelle.button(id);
  btn.title = id;
  facial_gesture_btns.push(btn);
});

// DICTIONARY: <BUTTON|STREAM<Image>>
const facial_gesture_instances = {};
facial_gesture_btns.forEach((btn) => {
  facial_gesture_instances[btn.title] = btn.$click
  .sample(input.$images)
  .map(async (img) => ({  
    x: await featureExtractor.process(img),
    y: btn.title,
    thumbnail: input.$thumbnails.get(),
  }))
  .awaitPromises();
  // Subscribe to the new stream
  facial_gesture_instances[btn.title]
    .subscribe(trainingSet.create);
});



// KEEPING TRACK OF WHAT IS ON THE DASHBOARD
// let fg_ids_on_dashboard = facial_gestures_ids;
// let fg_btns_on_dashboard = facial_gesture_btns;


// const btn_facial_gestures$ = facial_gestures$
//   .map(fg => marcelle.button(fg));

// btn_facial_gestures$.forEach(btn => {
//   console.log('Inside foreach');
//   btn.$click.subscribe(() => {
//     console.log(btn.title);
//   });
// });

// ADDING NEW GESTURES (BUTTONS) TO THE DASHBOARD
const btn_new_facial_gesture = marcelle.button('New');
btn_new_facial_gesture.title = 'Add a new facial gesture'
btn_new_facial_gesture.$click.subscribe(() => {
  console.log('Adding new facial gesture');
  let name = label.$value.get();
  console.log(name);
  let btn = marcelle.button(name);
  btn.title = name;
  facial_gesture_btns.push(btn);
  // Add on the dashboard
  myDashboard.page('Data Management').sidebar(btn);
  // Refresh the dsashboard
  // myDashboard.refresh();
  // Create a new stream for the new button
  // inside the object facial_gesture_instances
  facial_gesture_instances[btn.title] = btn.$click
  .sample(input.$images)
  .map(async (img) => ({  
    x: await featureExtractor.process(img),
    y: btn.title,
    thumbnail: input.$thumbnails.get(),
  }))
  .awaitPromises();
  // Subscribe to the new stream
  facial_gesture_instances[btn.title].subscribe(trainingSet.create);

  console.log("After adding: facial_gesture_btns[]:");
  console.log(facial_gesture_btns);
});

const myDashboard = marcelle.dashboard({
  title: 'My First Tutorial',
  author: 'Myself',
});

myDashboard
  .page('Data Management')
  .sidebar(input, featureExtractor)
  .use([label, btn_new_facial_gesture], trainingSetBrowser, trainingButton)
  .use(plotTraining);


facial_gesture_btns.forEach(button => {
  myDashboard.page('Data Management').sidebar(button);
});

myDashboard.page('Direct Evaluation').sidebar(input).use(predViz);

// function updateEverything() {
//   console.log('Updating everything');
//   facial_gesture_btns.forEach(button => {
//     console.log(fg_btns_on_dashboard.includes(button));
//     if (!fg_btns_on_dashboard.includes(button)) {
//       // Add on the dashboard
//       console.log('Adding button');
//       myDashboard.page('Data Management').sidebar(button);
//       // Update the list of buttons on the dashboard
//       fg_btns_on_dashboard.push(button);
//       fg_ids_on_dashboard.push(button.title);
//       // Create a new stream for the new button
//       // inside the object facial_gesture_instances
//       // facial_gesture_instances[button.title] = button.$click
//       //   .sample(input.$images)
//       //   .map(async (img) => ({
//       //     x: await featureExtractor.process(img),
//       //     y: button.title,
//       //     thumbnail: input.$thumbnails.get(),
//       //   }))
//       //   .awaitPromises();
//       // Subscribe to the new stream
//       // facial_gesture_instances[button.title].subscribe(trainingSet.create);
//     }
//   })
//   console.log('Succesfully terminated updateEverything()');
// }

myDashboard.show();

// npx marcelle
// NeDB