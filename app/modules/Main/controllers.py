from flask import Blueprint, render_template

import requests
import datetime

mod_main = Blueprint('Main',__name__)

@mod_main.route('/dashboard', methods=['GET', 'POST'])

#no data anonymization yet
#VIDEO MISSING
#for testing the reveal.js tracking container need to be running and you should
#use the exemplary presentation for tracking data
#currently quiz and dwellTimesObject get userToken and studentId appended


def main():
    #send get request to get json object with tracking data
    response = requests.get("http://localhost:4567/all").json()
    numberOfTrackedSessions = len(response)

    #initialization
    arrayWithStudentIDs = []
    totalDwellTimeSeconds = 0
    sumProgress = 0
    sumSlidesLookedAt = 0
    dwellTimesAllSessionsList = []
    quizSessionList = []
    audioSessionList = []
    #videoSessionList = []
    numberOfTimesFirstQuizPageWasReached = 0
    quizExisting = False

    for i in range(0, numberOfTrackedSessions):

        currentStudentID = response[i].get('student_id')
        timestampSessionBegin = response[i].get('created_at')
        timestampUpdated = response[i].get('updated_at')
        presentationUrl = response[i].get('tracking_json').get('presentationUrl')
        numberOfSlides = response[i].get('tracking_json').get('totalNumberOfSlides')
        userToken = response[i].get('tracking_json').get('userToken')
        dwellTimesObject = response[i].get('tracking_json').get('dwellTimes')
        numberOfSlidesPerTrackingSession = len(dwellTimesObject)
        timelineData = response[i].get('tracking_json').get('timeline')

        #bool added to avoid wrong measures (multiple quiz entries in session object when quiz is completed)
        numberOfTimesFirstQuizPageWasReachedBool = False


        #iterate through timeline data to get quiz info for session
        for j in range(0, len(timelineData)):

            #VORHER außerhalb der for schleife
            sessionQuizObject = []
            sessionAudioObject = []
            #sessionVideoObject = []

            if timelineData[j].get('type') == "audio":
                quizExisting = True
                if timeline[j].get('mediaEvent') == "play":
                    audioStart = timeline[j].get('timestamp')
                    audioID = timeline[j].get('metadata').get('id')
                    audioMediaSource = timeline[j].get('metadata').get('mediaSoure')

                if timeline[j].get('mediaEvent') == "pause":
                    audioPause = timeline[j].get('timestamp')
                    audioLasted = audioPause - audioStart
                    sessionAudioObject.append(audioID)
                    sessionAudioObject.append(audioMediaSource)
                    sessionAudioObject.append(audioLasted)



            if timelineData[j].get('type') == "quiz":
                if timelineData[j].get('score') != None:
                    quizScore = timelineData[j].get('score')
                    quizDwellTime = timelineData[j].get('dwellTime')
                else:
                    quizScore = 0
                    quizDwellTime = None

                #print("quizDwellTime: " + str(quizDwellTime))
                #print("quizScore: " + str(quizScore))

                if numberOfTimesFirstQuizPageWasReachedBool == False:
                    numberOfTimesFirstQuizPageWasReached = numberOfTimesFirstQuizPageWasReached + 1
                    numberOfTimesFirstQuizPageWasReachedBool = True
                quizId = timelineData[j].get('metadata').get('id')
                quizName = timelineData[j].get('metadata').get('name')
                quizTopic = timelineData[j].get('metadata').get('topic')
                quizTopic = quizTopic.replace("<p>", "")
                quizTopic = quizTopic.replace("</p>", "")
                quizNumberOfQuestions = timelineData[j].get('metadata').get('numberOfQuestions')
                timestampOfQuizSession =  timelineData[j].get('timestamp')

                sessionQuizObject.append(quizScore)
                sessionQuizObject.append(quizDwellTime)
                sessionQuizObject.append(quizId)
                sessionQuizObject.append(quizName)
                sessionQuizObject.append(quizTopic)
                sessionQuizObject.append(quizNumberOfQuestions)
                sessionQuizObject.append(timestampOfQuizSession)

                sessionQuizObject.append(currentStudentID)
                sessionQuizObject.append(userToken)
                #QUIZ LOGGING
                #print("quizId: " + str(quizId))
                #print("quizName: " + str(quizName))
                #print("quizTopic: " + str(quizTopic))
                #print("quizNumberOfQuestions: " + str(quizNumberOfQuestions))
                #print("timestampOfQuizSession: " + str(timestampOfQuizSession))

                #VORHER eins nach links eingerueckt
                #building the final quiz list with all quiz session elements
                if len(sessionQuizObject) > 0:
                    quizSessionList.append(sessionQuizObject)
                audioSessionList.append(sessionAudioObject)
                #videoSessionList.append(sessionVideoObject)

        sessionDwellTimeObject = []
        #iterate through object to get individual dwell time per slide (for every tracking sesion)
        for x in range(0, numberOfSlidesPerTrackingSession):
            dwellTimePerSlide = dwellTimesObject[x].get('dwellTime')
            sessionDwellTimeObject.append(dwellTimePerSlide)

        sessionDwellTimeObject.append(currentStudentID)
        sessionDwellTimeObject.append(userToken)
        dwellTimesAllSessionsList.append(sessionDwellTimeObject)

        #progress is between 0 and 1 (collected when the user closed the presentation)
        finalProgress = response[i].get('tracking_json').get('finalProgress')

        #LOGGING
        #print("number of slides: " + str(numberOfSlides))
        #print("URL: " + str(presentationUrl))
        #print("finalProgress: " + str(finalProgress))
        #print("session began at: " + str(timestampSessionBegin))
        #print("session updated at: " + str(timestampUpdated))
        #print(str(userToken))
        #print(str(sessionDwellTimeObject))

        #calculating the dwell time for each tracking session
        individualTotalDwellTime = response[i].get('tracking_json').get('totalDwellTime')
        seconds = float(individualTotalDwellTime[6:])
        minutes = float(individualTotalDwellTime[3:-3])
        hours = float(individualTotalDwellTime[:-6])
        totalDwellTimeSeconds = totalDwellTimeSeconds + seconds + (minutes * 60) + (hours * 60  * 60)

        sumProgress = sumProgress + finalProgress
        sumSlidesLookedAt = sumSlidesLookedAt + numberOfSlidesPerTrackingSession

        #insert all studentIDs (no duplicates) into a list to get number of students
        if currentStudentID not in arrayWithStudentIDs:
            arrayWithStudentIDs.append(currentStudentID)

    #calculating kpis
    numberOfStudents = len(arrayWithStudentIDs)
    averageDwellTime = totalDwellTimeSeconds/numberOfTrackedSessions
    averageProgress = sumProgress/numberOfTrackedSessions
    averageSlidesPerSession = sumSlidesLookedAt/numberOfTrackedSessions
    averageSlidesPerStudent = sumSlidesLookedAt/numberOfStudents

    numberOfQuizBeingDone = len(quizSessionList)

    #getting the number of quiz participants
    listWithStudentsParticipatedInQuiz = []
    for l in range(0, numberOfQuizBeingDone):
        studentId = quizSessionList[l][7]
        if studentId not in listWithStudentsParticipatedInQuiz:
            listWithStudentsParticipatedInQuiz.append(studentId)
    numberOfStudentsParticipatedInQuiz = len(listWithStudentsParticipatedInQuiz)

    #return JSON object with all the tracking data
    data = {}
    data['numberOfStudents'] = numberOfStudents
    data['numberOfTrackedSessions'] = numberOfTrackedSessions
    data['averageDwellTime'] = datetime.timedelta(seconds=(round(averageDwellTime)))
    data['averageProgress'] = round(averageProgress * 100)
    data['averageSlidesPerSession'] = averageSlidesPerSession
    data['averageSlidesPerStudent'] = averageSlidesPerStudent
    data['quizExisting'] = quizExisting
    data['numberOfStudentsParticipatedInQuiz'] = numberOfStudentsParticipatedInQuiz
    data['quizData'] = quizSessionList
    data['audioData'] = audioSessionList


    #LOGGING
    #print(str(dwellTimesAllSessionsList))
    #print("average Progress: " + str(averageProgress))
    #print("total dwell time in seconds: " + str(totalDwellTimeSeconds))
    #print("average dwell time is " + str(averageDwellTime) + " seconds")
    #print(type(response))
    #response = requests.get("http://localhost:4567/last-tracked").text
    #print("Das Quiz wurde " + str(len(quizSessionList)) + "-mal von " +
    #    str(numberOfStudentsParticipatedInQuiz) + " Studenten ausgefüllt")
    #print("QUIZ: " + str(quizSessionList))
    #print("AUDIO: " + str(audioSessionList))

    return render_template("dashboard.html", data=data)
