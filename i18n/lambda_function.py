# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)
# Please visit https://alexa.design/cookbook for additional examples on
# implementing slots, dialog management,
# session persistence, api calls, and more.

import requests
import logging
import calendar
from datetime import datetime
from pytz import timezone
import gettext

from alexa import data

from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor
)
from ask_sdk_core.utils import is_request_type, is_intent_name

s3_adapter = S3Adapter(bucket_name="custom-walk-testing")
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


class LaunchRequestIntentHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        _ = handler_input.attributes_manager.request_attributes["_"]

        speech = _(data.WELCOME_MSG)
        reprompt = _(data.WELCOME_REMPROMPT_MSG)

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for launch after they have set their birthday
    """

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = (
            "year" in attr and "month" in attr and "day" in attr)

        return attributes_are_present and is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        _ = handler_input.attributes_manager.request_attributes["_"]

        attr = handler_input.attributes_manager.persistent_attributes

        year = int(attr['year'])
        # month is a string, and we need to convert it to a month index later
        month = attr['month']
        day = int(attr['day'])

        # get device id / timezones
        sys_object = handler_input.request_envelope.context.system

        # get systems api information
        api_endpoint = sys_object.api_endpoint
        device_id = sys_object.device.device_id
        api_access_token = sys_object.api_access_token

        # construct systems api timezone url
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(
            api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = ""
        try:
            r = requests.get(url, headers=headers)
            res = r.json()
            logger.info("Device API result: {}".format(str(res)))
            userTimeZone = res
        except Exception:
            speech = _(data.ERROR_TIMEZONE_MSG)
            handler_input.response_builder.speak(speech)
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
        # alexa will automatically correct the oridinal for you.
        # no need to worry about when to use st, th, rd
        speak_output = _(data.HAPPY_BIRTHDAY_MSG).format(
            str(current_year - year))
        if now_date != next_birthday:
            diff_days = abs((now_date - next_birthday).days)
            logger.info(speak_output)
            speak_output = _(data.WELCOME_BACK_MSG).format(
                diff_days,
                (current_year-year)
            )
            if(diff_days != 1):
                speak_output = _(data.WELCOME_BACK_MSG_plural).format(
                    diff_days,
                    (current_year-year)
                )

        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class BirthdayIntentHandler(AbstractRequestHandler):
    """
    Handler for Capturing the Birthday
    """

    def can_handle(self, handler_input):
        return is_intent_name("CaptureBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        _ = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        locale = handler_input.request_envelope.request.locale

        # extract slot values
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value

        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['year'] = year
        session_attr['month'] = month
        session_attr['day'] = day

        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        date = self.formatDate(year, month, day, locale)

        speech = _(data.REGISTER_BIRTHDAY_MSG).format(date[0], date[1], date[2])
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

    # function to ensure that the date format corresponds with the locale that is triggering thee skill
    def formatDate(self, year, month, day, locale):
        if locale == 'en-US':
            date = [month, day, year]
        elif locale == 'jp-JP':
            date = [year, month, day]
        else:
            date = [day, month, year]

        return date




class HelpIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.HelpIntent
    """

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.HELP_MSG)

        handler_input.response_builder.speak(
            speak_output
        ).ask(speak_output)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info(exception)
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.ERROR_MSG)
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.CancelIntent and AMAZON.StopIntent
    """

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
            and is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.GOODBYE_MSG)
        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    Handler for SessionEndedRequest
    """

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here
        return handler_input.response_builder.response


class CacheSpeechForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the output speech and reprompt to session attributes,
    for repeat intent.
    """

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["speech"] = response.output_speech
        session_attr["reprompt"] = response.reprompt


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext


# register request / intent handlers
sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(BirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# register localization interceptor and cache speech interceptor
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_response_interceptor(CacheSpeechForRepeatInterceptor())

lambda_handler = sb.lambda_handler()
