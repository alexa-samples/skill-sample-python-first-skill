## Collecting slots turn-by-turn with auto-delegation
In the previous section, you built an Alexa skill that says, “Hello! Welcome to Cake Walk. That was a piece of cake! Bye!” In this section, you will make the skill more useful by having it ask the user for their birthday. When the user responds, the skill will understand and repeat the user’s birthday back to them.

To do this, you will need to use utterances, intents, and slots. You will also learn how to use dialog management to have your skill automatically ask follow-up questions to collect required information. For example, if the user says, “I was born July 12th,” dialog management will automatically ask the user what year they were born.

At the end of this module, your Cake Walk skill will be able to:
* **Ask** the user a question
* **Listen** for the answer
* **Respond** to the user

Use the  [Alexa developer console](https://developer.amazon.com/alexa/console/ask)  for this module. Log in to the console and open the Cake Walk skill.

## Step 1: Ask the user for their birthday
At the moment, the skill simply greets the user and exits. The welcome message helps set the context of the interaction—the user knows they are interacting with Cake Walk. Now you need to capture the user’s birthday to eventually calculate the number of days until the user’s next birthday. To do that, update the skill with programming logic that instructs Alexa to ask for the user’s birthday.

![](http://alexa-github.s3.amazonaws.com/python-code-tab.png)

**a.** In the developer console, click the **Code** tab.

Find the **LaunchRequestHandler**. Within the handler, the **speak_output** variable is passed to the **.speak()** function. In the next step, update the string to ask the user for their birthday.

**b.** Within the **LaunchRequestHandler**, in the **handle()** function, find the line that begins with **speak_output =**. Replace that line with the following:

```py
speak_output = "Hello! This is Cake walk. What is your birthday?"
```

Your `LaunchRequestHandler` should now look like:

```py
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! This is Cake walk. What is your birthday?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .response
        )
```

Now, remember that after Alexa responds, the skill exits. You need to tell Alexa to listen for the user to respond. To do that, you will use the **.ask()** function, which you previously commented out.

**c.** Within the **LaunchRequestHandler**, in the **handle()** function, remove the “#” before the **.ask()** function.

The **.ask()** function does two things:
* Tells the skill to wait for the user to reply, rather than simply exiting
* Allows you to specify a way to ask the question to the user again, if they don’t respond

> **A best practice is to make your reprompt text different from your initial speech text.**

The user may not have responded for a variety of reasons. The skill should pose the initial question again but do so in a natural way. The reprompt should provide more context to help the user provide an answer. Specify the reprompt text by creating a new variable named **reprompt_text**.

**d.** Within the **LaunchRequestHandler**, in the **handle()** function, find the line that begins **speak_output =**. Create a new line _below_ it by clicking at the end of the line and pressing **ENTER**.

**e.** Copy and paste the following code on the new line:
```py
reprompt_text = "I was born Nov. 6th, 2014. When are you born?"
```

Notice the reprompt gives an example of what Alexa expects the user to say by having Alexa provide her own birthday in the format she is looking for. Providing examples like this is a best practice.

> **Notice the numbers are spelled out in the reprompt text. You can use Speech Synthesis Markup Language (SSML) to have Alexa read "2014."**

Now you want the code to pass the `reprompt_text` variable to the **.ask()** function.

**f.** Within the **LaunchRequestHandler**, in the **handle()** function, replace **.ask(speak_output)** with **.ask(reprompt_text)**

Your `LaunchRequestHandler` should now look like:

```py
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! This is Cake walk. What is your birthday?"
        reprompt_text = "I was born Nov. 6th, 2015. When are you born?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
```

There is a potential complication with asking the user for their birthday. They might respond in many different ways. For example, the user might give only the month and day, or they might say something like, "Next Tuesday."
In this course, you won't handle all the different ways a user might respond, but we challenge you to account for them when you finish the course. Let's focus on a way to ensure that Alexa is able to collect the month, day, and year from the user.

Before moving on, save and deploy your updated code.

**g.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/3/building-a-skill-3-save.png)

**h.** Click **Deploy**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-4j.png)

> **Get into the habit of saving and deploying your changes regularly to ensure you don't lose anything. Save as you go!**  

The Cake Walk skill can now ask and listen, but it can't respond yet. You need to update our skill's front end before testing it. Specifically, you need to create an intent to interpret the user's response to the skill's question.

## Step 2: Use an intent and slots to capture information
Now make some adjustments to the skill's front end. Specifically, you need to create an intent that will interpret how the user responds to Alexa's question.
When you name an intent, think about what the intent is going to do. In this case, the intent is going to capture the user's birthday, so name it **CaptureBirthdayIntent**. Notice the words are not separated by spaces, and each new word begins with an uppercase letter.

**a.** Click the **Build** tab.

**b.** To the right of **Intents**, click **Add**. The Add Intent window opens.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2a.png)

**c.** Select **Create custom intent** and enter the following text for the name of the intent: **CaptureBirthdayIntent**

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2c.png)

**d.** Click **Create custom intent**. The intent is created.

> **Remember, an intent is an action to fulfill a user's request. An utterance is what invokes the intent. In response to the birthday question, a user might say - "I was born on November seventh, nineteen eighty three." You will add this utterance to the CaptureBirthdayIntent by typing it in exactly the way the user is expected to say it.**

**e.** In the **Sample Utterances** field, type the following, and then press **ENTER** or click the + icon: **I was born on November seventh nineteen eighty three**
Notice that the text does not include punctuation.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2e.png)

> **When finished, the Cake Walk skill will be able to capture any birthday.**

From this utterance, there are three key pieces of information to collect: month, day, and year. These are called slots. You need to let Alexa know which words are slots and what kind of slots they are.
Start with the month slot. In the utterance, you will replace the word representing the month (November) with the word **month** in curly brackets ({ }). This creates a slot called month. The utterance will then look like this: **I was born on {month} seventh nineteen eighty three**
There are two ways to create a slot. The first way is to select the word in the sample utterance where the slot should go and type the name of the slot in curly brackets (for example, **{month}**).
The second way is to select the word in the sample utterance and use the **Select an Existing Slot** dialog box when it appears. In the dialog box, click the field under **Create a new slot**, type the name of the slot without curly brackets (for example, **month**), and click **Add**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2e2.png)

**f.** In the utterance, use either method of creating a slot to create a slot called **month** over the word **November**.

**g.** Repeat this process for the other variable pieces of information (day and year).
Your utterance should now look like this: **I was born on {month} {day} {year}**
What if the user omits the words _I was born on_? Account for this by adding a second utterance with only the slots.

**h.** In the **Sample Utterances** field, type the following, and then press **ENTER** or click the + icon: **{month} {day} {year}**

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2h.png)

> **When entering a sample utterance, you may need to press ENTER twice for the utterance to be added. You can also click the + icon.**

Now, you should account for a few other potential slot combinations.

**i.** Enter each of the examples below as sample utterances. When you are finished, you should have six utterances.  
{month} {day}  
{month} {day} {year}  
{month} {year}  
I was born on {month} {day}  
I was born on {month} {day} {year}  
I was born in {month} {year}

You have let Alexa know what slots need to be collected (and covered some of the different patterns users might provide that information in). Now you need to define exactly what those slots are by assigning a slot type to each slot.

Scroll down the page to **Intent Slots**. This area displays the slots you have created.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2i.png)

Slots are assigned from the **Slot Type** drop-down menu to the right of each slot.

There are two types of slot types: custom and built-in. Wherever possible, use built-in slots. Alexa manages the definitions of built-in slots. These slots begin with **AMAZON** followed by what they define (for example, **AMAZON.Month**).

If an applicable built-in slot does not exist, create a custom slot and define the values it represents. For this course, you will only use built-in slots.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2i2.png)

**j.** To the right of the **month** slot, select **AMAZON.Month** from the **Slot Type** drop-down menu.

**k.** For the **day** slot, select **AMAZON.Ordinal** as the slot type.

**l.** For the **year** slot, select **AMAZON.FOUR_DIGIT_NUMBER** as the slot type.
![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2j.png)

You have created an intent to collect the user's birthday.

But what about a user who doesn't respond with all three slot values? For example, a user who responds, "In July." Let's take a look at solving that problem.

**m.** At the top of the page, click **Save Model**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2m.png)

## Step 3: Use dialog management
Slots can be required or optional. That is, if you need a given value from the user, you can designate a slot as required using dialog management. Marking a slot as required triggers Alexa to actively work to fill it. Start by making each of the slots required.

**a.** Click on “CaptureBirthdayIntent” on the left nav bar. In the **Intent Slots** section, to the right of the **month** slot, click **Edit Dialog**.

**b.** Under **Slot Filling**, toggle to make the slot required.

The **Alexa speech prompts** field appears. Here, you will enter text for Alexa to say if the user fails to provide a value for the **month** slot.

**c.** In the field, type **What month were you born in?** and then press **ENTER** or click the + icon.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-3c.png)

**d.** Repeat the process for the **day** and **year** slots.

Note: Return to the screen where you entered the sample utterances by clicking **CaptureBirthdayIntent** in the left-hand panel.

> Now that the slots are required, if a user responds, "July nineteen eighty two," Alexa recognizes that the month and year slots are filled, but the day slot is not.

>  Alexa will prompt the user for each unfilled slot. In this example, Alexa would ask, "What day were you born?"

One of the great things about dialog management is that the skill doesn't break or get confused if the user leaves out a piece of information or provides it out of the expected order. Instead, Alexa takes on the responsibility of collecting information designated as required to ensure a useful experience.

You have built an intent that listens for the user's answer to the birthday question. When the user responds, Alexa collects the user's birthday month, day, and year. This information will be sent to the skill's backend code in a JSON request.

Before moving on, notice the **HelloWorld** intent in the left-hand panel. That is a leftover from the starter template that you don't need.

**e.** Delete the **HelloWorldIntent** intent by clicking the trash can icon to the right of it. When prompted, click **Delete Intent**.

Be careful to delete **HelloWorldIntent** and _not_ **CaptureBirthdayIntent**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-3e.png)

> **You may notice other intents (such as AMAZON.HelpIntent) were automatically added to your skill. These are required for every skill and provide the user a means to cancel, stop, and get help. Do not remove these.**

**f.** At the top of the page, click **Save Model**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-2m.png)

**g.** Click **Build Model**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-3g.png)

When you click **Build Model**, your skill starts to build the training data that will help Alexa know how to map what the user says to your skill's intents. It may take a minute for the model to build.

At this point, your skill can ask and listen. Now, make it respond.

## Step 4: Define a new handler
To make the Cake Walk skill respond, you need to update the backend.

**a.** Click the **Code** tab.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-4a.png)

Remember modifying the **LaunchRequestHandler**? This time, you are going to build a new handler. This handler will acknowledge that the user provided their birthday and repeat the birthday back to the user.

If you look at the code, you will notice the **HelloWorldIntentHandler**. But you deleted the **HelloWorldIntent**, right? Not entirely. The intent is gone from the front end, but the backend handler is still there. You need a new handler, so make things easier and reuse this handler for a new one called **CaptureBirthdayIntentHandler**.

**b.** Find the line that starts **class HelloWorldIntentHandler**. On that line, rename **HelloWorldIntentHandler** to **CaptureBirthdayIntentHandler**

**c.** Within the **CaptureBirthdayIntentHandler**, on the line that begins **return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)**, change '**HelloWorldIntent**' to '**CaptureBirthdayIntent**'

This change ensures that the **canHandle()** function will be invoked when a **CaptureBirthdayIntent** request comes through. 

Your `CaptureBirthdayIntentHandler ` should now look like:

```py
class CaptureBirthdayIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

Now you need to update the logic within the handler so Alexa will confirm to the user that she heard their birthday. In this case, you will have Alexa read the birthday back to the user, like this: “Thanks, I'll remember that you were born on {month} {day} {year}.”

Start by creating three variables in the handler to save the slots the skill is collecting.

**d.** Within the **CaptureBirthdayIntentHandler**, find the line that begins **def handle(self, handler_input):**. Create a new line _below_it.

**e.** Copy and paste the following code on the new line:

```py
        slots = handler_input.request_envelope.request.intent.slots
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value
```

Next, update the **speak_output**. To do this, we use string interpolation to substitute values of our variables into placeholders in our string. While Python supports multiple ways to do this, we will use .format() function to replace placeholder values inside braces {} with the values of our variables.

This allows you to drop the new variables into a text string.

Here is an example of a string interpolation:

*`’Looks like you were born in #{month}’.format(month=month)`*

**f.** Within the **CaptureBirthdayIntentHandler**, in the **handle()** function, find the line that begins with **speak_output =**. Replace that line with the following code:

```py
speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)
```

Your **CaptureBirthdayIntentHandler** should now look like:

```py
class CaptureBirthdayIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value

        speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

You are almost finished. Remember changing the **HelloWorldIntentHandler** to **CaptureBirthdayIntentHandler**? In every skill that uses the SDK, there is a place to notify the SDK of the available handlers. This is called registering. Update the code to register the new handler.

**g.** Scroll down in the code until you find the line that begins **sb = SkillBuilder()**.

Under this line, you will notice the list of handlers in the skill. **HelloWorldIntentHandler** is listed, and you need to change it to **CaptureBirthdayIntentHandler**. Otherwise, the skill will give an error.

**h.** Replace the line **sb.add_request_handler(HelloWorldIntentHandler())** with **sb.add_request_handler(CaptureBirthdayIntentHandler())**

Your handler code at the bottom of the file should now look like:

### Register request / intent handlers
```py
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureBirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
```

**i.** Click **Save**.

**j.** Click **Deploy**. Because of the new handler, your skill will take a few moments to deploy.

## Step 5: Test your skill

It is time to test! The Cake Walk skill should now be able to do the following:
* **Ask** the user for their birthday
* **Listen** to the answer from the user and automatically follow up with questions if any required slots (month, day, year) are missing
* **Respond** to the user by repeating their birthday
Let's test the skill.

**a.** Click the **Test** tab.
Remember that you can test by typing what the user would say in the box at the top left, or you can speak to the skill by clicking and holding the microphone icon and speaking.

**b.** Test your skill by opening Cake Walk and responding when Alexa asks for your birthday.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/4/chapter4-5a.png)

> **If you are testing by typing what the user would say, spell out the numbers (for example, November seventh nineteen eighty three). Otherwise, the numbers won't be understood. You may have noticed that numbers have been have purposefully spelled out throughout the course. This is only a requirement when typing. If you speak to the skill, the numbers are automatically converted.**

Alexa should respond with, "Thanks, I'll remember that your birthday is {month} {day} {year}."
Go ahead and test what happens if you provide only the year, the year and the day, or other combinations. Alexa should prompt you for any slot values that you omit.

## Wrap-up
At this point, your skill has become slightly more nuanced. It can ask the user for their birthday and repeat it back to the user. Congratulations!

However, while your skill can ask for a user’s birthday, your skill doesn’t remember it the next time the skill is opened. It would be a better user experience if Cake Walk remembered the user’s birthday. In the next section, you will learn how to make your skill remember things.

## Code
If your skill isn’t working or you’re getting some kind of syntax error, download the code sample in Python from the link below. Then, go to the Code tab in the Alexa developer console and copy and paste the code into the **lambda_function.py** file. Be sure to save and deploy the code before testing it.

 [Python Github Code Sample, Module 2: Collecting Slots Turn by Turn](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-2) 

 [Continue to module 3](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-3)
