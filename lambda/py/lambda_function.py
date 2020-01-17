# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import os
import json
import locale
import requests
import calendar
import gettext
from datetime import datetime
from pytz import timezone
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from alexa import data

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_core.utils import is_request_type, is_intent_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        speech = data["WELCOME_MSG"]
        reprompt = data["WELCOME_REPROMPT_MSG"]

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

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
        month = attr['month'] # month gets stored as string, so no need to convert it to int
        day = int(attr['day'])
        
        data = handler_input.attributes_manager.request_attributes["_"]
        error_timezone_speech = data["ERROR_TIMEZONE_MSG"]

        # get skill locale from request
        skill_locale = handler_input.request_envelope.request.locale

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
	        handler_input.response_builder.speak(error_timezone_speech)
	        return handler_input.response_builder.response

        # get the current date with the time
        now_time = datetime.now(timezone(userTimeZone))

        # remove the time from the date because it affects our difference calculation
        now_date = datetime(now_time.year, now_time.month, now_time.day)
        current_year = now_time.year

        # get the next birthday
        next_birthday = datetime(current_year, month, day)

        # check if we need to adjust birthday by one year
        if now_date > next_birthday:
            next_birthday = datetime(
                current_year + 1,
                month,
                day
            )
            current_year += 1
       
        # calculate how many days until the next birthday
        diff_days = abs((now_date - next_birthday).days)

        # the following locales have a different HAPPY_BIRTHDAY_MSG for plural
        if (('fr' in skill_locale) or ('it' in skill_locale) or ('es' in skill_locale)) or ('pt' in skill_locale):

            # if it is not the user birthday
            if now_date != next_birthday:
                if diff_days > 1:
                    speak_output = data["WELCOME_BACK_MSG_plural"].format(diff_days, current_year-year)
                if diff_days < 2:
                    speak_output = data["WELCOME_BACK_MSG"].format(diff_days, current_year - year)

            # if it is the user birthday
            else:
                if (current_year - year > 1):
                    speak_output = data["HAPPY_BIRTHDAY_MSG_plural"].format(current_year - year)
                if current_year - year < 2:
                    speak_output = data["HAPPY_BIRTHDAY_MSG"].format(current_year - year)

        # all other locales
        else:
            speak_output = data["HAPPY_BIRTHDAY_MSG"].format(current_year - year)

            # if it is not the user birthday
            if now_date != next_birthday:
                if diff_days > 1:
                    # for ja and hi, the order of the slots is inverted, i.e. year before day
                    if ('ja' in skill_locale or 'hi' in skill_locale):
                        speak_output = data["WELCOME_BACK_MSG_plural"].format(current_year-year, diff_days)
                    else:
                        speak_output = data["WELCOME_BACK_MSG_plural"].format(diff_days, current_year-year)
                elif diff_days < 2:
                    # for ja and hi, the order of the slots is inverted, i.e. year before day
                    if ('ja' in skill_locale or 'hi' in skill_locale):
                        speak_output = data["WELCOME_BACK_MSG"].format(current_year - year, diff_days)
                    else:
                        speak_output = data["WELCOME_BACK_MSG"].format(diff_days, current_year - year)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class BirthdayIntentHandler(AbstractRequestHandler):
    """
    Handler for Capturing the Birthday
    """

    def can_handle(self, handler_input):
        return is_intent_name("CaptureBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        skill_locale = handler_input.request_envelope.request.locale

        # extract slot values
        year = slots["year"].value

        # if the interaction models uses synonyms for the month slot (for example hi-IN) the following logic will return the ID for the value
        try: 
            month = slots["month"].resolutions.resolutions_per_authority[0].values[0].value.id
        except:
        # if the above fails, it means that there are no synonyms being used, so retrieve the value for the month in the regular way
            month = slots["month"].value

        day = slots["day"].value

        # get the month as an integer instead of string
        month_as_index = self.monthIndex(month[:3])
        
        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['year'] = year
        session_attr['month'] = month_as_index
        session_attr['day'] = day

        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        # ensure that the order the arguments is correct (MM/DD/YYYY or DD/MM/YYYY) according to locale
        date = self.formatDate(year, month, day, skill_locale)

        speech = data["REGISTER_BIRTHDAY_MSG"].format(date[0], date[1], date[2])
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.set_should_end_session(True)
        return handler_input.response_builder.response

    # function to ensure that the date format corresponds with the locale that is triggering thee skill
    def formatDate(self, year, month, day, skill_locale):
        if skill_locale == 'en-US':
            # MM/DD/YYYY for USA
            date = [month, day, year]
        elif skill_locale == 'ja-JP':
            # YYYY/MM/DD for Japan
            date = [year, month, day]
        else:
            # DD/MM/YYY for RoW
            date = [day, month, year]
        return date

    # function to convert a month name to number, i.e. March as 3, July as 7 and so on
    def monthIndex(self, month):
        month_list = list(calendar.month_name)
        i = 0
        while i < len(month_list):
            if (month.lower() in month_list[i].lower()):
                return i
            i += 1

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["HELP_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["GOODBYE_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = data["REFLECTOR_MSG"].format(intent_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["ERROR_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        skill_locale = handler_input.request_envelope.request.locale

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        data = language_data[skill_locale[:2]]
        # if a more specialized translation exists, then select it instead
        # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
        #          then pick that instead
        if skill_locale in language_data:
            data.update(language_data[skill_locale])
        handler_input.attributes_manager.request_attributes["_"] = data

        # configure the runtime to treat time according to the skill locale
        skill_locale = skill_locale.replace('-','_')
        locale.setlocale(locale.LC_TIME, skill_locale)
        

sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn’t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())


lambda_handler = sb.lambda_handler()