"""
 Les tests unitaires du pauvre ... ;o)

 A exécuter directement, de manière autonome

 @python-version 3.3.5
 @author fhill
 @since 2017.01.13

"""



# < Pour pouvoir lancer ce script depuis ici et quand même utiliser tous les autres modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\..\..')
print(sys.path)
# />



import json
from lib.tools.JsonReader import JsonReader
import logging.config



logging.config.fileConfig('../../conf/logging.conf')


print("\n\n")
print("#######################################################################")
print("# Testing JsonReader...")
print("#")
print("\n\n")



print("\n\n")
print("#======================================================================")
print("# Test case 1...")
print("\n\n")



json_str_0 = '''
{
	"first_name": "Fran",
	"last_name" :"Hills"
}
'''

json_str = '''
{
  "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
  "id": "10606",
  "self": "http://localhost:8080/rest/api/2/issue/10606",
  "key": "CMD-18",
  "fields": {
    "issuetype": {
      "self": "http://localhost:8080/rest/api/2/issuetype/10100",
      "id": "10100",
      "description": "Pour les paiements de commandes",
      "iconUrl": "http://localhost:8080/secure/viewavatar?size=xsmall&avatarId=10316&avatarType=issuetype",
      "name": "Paiement",
      "subtask": true,
      "avatarId": 10316
    },
    "parent": {
      "id": "10201",
      "key": "CMD-6",
      "self": "http://localhost:8080/rest/api/2/issue/10201",
      "fields": {
        "summary": "Plateau agile 6",
        "status": {
          "self": "http://localhost:8080/rest/api/2/status/10005",
          "description": "",
          "iconUrl": "http://localhost:8080/images/icons/statuses/generic.png",
          "name": "4-Saisie dans Chorus",
          "id": "10005",
          "statusCategory": {
            "self": "http://localhost:8080/rest/api/2/statuscategory/2",
            "id": 2,
            "key": "new",
            "colorName": "blue-gray",
            "name": "À faire"
          }
        },
        "priority": {
          "self": "http://localhost:8080/rest/api/2/priority/3",
          "iconUrl": "http://localhost:8080/images/icons/priorities/medium.svg",
          "name": "Medium",
          "id": "3"
        },
        "issuetype": {
          "self": "http://localhost:8080/rest/api/2/issuetype/10006",
          "id": "10006",
          "description": "",
          "iconUrl": "http://localhost:8080/secure/viewavatar?size=xsmall&avatarId=10300&avatarType=issuetype",
          "name": "Commande",
          "subtask": false,
          "avatarId": 10300
        }
      }
    },
    "components": [],
    "timespent": null,
    "timeoriginalestimate": null,
    "description": null,
    "project": {
      "self": "http://localhost:8080/rest/api/2/project/10000",
      "id": "10000",
      "key": "CMD",
      "name": "Commandes",
      "avatarUrls": {
        "48x48": "http://localhost:8080/secure/projectavatar?avatarId=10324",
        "24x24": "http://localhost:8080/secure/projectavatar?size=small&avatarId=10324",
        "16x16": "http://localhost:8080/secure/projectavatar?size=xsmall&avatarId=10324",
        "32x32": "http://localhost:8080/secure/projectavatar?size=medium&avatarId=10324"
      }
    },
    "fixVersions": [],
    "aggregatetimespent": null,
    "resolution": null,
    "customfield_10500": null,
    "customfield_10501": 666,
    "customfield_10502": 665,
    "customfield_10503": null,
    "customfield_10504": null,
    "aggregatetimeestimate": null,
    "resolutiondate": null,
    "workratio": -1,
    "summary": "VSR",
    "lastViewed": "2016-12-16T12:30:08.378+0100",
    "watches": {
      "self": "http://localhost:8080/rest/api/2/issue/CMD-18/watchers",
      "watchCount": 1,
      "isWatching": true
    },
    "creator": {
      "self": "http://localhost:8080/rest/api/2/user?username=alexis.grabie",
      "name": "alexis.grabie",
      "key": "alexis.grabie",
      "emailAddress": "alexis.grabie@agriculture.gouv.fr",
      "avatarUrls": {
        "48x48": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=48",
        "24x24": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=24",
        "16x16": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=16",
        "32x32": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=32"
      },
      "displayName": "alexis.grabie@agriculture.gouv.fr",
      "active": true,
      "timeZone": "Europe/Paris"
    },
    "customfield_10000": "0|i0003r:",
    "customfield_10001": null,
    "customfield_10002": null,
    "customfield_10301": null,
    "customfield_10400": "2016-08-25",
    "customfield_10500": null,
    "customfield_10501": 666.0,
    "customfield_10502": 665.0,
    "customfield_10503": null,
    "customfield_10504": null,
    "subtasks": [],
    "created": "2016-08-29T15:58:20.000+0200",
    "reporter": {
      "self": "http://localhost:8080/rest/api/2/user?username=alexis.grabie",
      "name": "alexis.grabie",
      "key": "alexis.grabie",
      "emailAddress": "alexis.grabie@agriculture.gouv.fr",
      "avatarUrls": {
        "48x48": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=48",
        "24x24": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=24",
        "16x16": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=16",
        "32x32": "http://www.gravatar.com/avatar/da9442243f6b8a2fe05812b87db2ce18?d=mm&s=32"
      },
      "displayName": "alexis.grabie@agriculture.gouv.fr",
      "active": true,
      "timeZone": "Europe/Paris"
    },
    "customfield_10000": "0|i0003r:",
    "aggregateprogress": {
      "progress": 0,
      "total": 0
    },
    "priority": {
      "self": "http://localhost:8080/rest/api/2/priority/3",
      "iconUrl": "http://localhost:8080/images/icons/priorities/medium.svg",
      "name": "Medium",
      "id": "3"
    },
    "customfield_10001": null,
    "customfield_10002": null,
    "labels": [],
    "customfield_10400": "2016-08-25",
    "customfield_10301": null,
    "environment": null,
    "timeestimate": null,
    "aggregatetimeoriginalestimate": null,
    "versions": [],
    "duedate": null,
    "progress": {
      "progress": 0,
      "total": 0
    },
    "issuelinks": [],
    "votes": {
      "self": "http://localhost:8080/rest/api/2/issue/CMD-18/votes",
      "votes": 0,
      "hasVoted": false
    },
    "assignee": null,
    "updated": "2016-12-16T12:30:07.000+0100",
    "status": {
      "self": "http://localhost:8080/rest/api/2/status/10102",
      "description": "Utilisé pour le paiement des commandes. Etat après saisi dans Chorus.",
      "iconUrl": "http://localhost:8080/images/icons/statuses/generic.png",
      "name": "4-Saisi par compta",
      "id": "10102",
      "statusCategory": {
        "self": "http://localhost:8080/rest/api/2/statuscategory/2",
        "id": 2,
        "key": "new",
        "colorName": "blue-gray",
        "name": "À faire"
      }
    }
  }
}
'''

jr = JsonReader(json_str)
#jr.setLogger(logging.getLogger("default"))

assert(jr.readSafe('fields', 'issuetype', 'name')               == 'Paiement')
assert(jr.readSafe('fields', 'NON_EXISTING_FIELD', 'name')      is None)
assert(jr.readSafe('NON_EXISTING_FIELD', 'issuetype', 'name')   is None)
assert(jr.readSafe('fields', 'issuetype', 'NON_EXISTING_FIELD') is None)
assert(jr.readSafe('fields', 'customfield_10001'              ) is None)
assert(jr.readSafe('fields', 'customfield_10001', 'any'       ) is None)   # customfield is explicitely NULL
assert(jr.readSafe('fields', 'customfield_10400', 'any'       ) is None)   # customfield has no sub-keys
assert(jr.readSafe('fields', 'customfield_10400', 'any', 'minee' ) is None)   # customfield has no sub-keys


none_val = 'SORRY NOTHING HERE'
jr = JsonReader(json_str, none_val)

assert(jr.readSafe('fields', 'issuetype', 'name')               == 'Paiement')
assert(jr.readSafe('fields', 'NON_EXISTING_FIELD', 'name')      == none_val)
assert(jr.readSafe('NON_EXISTING_FIELD', 'issuetype', 'name')   == none_val)
assert(jr.readSafe('fields', 'issuetype', 'NON_EXISTING_FIELD') == none_val)


jr = JsonReader(json.loads(json_str))

assert(jr.readSafe('fields', 'issuetype', 'name')               == 'Paiement')
assert(jr.readSafe('fields', 'NON_EXISTING_FIELD', 'name')      is None)
assert(jr.readSafe('NON_EXISTING_FIELD', 'issuetype', 'name')   is None)
assert(jr.readSafe('fields', 'issuetype', 'NON_EXISTING_FIELD') is None)
