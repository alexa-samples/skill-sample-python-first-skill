## Introduction
In this module, you will build Cake Walk, a simple skill that asks the user for their birthday, remembers it, tells them how many days until their next birthday, and wishes them Happy Birthday on their birthday.
* asks the user for their birthday
* remembers it
* tells them how many days until their next birthday
* wishes them Happy Birthday on their birthday
In “Why develop skills with Alexa?” You saw what happens when a user interacts with a simple skill called “Hello World”. In the video below, let’s take a look at how users will interact with Cake Walk once you’ve built it:

As you can see the skill is simple to use yet a bit complex to build. The burden is on us, the skill builder, to make the interaction simple and natural. One way to make it as natural as possible is to mimic human conversational patterns. Humans have memory so your skill should too. It would be frustrating if your best friend always had to ask your name (which may be a sign that they really aren’t your best friend at all). While you could build cake walk in a day, because of its complexity you’ll build cake walk over four modules in this course.

Once you’ve completed this course; you’ll have built a skill that is useful, simple, and sticky. Useful skills provide value to users. For this skill Cake Walk is fun and useful to users by celebrating their birthday with a count down. Cake Walk is also a great example of a sticky skill, which retains the user’s interest and inspires them to keep coming back. Cake Walk encourages our user to keep checking in until their special day.  Let’s get started!

### About this module
If this is your first time building an Alexa skill, we recommend completing this module and the next three, which walk you through all the necessary steps.
Don’t worry if you get stuck along the way or if your code breaks. At the end of each module, the complete working code solution is provided for you under the **Code** heading.
If you’re already up to speed on the fundamentals of Alexa skill building and want to make your skill more conversational, please take a look at the  [conversational design course](http://alexa.design/cdw) .

### Features covered
* Utterances
* Intents
* Slots
* Dialog management
* Memory and persistence
* User profile settings

## Step 1: Log in
To get started, log into the  [Alexa developer console](https://developer.amazon.com/alexa/console/ask)  with your Amazon Developer account. If you do not have an account,  [click here](https://www.amazon.com/ap/register?clientContext=131-0331464-9465436&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&siteState=clientContext%3D142-6935021-1894360%2CsourceUrl%3Dhttps%253A%252F%252Fdeveloper.amazon.com%252Falexa%2Csignature%3Doyixlki7Yxz8bRUtt4vGJ4EugQ8j3D&marketPlaceId=ATVPDKIKX0DER&language=en_US&pageId=amzn_developer_portal&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Falexa&prevRID=HSRBQ1KHA4E5D1PBHPPP&openid.assoc_handle=mas_dev_portal&openid.mode=checkid_setup&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0)  to create one.


## Step 2: Create your skill

**a.** Click **Create Skill** on the right-hand side of the console. A new page displays.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-2a.png)


**b.** In the **Skill name** field, enter **Cake Walk**.

**c.** Leave the **Default language** set to **English (US)**.

**d.** You are building a custom skill. Under **Choose a model to add to your skill**, select **Custom**.

![](http://alexa-github.s3.amazonaws.com/skill-name-custom.png)

> **Skills have a front end and backend. The front end is where you map utterances (what the user says) into an intent (the desired action). You must decide how to handle the user’s intent in the backend. Host the skill yourself using an    function or HTTPS endpoint, or choose Alexa to host the skill for you. There are limits to the AWS Free Tier, so if your skill goes viral, you may want to move to the self-hosted option. For this course, choose Alexa-Hosted (Python).**

**e.** Under **Choose a method to host your skill’s backend resources**, select **Alexa-Hosted (Python)**.

![](http://alexa-github.s3.amazonaws.com/alexa-hosted-python.png)

**f.** At the top of the page, click **Create skill**.

![](http://alexa-github.s3.amazonaws.com/create-skill-button.png)

> **It takes a few moments for AWS to provision resources for your skill. When this process completes, move to the next section.**

>![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-2f-2.png)

> **Note: When you exit and return to the Alexa developer console, find your skill on the Skills tab, in the Alexa Skills list. Click Edit to continue working on your skill.**

> ![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-2f-3.png)

## Step 3: Greet the user
The first thing a user will want to do with the skill is open it. The intent of opening the skill is built into the experience, so you don’t need to define this intent in your front end.

However, you need to respond to the intent in your backend. In this step, you will update your backend code to greet the user when they open the skill.

**a.** Open the Cake Walk skill in the Alexa developer console. Click the Code tab. The code editor opens the lambda_function.py file.

![](http://alexa-github.s3.amazonaws.com/python-code-tab.png)

_To define how your skill responds to a JSON request, you will define a handler for each intent._

There are two pieces to a handler:
* **can_handle()** function
* **handle()** function
The **can_handle()** function is where you define what requests the handler responds to. The **handle()** function returns a response to the user.
If your skill receives a request, the **can_handle()** function within each handler determines whether or not that handler can service the request.
In this case, the user wants to launch the skill, which is a **LaunchRequest**. Therefore, the **can_handle()** function within the **LaunchRequestHandler** will let the SDK know it can fulfill the request. In computer terms, the **can_handle** returns _true_ to confirm it can do the work.

> **Tip:** In the code editor, search for text by pressing **CTRL+F** (**Command+F** on a Mac). A search window opens. This is helpful for searching for pieces of code within the editor.
>
What should happen when a user launches the Cake Walk skill? In this case, you want the skill to simply confirm that the user opened it by saying, "Hello! Welcome to Cake Walk. That was a piece of cake! Bye!"
Within the **LaunchRequestHandler** object, find the **handle()** function. This function uses the **responseBuilder** function to compose and return the response to the user.

Within the **handle()** function, find the line that begins **speak_output =**. This variable contains the string of words the skill should say back to the user when they launch the skill. Let’s change what it says to make sense for this skill.

**b.** Within the **LaunchRequestHandler** object, find the **handle()** function, and the line that begins **speak_output =**. Replace that line with the following:

```python
speak_output = "Hello! Welcome to cake walk. That was a piece of cake! Bye!"
```

> **If you are not familiar with programming, a string is encapsulated in single or double quotation marks. To change a string’s text, replace the text within the quotation marks.**
>
> **When you replace existing text or add new text to the code, blank lines may be introduced just before or after the text. Blank lines will not impact the code, but you may remove them.**
>
> **You may also notice your lines of code are not indented the same as code snippets in this course. This will also not impact the code, but you can use the TAB key to indent code if you would like.**

Within the **LaunchRequestHandler**, on the line under the speech text you just replaced, look for **handlerInput.responseBuilder**. This piece of the SDK will help build the response to the user.

On the next line, look for **.speak(speak_output)**. Note the **speak_output** variable, which you defined earlier. Calling the **.speak()** function tells **responseBuilder** to speak the value of **speak_output** to the user.

Next, look for the **.ask()** function within **responseBuilder**. (Be sure you are looking in the **LaunchRequestHandler**, within the **handle()** function.)
If the skill was supposed to listen for the user’s response, you would use this. In this case, you want the skill to speak and then exit. Therefore, let’s omit this line of code for now.

**c.** Within the **LaunchRequestHandler**, in the **handle()** function, find the line that begins **.ask()**. Add a **#** at the beginning of the line. This turns the line into a comment, meaning the line is ignored when the code runs.

**d.** Next, look for **.response** just below the line you commented out in the **LaunchRequestHandler**. This converts the **responseBuilder’s** work into the response that the skill will return. Remember the line that started with return? Think of it like hitting the Send button—it sends the response.

Your **LaunchRequestHandler** should now look like:

```python
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! Welcome to cake walk. That was a piece of cake! Bye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .response
        )
```
You have built the code that will handle a LaunchRequest for this skill. Before doing anything else, save your changes and deploy the code.

**e.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-3-save.png)

**f.** Click **Deploy**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-3-deploy.png)

## Step 4: Test your skill
Now it is time to test the skill. Start by activating the test simulator.

**a.** Click the **Test** tab. The test simulator opens.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-4-1.jpg)

An alert may appear requesting to use your computer’s microphone. Click **Allow** to enable testing the skill with your voice, just like if you were talking to an Alexa-enabled device.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-4-2.png)

**b.** From the drop-down menu at the top left of the page, select **Development**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-4-3.png)

# Testing inside the developer console
There are two ways to test your skill in the console. With the first method, type what the user would say into the box at the top left. Be precise—spelling matters! Alternately, speak to the skill by clicking and holding the microphone icon and speaking.

So far, the skill has one intent: **LaunchRequest**. This function responds to the user when they ask Alexa to open or launch the skill. The user will say, “Alexa, open Cake Walk.” Cake Walk is the name of your skill and was automatically set as the invocation name for the skill. You can change the invocation name, but let’s leave it as is for this exercise.

**c.** Test the skill. Type **open Cake Walk** (not case sensitive) into the box at the top left and press **ENTER**, or click and hold the microphone icon and say, “**Open Cake Walk**.”

> **When testing your skill in the Alexa developer console, you don’t need to provide the wake word (usually “Alexa”). Typing or saying, “Open Cake Walk” is fine. When testing on an Alexa-enabled device, you need the wake word: “Alexa, open Cake Walk.”**

## Wrap-up
When you open the skill, does it say, "Hello! Welcome to Cake Walk. That was a piece of cake! Bye!"? If so, congratulations! You have laid the groundwork for the skill. You will be building new skills with compelling conversational voice experiences in no time.

There is still a lot to learn! In the next section, you will expand the skill to make it more useful.

## Code
If your skill isn’t working or you’re getting some kind of syntax error, download the code sample in Python from the link below. Then, go to the Code tab in the Alexa developer console and copy and paste the code into the **lambda_function.py** file. Be sure to save and deploy the code before testing it.

 [Python Github Code Sample, Module 1: Build a Skill in 5 Minutes](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-1)

 [Continue to module 2](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-2)
