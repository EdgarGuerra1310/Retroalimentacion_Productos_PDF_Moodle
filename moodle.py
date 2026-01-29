import requests

DOMAIN = "https://campusvirtual-sifods.minedu.gob.pe/webservice/rest/server.php"
TOKEN = "934a5bc65d092299e862902196a6f43b"

def get_assignid(course_id, cmid):
    params = {
        "wstoken": TOKEN,
        "wsfunction": "mod_assign_get_assignments",
        "moodlewsrestformat": "json",
        "courseids[0]": course_id
    }

    r = requests.get(DOMAIN, params=params, verify=False, timeout=30)
    r.raise_for_status()
    data = r.json()

    for course in data.get("courses", []):
        for assign in course.get("assignments", []):
            if assign.get("cmid") == cmid:
                return assign.get("id")

    return None


def get_submissions(assignid):
    params = {
        "wstoken": TOKEN,
        "wsfunction": "mod_assign_get_submissions",
        "moodlewsrestformat": "json",
        "assignmentids[0]": assignid
    }

    r = requests.get(DOMAIN, params=params, verify=False, timeout=30)
    r.raise_for_status()
    return r.json()