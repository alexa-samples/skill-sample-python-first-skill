## Adding memory to your skill
In this section, you will enable the Cake Walk skill to remember the user’s birthday. What’s the point of the skill collecting information if the skill won’t remember it?

Use the  [Alexa developer console](https://developer.amazon.com/alexa/console/ask)  for this module. Log in to the console and open the Cake Walk skill.

## Step 1: Use Amazon S3 to save and read data
Right now, you have the birthday, month, and year within the code. The problem is that the skill forgets these values when the code finishes running. To solve the problem, you are going to save the values to Amazon S3. This way, the skill can read them from session to session.

The SDK provides a useful mechanism for saving information across sessions: the AttributesManager. With the manager, your read/write code can remain the same, even if you change where you save your data later.

The backend code for Alexa skills can live on any HTTPS server. Most of the time, Alexa developers write and host their backend code using AWS. While building Cake Walk, you have been writing code in the developer console using an Alexa-hosted skill. That code is running on the AWS Free Tier, which has limitations. Alexa-hosted skills are great for learning to build and even to publish simple skills before you have a large audience. However, if your skill becomes popular, you may want to consider moving your backend code over to your own AWS resources.

How does this relate to adding memory to your skill? When using an Alexa-hosted skill for your backend code, it will be stored in Amazon S3. If you choose to build your code on your own AWS resources, it may make more sense to use Amazon DynamoDB. Don’t worry if you don’t know the difference between the two. The important thing to know is that the backend code you are writing now will work with Amazon S3, and it will only require minor changes to work with DynamoDB if you decide to migrate to your own AWS resources later.

Start by using the AttributesManager to save the user’s birthday in Cake Walk.

**a.** In the developer console, click the **Code** tab.

**b.** Double-click the**requirements.txt** file in the pane on the left. The file opens in the editor.

![](http://alexa-github.s3.amazonaws.com/python-requirements-1.png)

**c.** You are going to add a **requirement**. It’s easiest to put a new dependency at the bottom of the existing list.

**d.** Copy and paste the following line of code at the end of the file by adding a new line. This will import the dependency for the S3 adapter.

```
ask-sdk-s3-persistence-adapter
```

Your requirements.text file should now look like:

```
boto3==1.9.216
ask-sdk-core==1.11.0
ask-sdk-s3-persistence-adapter
```

![](http://alexa-github.s3.amazonaws.com/python-requirements-2.png)

**e.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-1e.png)

**f.** Switch back to the other file by clicking the **lambda_function.py** tab.
The new dependency allows you to use the AttributesManager to save and read user data using Amazon S3. Now, you need to import that dependency to the code. To do this, you need to let the code know the dependency exists.

**g.** In the **lambda_function.py** file, find the line that begins **import ask_sdk_core.utils as ask_utils**. Create a new line just _below_ it, and copy and paste in the following code:

```py
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])
```

**h.** In the **lambda_function.py** file, find the line that begins **from ask_sdk_core.skill_builder import SkillBuilder**. Replace this line with the following code:

```py
from ask_sdk_core.skill_builder import CustomSkillBuilder
```

This will import the S3 Persistence adapter, create your S3 adapter and set you up with a bucket on S3 to store your data. Once done, this section of code should look like:

```py
import logging
import ask_sdk_core.utils as ask_utils
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
```

**i.** In the **lambda_function.py** file, scroll all the way down to find the line that begins **sb = SkillBuilder()**. Replace this line with the following code:

```py
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
```

**j.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-1e.png)

You are now set up to use AttributesManager to save and read data to Amazon S3. Later, if you decide to move your skill’s backend code to your own AWS resources, you will reverse the changes made in this step.

## Step 2: Save Data
Now you will modify the code to save the user’s birthday. On the **Code** tab, within the **lambda_function.py** file, find the **CaptureBirthdayIntentHandler.** This is the handler you created in the last section.

**a.** You will use the AttributesManager to save the user’s birthday. Within the **CaptureBirthdayIntentHandler**, in the **handle()** function, find the line that begins **day = slots["day"].value**. Create a new line just _below_ it, and copy and paste in the following code:

```py
attributes_manager = handler_input.attributes_manager
```

The Cake Walk skill code receives the year, month, and day. You need to tell Amazon S3 to save these values. The code tells the AttributesManager what the data is, and the manager sends it to Amazon S3.

**b.** Within the **CaptureBirthdayIntentHandler**, find the line you just added (it begins **attributes_manager = handler_input.attributes_manager**). Create a new line just _below_ it, and copy and paste in the following code:

```py
birthday_attributes = {
            "year": year,
            "month": month,
            "day": day
        }
```

This piece of code is mapping the variables already declared in the code to corresponding variables that will be created in Amazon S3 when the code runs.

These variables are now declared as _persistent_ (they are local to the function in which they are declared, yet their values are retained in memory between calls to the function). Now you can save the user’s data to them. First, use the **AttributesManager** to set the data to save to Amazon S3.


**c.** Within the **CaptureBirthdayIntentHandler**, find the line you just added (it begins **birthday_attributes =**). Create a new line just _below_ it, and copy and paste in the following code:

```py
attributes_manager.persistent_attributes = birthday_attributes
```

**d.** Within the **CaptureBirthdayIntentHandler**, find the line you just added (it begins **attributes_manager.persistent_attributes = birthday_attributes**). Create a new line just _below_ it, and copy and paste in the following code:

```py
attributes_manager.save_persistent_attributes()
```

 Your final code should now look like:

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

        attributes_manager = handler_input.attributes_manager

        birthday_attributes = {
            "year": year,
            "month": month,
            "day": day
        }

        attributes_manager.persistent_attributes = birthday_attributes
        attributes_manager.save_persistent_attributes()

        speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.’.format(month=month, day=day, year=year)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
```

**e.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-1e.png)

## Step 3: Read stored data
Great, now the user’s birthday is saved to Amazon S3. However, now the skill needs to be updated so the next time the user opens Cake Walk, Alexa knows the user’s birthday information is stored and she doesn’t have to ask for it. To do this, you will modify the code to read the data stored in Amazon S3 before asking the user for their birthday. If the data exists, Alexa doesn’t need to ask for it. If the data isn’t there, Alexa will ask for the information.

> **An Amazon S3 bucket is a public cloud storage resource. A bucket is similar to a file folder for storing objects, which consists of data and descriptive metadata.**

A new handler is needed to read the stored data. The **canHandle()** and **handle()** functions in the new handler will communicate with Amazon S3. You will add it between the **LaunchRequestHandler** and the **CaptureBirthdayIntentHandler**.

**a.** Find the line that begins **CaptureBirthdayIntentHandler**. Create a new line just above, and copy and paste in the following code for the new handler:

```py
class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    """Handler for launch after they have set their birthday"""

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("year" in attr and "month" in attr and "day" in attr)

        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        year = attr[‘year’]
        month = attr[‘month’] # month is a string, and we need to convert it to a month index later
        day = attr[‘day’]

        # TODO:: Use the settings API to get current date and then compute how many days until user’s bday
        # TODO:: Say happy birthday on the user’s birthday

        speak_output = "Welcome back it looks like there are X more days until your y-th birthday."
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
```

The new handler has the **canHandle()** and **handle()** functions. The **canHandle()** function checks if the user's birthday information is saved in Amazon S3. If it is, the handler lets the SDK know it can do the work (it has the user's birthday information and can do what comes next). The **handle()** function tells Alexa to say, "Welcome back. It looks like there are x more days until your y-th birthday."

When you changed the name of a handler in a previous section, you also had to change the name in the list of handlers at the bottom of the code. Because you added a new handler, you must add the new handler to this list.

**b.** Toward the bottom of the code, find the line that begins with **sb.add_request_handler(LaunchRequestHandler())**, Create a new line just _above_ it. Copy and paste in the following code on the new line:

```py
sb.add_request_handler(HasBirthdayLaunchRequestHandler())
```

That section of code should now look like the following:

```py
sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureBirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn’t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
```

**c.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-1e.png)

**d.** Click **Deploy**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-3f.png)

# How to delete or reset the user’s birthday
When testing, you may need to delete or reset the user’s birthday. There are two ways to do this.

Use the first method in the simulator on the **Test** tab of the Alexa developer console. Type or say, "Alexa, tell Cake Walk I was born on {month} {day} {year}."

The second method is to delete the saved information from Amazon S3 by using the following steps:

**a.** While on the **Code** tab, click **Media storage** on the bottom left-hand corner of the screen. The S3 Management Console opens.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-reset-a.png)

**b.** At the top of the page, find the breadcrumbs. Click the breadcrumb that starts **amzn-1-ask-skill**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-reset-b.png)

**c.** Click on the check box next to the file(s) that begins with **amzn1.ask.account**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/5/chapter5-reset-c.png)

**d.** Click **Actions**.

**e.** Click **Delete**.

**f.** Click **Delete**. The user’s birthday is deleted.

## Wrap-up
Here’s a summary of what you did in this section. First, you adjusted the Cake Walk skill to use the AttributesManager to save and read user information to Amazon S3. Then, you added code to the **CaptureBirthdayIntentHandler** to save the user’s birthday. Lastly, you created a new handler (**HasBirthdayLaunchRequestHandler**) so Alexa doesn’t repeatedly ask the same user for their birthday.

It’s time to test, so click the **Test** tab, then follow the steps below.

### Step 1: Launch the skill
Say “Open Cake Walk”.

Alexa should respond, “Hello! This is Cake walk. When is your birthday?”

### Tell Alexa your birthday
Feel free to try giving Alexa partial information and ensure she asks for and collects the missing information.

Once she has your birth month, day, and year, Alexa should respond, “Thanks, I’ll remember that your birthday is {month} {day} {year}.”

The session ends. At this point, without the code you added in this section, the next time you invoke the skill, Alexa would ask for your birthday again. Now, Alexa stores this information.

### Launch the skill a second time
Say “Open Cake Walk”.

Alexa should respond, “Welcome back. It looks like there are X more days until your y-th birthday.”

You probably noticed that, with the way the code works right now, Alexa is saying “X” and “Y T H”. Don’t worry. In the next section, you will work on the code to calculate how many days until the user’s next birthday so Alexa can respond with that information.

## Code
If your skill isn’t working or you’re getting some kind of syntax error, download the code sample in Python from the link below. Then, go to the Code tab in the Alexa developer console and copy and paste the code into the **lambda_function.py** file. Be sure to save and deploy the code before testing it.

 [Python Github Code Sample, Module 3: Add Memory to Your Skill](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-3)

 [Continue to module 6](https://developer.amazon.com/alexa/alexa-skills-kit/resources/training-resources/cake-walk/cake-walk-6)
