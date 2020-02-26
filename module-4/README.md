## Using the Alexa Settings API
In this section, you will enable the Cake Walk skill to calculate the number of days until the user’s next birthday.
Use the  [Alexa developer console](https://developer.amazon.com/alexa/console/ask)  for this module. Log in to the console and open the Cake Walk skill.

To calculate the number of days until the user’s next birthday accurately, we need additional information, like current date, and user’s time zone. Luckily, you can use the Alexa Settings API to get this information. To do that, we need to pass the following information to the Alexa Settings API:

1. Device ID
2. URL for the Alexa Settings API (API Endpoint)
3. Authorization token (Access Token)
4. Import supporting libraries (We will do this in Step 3)

We will retrieve items 1-3 in Step 1 below, and tackle the import of libraries in in Step 3.

## Step 1: Get Device ID, API endpoint, and Authorization Token for Alexa Settings API
To query the Alexa Settings API, you need to provide the device ID for the Alexa-enabled device that prompted the Cake Walk skill to open.

The device ID is provided in every request that comes to the skill code. We will traverse the request object to get the device ID using the **requestEnvelope:**

```
handlerInput.requestEnvelope.context.System.device.deviceId
```

> **Alternatively, the SDK provides a utility function that simplifies getting the device ID. Feel free to use it instead:**
>
> **device_id = ask_sdk_core.utils.request_util.get_device_id(handler_input)**
>
> *For additional information, refer to  [ASK SDK Python Utilities. ](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/api/core.html#module-ask_sdk_core.utils.predicate)*

**a.** In the developer console, click the **Code** tab, then click on the file **requirements.txt**

**b.** Add a new line at the end of this file, and type the following line of code -

```
pytz
```

The **pytz** library allows accurate and cross platform timezone calculations, and will help us figure out the user's timezone accurately.

Your **requirements.txt** file should now look like:

```
boto3==1.9.216
ask-sdk-core==1.11.0
ask-sdk-s3-persistence-adapter
pytz
```

**c.** In the developer console, click the **Code** tab, then click on the file **lambda_function.py**

**d.** Find the **HasBirthdayLaunchRequestHandler** and then the **handle()** function within the handler. Create a new line just below the line that begins **day = attr['day']**. Copy and paste in the following code:

```py
        # get device id
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        # get Alexa Settings API information
        api_endpoint = sys_object.api_endpoint
        api_access_token = sys_object.api_access_token
```

Your **HasBirthdayLaunchRequestHandler** should now look like:

```py
class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    “””Handler for launch after they have set their birthday”””

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (“year” in attr and “month” in attr and “day” in attr)

        return attributes_are_present and ask_utils.is_request_type(“LaunchRequest”)(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        year = attr['year']
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = attr['day']

        # get device id
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        # get systems api information
        api_endpoint = sys_object.api_endpoint
        api_access_token = sys_object.api_access_token

        # TODO:: Use the settings API to get current date and then compute how many days until user’s bday
        # TODO:: Say happy birthday on the user’s birthday

        speak_output = “Welcome back it looks like there are X more days until your y-th birthday.”
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
```

Now that we have the Device ID, API endpoint, and the access token, we are ready to call the Alexa Settings API to get the user time zone.

## Step 2: Using the Alexa Settings API to retrieve the user time zone
There’s a chance that an error can happen when the code makes a call to the Alexa Settings API. For example, if the API takes too long to respond, the code could time out. Therefore, you need to wrap the code in a **try_catch_**_ block. A _**_try_catch** block is a way to ensure the skill code doesn’t crash if it encounters an error. You will wrap the code that _could_ crash in a **try** block. If the code within that block crashes, the **catch** block will run to handle errors.

You want to know the time zone for the user’s Alexa-enabled device. In the **try** block, use **serviceClientFactory** to get the settings service client—upsServiceClient—and pass the device ID to the **getSystemTimeZone** function to get the time zone. The **catch** block will log an error message using **console.log** and return an error message response that Alexa will say to the user.

**a.** Within the **HasBirthdayLaunchRequestHandler**, find the line that begins with **api_access_token = sys_object.api_access_token** (you just added this in the previous step). Create a new line just below this, and copy/paste the following code:

```py
        # construct systems api timezone url
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = ""
        try:
            r = requests.get(url, headers=headers)
            res = r.json()
            logger.info("Device API result: {}".format(str(res)))
            userTimeZone = res
        except Exception:
            handler_input.response_builder.speak("There was a problem connecting to the service")
            return handler_input.response_builder.response
```

Your **HasBirthdayLaunchRequestHandler** should now look like:

```py
class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    “””Handler for launch after they have set their birthday”””

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (“year” in attr and “month” in attr and “day” in attr)

        return attributes_are_present and ask_utils.is_request_type(“LaunchRequest”)(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        year = attr['year']
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = attr['day']

        # get device id
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        # get Alexa Settings API information
        api_endpoint = sys_object.api_endpoint
        api_access_token = sys_object.api_access_token

        # construct systems api timezone url
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = “”
        try:
            r = requests.get(url, headers=headers)
            res = r.json()
            logger.info(“Device API result: {}”.format(str(res)))
            userTimeZone = res
        except Exception:
            handler_input.response_builder.speak(“There was a problem connecting to the service”)
            return handler_input.response_builder.response

        # TODO:: Use the settings API to get current date and then compute how many days until user's bday
        # TODO:: Say happy birthday on the user's birthday

        speak_output = "Welcome back it looks like there are X more days until your y-th birthday."
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
```

**b.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/6/chapter6-1d.png)


## Step 3: Retrieve the current date
The code will use the time zone to get the current date. You can use the **currentDateTime** function to return the correct date according to the time zone captured from the user's device. You will add this function below the **try/catch** block added in a previous step.

**a.** In the **lambda_function.py** file, find the line that begins **import ask_sdk_core.utils as ask_utils**. Create a new line just _below_ it, and copy and paste in the following code:

```py
import os
import requests
import calendar
from datetime import datetime
from pytz import timezone
```

We will need these libraries to work with date and timezones. Once done, this section of code should look like:

```py
import logging
import ask_sdk_core.utils as ask_utils
import os
import requests
import calendar
from datetime import datetime
from pytz import timezone
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ[“S3_PERSISTENCE_BUCKET”])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
```

**b.** Within the **HasBirthdayLaunchRequestHandler**, find the comment that begins with **# TODO:: Use the settings API to get current date and then compute how many days until user’s bday**. Replace this line with the following code:

```py
        # getting the current date with the time
        now_time = datetime.now(timezone(userTimeZone))
```

**c.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/6/chapter6-1d.png)

## Step 4: Extract the month, day, and year
You would like the Cake Walk skill to wish the user happy birthday at midnight in their time zone. This could be a problem because **currentDateTime** provides the date and time to the second. The Cake Walk skill does not ask the user to provide their birthday down to the second. Therefore, the code needs to extract just the month, day, and year from **currentDateTime**, and then re-create the date without the seconds included.

**a.** Within the **HasBirthdayLaunchRequestHandler**, in the **handle()** function, create a new line just _below_ the code you just added (**now_time =**). Copy and paste in the following code:

```py
        # Removing the time from the date because it affects our difference calculation
        now_date = datetime(now_time.year, now_time.month, now_time.day)
        current_year = now_time.year
```

Your **HasBirthdayLaunchRequestHandler** should now look like:

```py
class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    “””Handler for launch after they have set their birthday”””

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (“year” in attr and “month” in attr and “day” in attr)

        return attributes_are_present and ask_utils.is_request_type(“LaunchRequest”)(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        year = attr['year']
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = attr['day']

        # get device id
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        # get Alexa Settings API information
        api_endpoint = sys_object.api_endpoint
        api_access_token = sys_object.api_access_token

        # construct systems api timezone url
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = “”
        try:
            r = requests.get(url, headers=headers)
            res = r.json()
            logger.info(“Device API result: {}”.format(str(res)))
            userTimeZone = res
        except Exception:
            handler_input.response_builder.speak(“There was a problem connecting to the service”)
            return handler_input.response_builder.response

        # getting the current date with the time
        now_time = datetime.now(timezone(userTimeZone))

        # Removing the time from the date because it affects our difference calculation
        now_date = datetime(now_time.year, now_time.month, now_time.day)
        current_year = now_time.year

        # TODO:: Say happy birthday on the user’s birthday

        speak_output = "Welcome back it looks like there are X more days until your y-th birthday."
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
```

**b.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/6/chapter6-1d.png)

## Step 5: Determine the user's next birthday
Now the code needs to determine the user's next birthday. First, the code will combine the year and month of their birthday with the current year. Second, the code will determine if the user's birthday has already passed this calendar year. If it has, the code will add a year to the value of their next birthday.

**a.** Within the **HasBirthdayLaunchRequestHandler**, in the **handle()** function, create a new line just _below_ the lines you just added (**now_date** and **current_year**). Copy and paste in the following code:

```py
# getting the next birthday
month_as_index = list(calendar.month_abbr).index(month[:3].title())
next_birthday = datetime(current_year, month_as_index, day)
```

**b.** Within the **HasBirthdayLaunchRequestHandler**, find the following code

```py
year = attr['year']
month = attr['month'] # month is a string, and we need to convert it to a month index later
day = attr['day']
```

Replace above lines of code with the ones below:

```py
year = int(attr['year'])
month = attr['month'] # month is a string, and we need to convert it to a month index later
day = int(attr['day'])
```

**c.** Click **Save**.

## Step 6: Compute difference between current date and user's next birthday
Now that the code has the current date and the date of the user's next birthday, it's time to compute the difference. First, the code needs to convert each date into Unix epoch time (the number of seconds elapsed since 00:00:00 January 1, 1970, Coordinated Universal Time (UTC), minus leap seconds).
Second, the code will calculate the difference in milliseconds between the two dates and take the absolute value of the difference.
Finally, the code will convert the difference in milliseconds back to days. One day in milliseconds = 24 hours X 60 minutes X 60 seconds X 1000 milliseconds.
The following is how this would appear in the code—but don’t add it to the code yet:

```py
diff_days = abs((now_date - next_birthday).days)
```

 The code only needs to calculate the difference when it’s not the users birthday. Therefore, you will wrap this code in an **if** statement that checks if the current date is the user’s birthday.

If it is the user’s birthday, you want the skill to wish them happy birthday. You can combine the code for this with the **if** statement so when it is not the user’s birthday, the **speakOutput** is set to tell the user how many days until their next birthday.

**a.** Within the **HasBirthdayLaunchRequestHandler**, in the **handle()** function, find the line that begins with **speak_output = "Welcome back it looks like there are X more days until your y-th birthday."**. Replace that line with the following code:

```py
     # check if we need to adjust bday by one year
        if now_date > next_birthday:
            next_birthday = datetime(
                current_year + 1,
                month_as_index,
                day
            )
            current_year += 1
        # setting the default speak_output to Happy xth Birthday!!
        # Alexa will automatically correct the ordinal for you.
        # no need to worry about when to use st, th, rd
        speak_output = “Happy {}th birthday!”.format(str(current_year - year))
        if now_date != next_birthday:
            diff_days = abs((now_date - next_birthday).days)
            speak_output = “Welcome back. It looks like there are \
                            {days} days until your {birthday_num}th\
                            birthday”.format(
                                days=diff_days,
                                birthday_num=(current_year-year)
                            )
```

**b.** Within the **HasBirthdayLaunchRequestHandler**, remove the comment that begins with **# TODO:: Say happy birthday on the user’s birthday**. We’ve just added this functionality.

Your **HasBirthdayLaunchRequestHandler** should now look like:

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
        year = int(attr['year'])
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = int(attr['day'])

        # get device id
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        # get Alexa Settings API information
        api_endpoint = sys_object.api_endpoint
        api_access_token = sys_object.api_access_token

        # construct systems api timezone url
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = ""
        try:
	        r = requests.get(url, headers=headers)
	        res = r.json()
	        logger.info("Device API result: {}".format(str(res)))
	        userTimeZone = res
        except Exception:
	        handler_input.response_builder.speak("There was a problem connecting to the service")
	        return handler_input.response_builder.response

        # getting the current date with the time
        now_time = datetime.now(timezone(userTimeZone))

        # Removing the time from the date because it affects our difference calculation
        now_date = datetime(now_time.year, now_time.month, now_time.day)
        current_year = now_time.year

        # getting the next birthday
        month_as_index = list(calendar.month_abbr).index(month[:3].title())
        next_birthday = datetime(current_year, month_as_index, day)

        # check if we need to adjust bday by one year
        if now_date > next_birthday:
            next_birthday = datetime(
                current_year + 1,
                month_as_index,
                day
            )
            current_year += 1
        # setting the default speak_output to Happy xth Birthday!!
        # alexa will automatically correct the ordinal for you.
        # no need to worry about when to use st, th, rd
        speak_output = "Happy {}th birthday!".format(str(current_year - year))
        if now_date != next_birthday:
            diff_days = abs((now_date - next_birthday).days)
            speak_output = "Welcome back. It looks like there are \
                            {days} days until your {birthday_num}th\
                            birthday".format(
                                days=diff_days,
                                birthday_num=(current_year-year)
                            )

        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
```

**c.** Click **Save**.

![](https://d3ogm7ac91k97u.cloudfront.net/content/dam/alexa/alexa-skills-kit/courses/cake-walk/6/chapter6-1d.png)

## Step 7: Save, deploy, and test

**a.** Click **Deploy** to build the skill.

**b.** Go to the **Test** tab, open the skill, and see if Alexa responds by telling you how many days until your next birthday. If she does, congratulations!

## Code
If your skill isn’t working or you’re getting some kind of syntax error, download the code sample in Python from the link below. Then, go to the Code tab in the Alexa developer console and copy and paste the code into the **lambda_function.py** file. Be sure to save and deploy the code before testing it.

 [Python Github Code Sample, Module 4: Using the Alexa Setting API](https://github.com/alexa/skill-sample-python-first-skill/tree/master/module-4)