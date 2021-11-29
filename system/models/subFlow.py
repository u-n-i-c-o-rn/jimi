import jimi
import time

class _subFlow(jimi.action._action):
	triggerID = str()
	customEventsValue = False
	eventsValue = str()
	customEventsList = False
	eventsList = list()
	mergeFinalDataValue = False 
	mergeFinalEventValue = False
	mergeFinalConductValue = False
	maxRetries = int()
	retryDelay = int()

	def doAction(self,data):
		triggerID = jimi.helpers.evalString(self.triggerID,{"data" : data["flowData"]})

		events = [data["flowData"]["event"]]

		tempData = jimi.conduct.copyData(jimi.conduct.dataTemplate(data,keepEvent=True))
		tempData["flowData"]["callingTriggerID"] = data["flowData"]["trigger_id"]

		if self.customEventsValue:
			events = jimi.helpers.evalString(self.eventsValue,{"data" : data["flowData"]})
			if type(events) is not list:
				events = [events]
		if self.customEventsList:
			events = jimi.helpers.evalList(self.eventsList,{"data" : data["flowData"]})

		while True:
			trigger = jimi.trigger._trigger().getAsClass(id=triggerID)
			if len(trigger) == 1:
				subflowResult = True
				trigger = trigger[0]
				finalData = trigger.notify(events,tempData)
				if "subflowResult" in finalData["flowData"]["var"]:
					subflowResult = finalData["flowData"]["var"]["subflowResult"]
				if subflowResult:
					if self.mergeFinalDataValue:
						data["flowData"]["action"] = finalData["flowData"]["action"]
						data["flowData"]["var"] = finalData["flowData"]["var"]
						data["flowData"]["plugin"] = finalData["flowData"]["plugin"]
					if self.mergeFinalEventValue:
						data["eventData"]["var"] = finalData["eventData"]["var"]
						data["eventData"]["plugin"] = finalData["eventData"]["plugin"]
					if self.mergeFinalConductValue:
						data["conductData"]["var"] = finalData["conductData"]["var"]
						data["conductData"]["plugin"] = finalData["conductData"]["plugin"]
				elif self.maxRetries > 0:
					self.maxRetries -= 1
					time.sleep(self.retryDelay)
				else:
					break
			else:
				return { "result" : False, "rc" : 5, "msg" : "Unable to find the specified triggerID={0}".format(triggerID) }

		return { "result" : subflowResult, "rc" : 0 }
