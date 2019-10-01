# Cake Walk 

## Module 3: Add Memory To Your Skill

The files in this folder represent how Calk Walk should appear at the end of this module. If you're stuck you can compare your files with these to figure out where you went wrong. You can also use these files to skip head.

### Step-by-step Instructions

You can find the instructions here: [Adding memory to your skill](https://developer.amazon.com/alexa-skills-kit/courses/cake-walk-5)

Once you're ready you move on to [Module 4: Use the Settings API ](../module-4/README.md)

### Contents

*  [en-US.json](./en-US.json)
*  [index.js](./index.js)
*  [package.json](./package.json)
 
#### en-US.json 
---
This is your skill's interaction model. You can use this file to create your voice user interface. To use this file:

1. From the [alexa developer console](https://developer.amazon.com) click on the **Build** tab.
2. On the left hand side click on **JSON Editor**. 
3. Copy the contents of [en-US.json](./en-US.json) and paste it over the contents of the editor
4. Click **Save Model**
5. Click **Build Model**

#### index.js
---
This is your skill's backend code. It's the logic that handles the requests that are sent to your skill. To use this file:

1. From the [alexa developer console](https://developer.amazon.com) click on the **Code** tab.
2. Open the **index.js** file by selecting the tab or double-clicking on the file name on the right-hand side.
3. Copy the contents of [index.js](./index.js) and paste it over the data in your browser.
4. Click **Save**.
5. Click **Deploy**.

#### package.json
---
This file describes your project. It includes various meta data including the dependencies of your project. We are dependent on the [ASK SDK](https://ask-sdk-for-nodejs.readthedocs.io/en/latest/) which is automatically included when we created Alexa Hosted skill. We added a new dependency on the **ask-sdk-s3-persistence-adapter**, so we've updated in the code. To this this file:

1. From the [alexa developer console](https://developer.amazon.com) click on the **code** tab.
2. Open the **package.json** file by selecting the tab or double-clicking on the file name on the right-hand side.
3. Copy the contents of [package.json](./package.json) and paste it over the data in your browser.
4. Click **Save**.
5. Click **Deploy**.